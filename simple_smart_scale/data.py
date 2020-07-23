import dill
import os
import datetime
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean
from math import sqrt
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

distribs = {
'gainer':[9.113924051, 12.07594937, 13.67088608, 15.03797468, 16.63291139, 17.7721519, 19.59493671, 20.50632911, 21.64556962, 22.32911392, 23.46835443, 24.37974684, 25.06329114, 25.74683544, 26.20253165, 26.88607595, 27.34177215, 28.02531646, 28.70886076, 29.39240506],
'stable':[0.683544304, 1.139240506, 1.82278481, 2.278481013, 2.962025316, 3.417721519, 3.873417722, 4.784810127, 5.240506329, 5.924050633, 6.835443038, 6.607594937, 7.063291139, 7.518987342, 7.746835443, 7.974683544, 7.974683544, 8.202531646, 7.974683544, 7.746835443],
'minimal loser':[-1.139240506, -1.367088608, -1.367088608, -1.594936709, -2.278481013, -2.050632911, -1.82278481, -2.050632911, -1.82278481, -1.594936709, -0.683544304, -0.455696203, -0.455696203, -0.683544304, -0.455696203, 0, 0, 0.227848101, -0.227848101, -0.227848101],
'regainer':[-2.962025316, -4.784810127, -5.240506329, -6.151898734, -6.379746835, -6.607594937, -6.835443038, -6.151898734, -6.379746835, -5.924050633, -5.696202532, -5.696202532, -5.924050633, -6.379746835, -7.291139241, -8.202531646, -9.341772152, -11.39240506, -13.67088608, -16.86075949],
'slow loser':[-5.924050633, -7.974683544, -9.341772152, -10.48101266, -11.62025316, -11.84810127, -11.84810127, -11.62025316, -11.16455696, -10.70886076, -9.569620253, -8.886075949, -7.974683544, -7.291139241, -6.151898734, -5.696202532, -5.240506329, -4.784810127, -4.784810127, -5.012658228],
'moderate loser':[-6.835443038, -9.797468354, -12.30379747, -14.12658228, -15.72151899, -16.86075949, -17.5443038, -17.5443038, -17.3164557, -17.3164557, -16.63291139, -15.94936709, -15.72151899, -15.26582278, -15.03797468, -15.49367089, -15.94936709, -17.08860759, -18.4556962, -20.50632911],
'large loser':[-10.93670886, -15.49367089, -20.05063291, -23.01265823, -26.20253165, -27.56962025, -28.93670886, -29.62025316, -30.30379747, -29.84810127, -29.39240506, -28.70886076, -28.02531646, -26.65822785, -25.97468354, -24.83544304, -24.15189873, -23.69620253, -23.69620253, -24.15189873]
}

def interpolate_trimonth_pcts_to_monthly(weightgainpcts):
    ret = []
    vals = [0] + weightgainpcts
    l = len(vals)
    for i in range(1, l):
        bottom = vals[i-1]
        top = vals[i]
        rnge = top-bottom
        ret.append(rnge*1/3-bottom)
        ret.append(rnge*2/3-bottom)
        ret.append(top)
    return ret

interp_distribs = {k: interpolate_trimonth_pcts_to_monthly(v) for k,v in distribs.items()}

def daily_weights_to_monthly_pcts(weight_pairs):
    avg_days_in_month = datetime.timedelta(days=30.42)
    offset = datetime.timedelta(days=0)
    weight_pairs = [pair[:] for pair in weight_pairs]
    buf = []
    ret = []
    orig_weight, startdate = weight_pairs[0]
    while weight_pairs:
        buf = [x[0] for x in weight_pairs if (x[1]-startdate) >= offset and (x[1] - startdate) < offset + avg_days_in_month]
        weight_pairs = [x for x in weight_pairs if  (x[1] - startdate) > offset + avg_days_in_month]
        
        month_avg = mean(buf)
        ret.append(month_avg / orig_weight)
        offset += avg_days_in_month
    return ret

# makes two lists of the same length
def justify_lists(l1, l2): 
    return list(zip(*zip(l1, l2)))

# assumes the two lists are justified to the same length
def euclidean_dist(l1,l2):
    tot = 0
    for i in range(len(l1)):
        tot += (l1[i]-l2[i]) ** 2
    return sqrt(tot)

# also assumes justification
def covariance_dist(l1, l2):
    mean_l1 = sum(l1) / len(l1)
    mean_l2 = sum(l2) / len(l2)
    return sum((a - mean_l1) * (b - mean_l2) for (a,b) in zip(l1,l2)) / len(l1)

# calc dist between 2 timeseries
def full_dist(l1, l2):
    a,b = justify_lists(l1, l2)
    e = euclidean_dist(a, b)
    c = covariance_dist(a,b)
    return e + c

def get_NN_classification():
    weight_pcts_mthly = daily_weights_to_monthly_pcts(get_weight_history())
    distrib_dists = {k: full_dist(weight_pcts_mthly, v) for k,v in interp_distribs.items()}
    distrib_ord = list(sorted([(k,v) for k,v in distrib_dists.items()], key=lambda x: x[1]))
    closest_class = distrib_ord[0][0]
    maxdist = distrib_ord[-1][-1]
    distrib_closenesses = {k: 1 - v/maxdist for k,v in distrib_dists.items()}
    return (closest_class, distrib_closenesses)

