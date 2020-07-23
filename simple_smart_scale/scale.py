import random
import time

# this is for testing purposes
# allows the GUI to run when not running on RPI
config = 'real'
try:
    import board
except:
    config = 'rand'

def scale_running_avg(readers, spec = 4):
    avg = 0
    cnt = 0
    d = float('inf')

    while d > spec or cnt < 150:
        cnt += 1
        total_readout = sum([reader.value for reader in readers])
        diff = total_readout - avg
        tmp = avg
        avg += diff/cnt
        d = abs(avg - tmp)
    
    return avg

# returns a partially complete scale config list
def configure_zero():
    # these imports are only needed here
    # and some of these packages are RPI specific!
    import board
    import busio
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn

    initialized = False
    readers = None
    while not initialized:
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            readers = []
            # this should end up initializing 4 scale readers
            for n in [0x48,0x49]:
                ads = ADS.ADS1115(i2c, address=n)
                reader = AnalogIn(ads, ADS.P0, ADS.P1)
                readers.append(reader)
                reader = AnalogIn(ads, ADS.P2, ADS.P3)
                readers.append(reader)
            initialized = True
        except:
            print('scale initializer err!')
    
    zero = scale_running_avg(readers)
    config = [readers, zero, None]
    return config

# takes a partial scale config list and computes the kg_per_step
# mutates the list. returns nothing
def configure_20kg(config_list):
    readers, zero, kg_per_step = config_list
    off = scale_running_avg(readers)
    weight = 20
    kg_per_step = weight/(off - zero)
    config_list[-1] = kg_per_step
    return
 
def get_weight(readers, zero, kg_per_step):
    
    steps = scale_running_avg(readers, spec=8)

    w = (steps - zero) * kg_per_step
    print(f'weight: {w}')
    return w

weight_opts = {
    'rand': lambda x,y,z: float(random.randint(0,250)),
    'real': get_weight
}

weigh_func = weight_opts[config]