import PySimpleGUI as sg
import simple_smart_scale.scale as scale
import simple_smart_scale.data as data

graph_loc = data.graph_loc
weight_loc = data.weights_loc


def main():

    # this whole section builds the skeleton for the GUI layout
    graphcol = [
        [sg.Text('Weight Graph', key='graphlabel', auto_size_text=True)],
        [sg.Image(key="-IMAGE-")]
    ]

    buttoncol = [
        [sg.Button('tare')],
        [sg.Button('calibrate (20kg)')],
        [sg.Button('weigh')],
        [sg.Button('classify')]
    ]

    def label_pair_producer(label, font = None):
        lbl = sg.Text(key=label, text=label + ': ', font= font, auto_size_text=True)
        val = sg.Text(key=label+'_val', text='_',size=(6, 1))
        return [lbl, val]

    classifications = [
        label_pair_producer('gainer'),
        label_pair_producer('stable'),
        label_pair_producer('minimal loser'),
        label_pair_producer('regainer'),
        label_pair_producer('slow loser'),
        label_pair_producer('moderate loser'),
        label_pair_producer('large loser')
    ]

    # finalize and render the starting layout
    buttoncol.append([sg.HorizontalSeparator()])
    buttoncol.extend(classifications)
    layout = [
        [
            sg.Column(graphcol),
            sg.VSeperator(),
            sg.Column(buttoncol),
        ],
        [sg.HorizontalSeparator()],
        label_pair_producer('weight', font=('Helvetica', '17')),
        label_pair_producer('class', font=('Helvetica', '15')),
    ]

    # some basic setup
    window = sg.Window("Image Viewer", layout)
    window.finalize()
    window["-IMAGE-"].update(filename=graph_loc)
    scale_config = [None, None, None]
    weight = None
    
    # main event loop
    # this is where the interactive logic happens
    while True:
        event, values = window.read()

        # exit appropriately
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        # zero the scale and get a config
        if event == 'tare':
            scale_config = scale.configure_zero()
            window['weight_val'].update('0.00')

        # calibrate to 20kg to prepare for weighing
        if event == 'calibrate (20kg)':
            scale.configure_20kg(scale_config)
            window['weight_val'].update('20.00')

        # get a valid weight and display it
        if event == 'weigh':
            try:
                weight = scale.weigh_func(*scale_config)
                window['weight_val'].update(f'{weight:.2f}')
                data.update_weight_data(weight)
            except Exception as e:
                print(e)
        
        # generate graph, save it
        # run dataframe through classifier
        if event == 'classify':
            True

        # just update the image every time
        try:
            window["-IMAGE-"].update(filename=graph_loc)
        except:
            pass

    window.close()
    return

if __name__ == "__main__":
    main()