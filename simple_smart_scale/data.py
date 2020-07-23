import dill
import os
import datetime
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

sns.set()

weights_loc = './weights.dill'
graph_loc = './weight_graph.png'

# get the data
def get_weight_history():
    if os.path.isfile(weights_loc):
        with open(weights_loc, mode='rb') as f:
            weights = dill.load(f)
        return weights
    else:
        return None
    return

# update weight data
def update_weight_data(weight):
    weightdata = get_weight_history()
    now = datetime.datetime.today()
    if weightdata is None:
        weightdata = []
    weightdata.append((weight, now))

    with open(weights_loc, mode='wb') as f:
        dill.dump(weightdata, f)
    
    weights, dates = list(zip(*weightdata))
    start = dates[0]
    seconds_since = [(timestamp - start).total_seconds() for timestamp in dates]
    
    # save the new graph
    df = pd.DataFrame({'weight (kg)': weights, 'seconds since first weigh-in': seconds_since})
    ax = sns.lineplot(y="weight (kg)", x="seconds since first weigh-in", data=df, marker='.', fillstyle='full', color='tab:blue', markeredgewidth=0)
    plt.savefig(graph_loc)
    return

