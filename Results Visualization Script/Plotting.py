"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

IMPORTING LIBRARIES

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import itertools
from plotly.subplots import make_subplots

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Plotting Bar Graphs

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

data  = pd.read_excel('20.xlsx')
dataK = pd.read_excel('Kubernetes Microservice CPU Utilization.xlsx')
# data.head()

case = 0         # Specify case as index from scenarios such as 0 implies 20-2
scenarios = np.array(("20-2","50-2","80-2","20-5","50-5","80-5","20-10","50-10","80-10"))

replica = int(scenarios[case][3:5])
Threshold = int(scenarios[case][0:2])

st = str(Threshold)+"-"+str(replica);
front_end = pd.DataFrame([data[st+".1"],data[st+".2"],data[st+".3"],data[st+".4"],data[st+".5"],data[st+".6"],data[st+".7"],data[st+".8"],data[st+".9"],data[st+".10"],data[st+".11"]])
front_end = front_end.T
# front_end.head()


front_endK = pd.DataFrame([dataK[st+".1"],dataK[st+".2"],dataK[st+".3"],dataK[st+".4"],dataK[st+".5"],dataK[st+".6"],dataK[st+".7"],dataK[st+".8"],dataK[st+".9"],dataK[st+".10"],dataK[st+".11"]])
front_endK = front_endK.T
# front_endK.head()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Data Frame for CPU OverUtilization

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

services_sheets = np.array(("cartsevice","checkout","adservice","frontend","currency","payment","productcatalogue","recommendation","shipping","email","rediscart"))
scenarios = np.array(("20-2","50-2","80-2","20-5","50-5","80-5","20-10","50-10","80-10"))
multi_ser_data1 = pd.DataFrame()
services_sheets = np.array(("frontend","adservice","cartsevice","checkout","currency","payment","email","productcatalogue","recommendation","shipping","rediscart"))


current_scenario = scenarios[case]

for i in range(11):

    my_dict = {}
    var_name = services_sheets[i]
    my_dict[var_name] = pd.read_excel('Compiled Results.xlsx',i+1)
    value = my_dict[var_name]

    Avg_CPU_OvUt = value[value.iloc[:,1] == 'Avg CPU OverUtilization']
    Avg_CPU_OvUt.insert(1, "rep", np.zeros(9))
    Avg_CPU_OvUt.iloc[0:3,1] = 2*np.ones(3)
    Avg_CPU_OvUt.iloc[3:6,1] = 5*np.ones(3)
    Avg_CPU_OvUt.iloc[6:9,1] = 10*np.ones(3)


    
    Avg_CPU_OvUt.iloc[np.double(np.linspace(0,9,4)[:-1]).astype(int),0] = 20*np.ones(3)
    Avg_CPU_OvUt.iloc[np.double(np.linspace(1,10,4)[:-1]).astype(int),0] = 50*np.ones(3)
    Avg_CPU_OvUt.iloc[np.double(np.linspace(2,11,4)[:-1]).astype(int),0] = 80*np.ones(3)
    
    

    temp = pd.DataFrame(Avg_CPU_OvUt.iloc[case,0:5]).T
    temp["service"] = var_name
    multi_ser_data1 = pd.concat([multi_ser_data1, temp], axis=0)
    

multi_ser_data1["sortDind"] = np.array(multi_ser_data1.iloc[:,3].argsort()[::-1][:11])
multi_ser_data1["sortDval"] = np.sort(multi_ser_data1.iloc[:,3])[::-1]

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Data Frame for Overutilization Times

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

services_sheets = np.array(("frontend","adservice","cartsevice","checkout","currency","payment","email","productcatalogue","recommendation","shipping","rediscart"))

multi_ser_data2 = pd.DataFrame()

for i in range(11):

    my_dict = {}
    var_name = services_sheets[i]
    my_dict[var_name] = pd.read_excel('Compiled Results.xlsx',i+1)
    value = my_dict[var_name]

    Avg_CPU_OvUt = value[value.iloc[:,1] == 'Overutilization Times']
    Avg_CPU_OvUt.insert(1, "rep", np.zeros(9))
    Avg_CPU_OvUt.iloc[0:3,1] = 2*np.ones(3)
    Avg_CPU_OvUt.iloc[3:6,1] = 5*np.ones(3)
    Avg_CPU_OvUt.iloc[6:9,1] = 10*np.ones(3)


    
    Avg_CPU_OvUt.iloc[np.double(np.linspace(0,9,4)[:-1]).astype(int),0] = 20*np.ones(3)
    Avg_CPU_OvUt.iloc[np.double(np.linspace(1,10,4)[:-1]).astype(int),0] = 50*np.ones(3)
    Avg_CPU_OvUt.iloc[np.double(np.linspace(2,11,4)[:-1]).astype(int),0] = 80*np.ones(3)
    
    

    temp = pd.DataFrame(Avg_CPU_OvUt.iloc[case,0:5]).T
    temp["service"] = var_name
    multi_ser_data2 = pd.concat([multi_ser_data2, temp], axis=0)
    

multi_ser_data2["sortDind"] = np.array(multi_ser_data1.iloc[:,3].argsort()[::-1][:11])
multi_ser_data2["sortDval"] = np.sort(multi_ser_data2.iloc[:,3])[::-1]


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Data Frame for CPU Utilization

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

services_sheets = np.array(("frontend","adservice","cartsevice","checkout","currency","payment","email","productcatalogue","recommendation","shipping","rediscart"))

multi_ser_data4 = pd.DataFrame()

for i in range(11):

    my_dict = {}
    var_name = services_sheets[i]
    my_dict[var_name] = pd.read_excel('Compiled Results.xlsx',i+1)
    value = my_dict[var_name]

    Avg_CPU_OvUt = value[value.iloc[:,1] == 'Avg CPU Utilization']
    Avg_CPU_OvUt.insert(1, "rep", np.zeros(9))
    Avg_CPU_OvUt.iloc[0:3,1] = 2*np.ones(3)
    Avg_CPU_OvUt.iloc[3:6,1] = 5*np.ones(3)
    Avg_CPU_OvUt.iloc[6:9,1] = 10*np.ones(3)


    
    Avg_CPU_OvUt.iloc[np.double(np.linspace(0,9,4)[:-1]).astype(int),0] = 20*np.ones(3)
    Avg_CPU_OvUt.iloc[np.double(np.linspace(1,10,4)[:-1]).astype(int),0] = 50*np.ones(3)
    Avg_CPU_OvUt.iloc[np.double(np.linspace(2,11,4)[:-1]).astype(int),0] = 80*np.ones(3)
    
    

    temp = pd.DataFrame(Avg_CPU_OvUt.iloc[case,0:5]).T
    temp["service"] = var_name
    temp.iloc[:,3]
    multi_ser_data4 = pd.concat([multi_ser_data4, temp], axis=0)
    

multi_ser_data4["sortDind"] = np.array(multi_ser_data1.iloc[:,3].argsort()[::-1][:11])
multi_ser_data4["sortDval"] = np.sort(multi_ser_data4.iloc[:,3])[::-1]

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Data Frame for Overprovisioned CPU

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

services_sheets = np.array(("frontend","adservice","cartsevice","checkout","currency","payment","email","productcatalogue","recommendation","shipping","rediscart"))

multi_ser_data5 = pd.DataFrame()

for i in range(11):

    my_dict = {}
    var_name = services_sheets[i]
    my_dict[var_name] = pd.read_excel('Compiled Results.xlsx',i+1)
    value = my_dict[var_name]

    Avg_CPU_OvUt = value[value.iloc[:,1] == 'Avg Overprovisioned CPU']
    Avg_CPU_OvUt.insert(1, "rep", np.zeros(9))
    Avg_CPU_OvUt.iloc[0:3,1] = 2*np.ones(3)
    Avg_CPU_OvUt.iloc[3:6,1] = 5*np.ones(3)
    Avg_CPU_OvUt.iloc[6:9,1] = 10*np.ones(3)


    
    Avg_CPU_OvUt.iloc[np.double(np.linspace(0,9,4)[:-1]).astype(int),0] = 20*np.ones(3)
    Avg_CPU_OvUt.iloc[np.double(np.linspace(1,10,4)[:-1]).astype(int),0] = 50*np.ones(3)
    Avg_CPU_OvUt.iloc[np.double(np.linspace(2,11,4)[:-1]).astype(int),0] = 80*np.ones(3)
    
    

    temp = pd.DataFrame(Avg_CPU_OvUt.iloc[case,0:5]).T
    temp["service"] = var_name
    temp.iloc[:,3]
    multi_ser_data5 = pd.concat([multi_ser_data5, temp], axis=0)
    

multi_ser_data5["sortDind"] = np.array(multi_ser_data1.iloc[:,3].argsort()[::-1][:11])
multi_ser_data5["sortDval"] = np.sort(multi_ser_data5.iloc[:,3])[::-1]

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Data Frame for Underprovisioned CPU

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

services_sheets = np.array(("frontend","adservice","cartsevice","checkout","currency","payment","email","productcatalogue","recommendation","shipping","rediscart"))

multi_ser_data6 = pd.DataFrame()

for i in range(11):

    my_dict = {}
    var_name = services_sheets[i]
    my_dict[var_name] = pd.read_excel('Compiled Results.xlsx',i+1)
    value = my_dict[var_name]

    Avg_CPU_OvUt = value[value.iloc[:,1] == 'Avg Underprovisioned CPU']
    Avg_CPU_OvUt.insert(1, "rep", np.zeros(9))
    Avg_CPU_OvUt.iloc[0:3,1] = 2*np.ones(3)
    Avg_CPU_OvUt.iloc[3:6,1] = 5*np.ones(3)
    Avg_CPU_OvUt.iloc[6:9,1] = 10*np.ones(3)


    
    Avg_CPU_OvUt.iloc[np.double(np.linspace(0,9,4)[:-1]).astype(int),0] = 20*np.ones(3)
    Avg_CPU_OvUt.iloc[np.double(np.linspace(1,10,4)[:-1]).astype(int),0] = 50*np.ones(3)
    Avg_CPU_OvUt.iloc[np.double(np.linspace(2,11,4)[:-1]).astype(int),0] = 80*np.ones(3)
    
    

    temp = pd.DataFrame(Avg_CPU_OvUt.iloc[case,0:5]).T
    temp["service"] = var_name
    temp.iloc[:,3]
    multi_ser_data6 = pd.concat([multi_ser_data6, temp], axis=0)


multi_ser_data6["sortDind"] = np.array(multi_ser_data1.iloc[:,3].argsort()[::-1][:11])
multi_ser_data6["sortDval"] = np.sort(multi_ser_data6.iloc[:,3])[::-1]

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Data Frame for Supply CPU

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

services_sheets = np.array(("frontend","adservice","cartsevice","checkout","currency","payment","email","productcatalogue","recommendation","shipping","rediscart"))

multi_ser_data7 = pd.DataFrame()

for i in range(11):

    my_dict = {}
    var_name = services_sheets[i]
    my_dict[var_name] = pd.read_excel('Compiled Results.xlsx',i+1)
    value = my_dict[var_name]

    Avg_CPU_OvUt = value[value.iloc[:,1] == 'Avg Supply CPU']
    Avg_CPU_OvUt.insert(1, "rep", np.zeros(9))
    Avg_CPU_OvUt.iloc[0:3,1] = 2*np.ones(3)
    Avg_CPU_OvUt.iloc[3:6,1] = 5*np.ones(3)
    Avg_CPU_OvUt.iloc[6:9,1] = 10*np.ones(3)


    
    Avg_CPU_OvUt.iloc[np.double(np.linspace(0,9,4)[:-1]).astype(int),0] = 20*np.ones(3)
    Avg_CPU_OvUt.iloc[np.double(np.linspace(1,10,4)[:-1]).astype(int),0] = 50*np.ones(3)
    Avg_CPU_OvUt.iloc[np.double(np.linspace(2,11,4)[:-1]).astype(int),0] = 80*np.ones(3)
    
    

    temp = pd.DataFrame(Avg_CPU_OvUt.iloc[case,0:5]).T
    temp["service"] = var_name
    temp.iloc[:,3]
    multi_ser_data7 = pd.concat([multi_ser_data7, temp], axis=0)


multi_ser_data7["sortDind"] = np.array(multi_ser_data1.iloc[:,3].argsort()[::-1][:11])
multi_ser_data7["sortDval"] = np.sort(multi_ser_data7.iloc[:,3])[::-1]

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Data Frame for Overprovisioned Time

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# services_sheets = np.array(("cartsevice","checkout","adservice","frontend","currency","payment","productcatalogue","recommendation","shipping","email","rediscart"))
services_sheets = np.array(("frontend","adservice","cartsevice","checkout","currency","payment","email","productcatalogue","recommendation","shipping","rediscart"))

multi_ser_dataa = pd.DataFrame()

# for i in range(11):

my_dict = {}
var_name = services_sheets[i]
my_dict[var_name] = pd.read_excel('Compiled Results.xlsx',12)
value = my_dict[var_name]

Avg_CPU_OvUt = value[value.iloc[:,1] == 'Avg Overprovisioned Time']
Avg_CPU_OvUt.insert(1, "rep", np.zeros(9))
Avg_CPU_OvUt.iloc[0:3,1] = 2*np.ones(3)
Avg_CPU_OvUt.iloc[3:6,1] = 5*np.ones(3)
Avg_CPU_OvUt.iloc[6:9,1] = 10*np.ones(3)


Avg_CPU_OvUt.iloc[np.double(np.linspace(0,9,4)[:-1]).astype(int),0] = 20*np.ones(3)
Avg_CPU_OvUt.iloc[np.double(np.linspace(1,10,4)[:-1]).astype(int),0] = 50*np.ones(3)
Avg_CPU_OvUt.iloc[np.double(np.linspace(2,11,4)[:-1]).astype(int),0] = 80*np.ones(3)
temp = Avg_CPU_OvUt.iloc[:,0:5]  

Avg_CPU_OvUt = value[value.iloc[:,1] == 'Avg Underprovisioned Time']
Avg_CPU_OvUt = Avg_CPU_OvUt.iloc[:,1:4]  
temp = pd.concat([temp, Avg_CPU_OvUt.set_axis(temp.index)], axis=1)

Avg_CPU_OvUt = value[value.iloc[:,1] == 'Avg Overutilization Time']
Avg_CPU_OvUt = Avg_CPU_OvUt.iloc[:,1:4]  
temp = pd.concat([temp, Avg_CPU_OvUt.set_axis(temp.index)], axis=1)

Avg_CPU_OvUt = value[value.iloc[:,1] == 'Avg Overutilization Time']
Avg_CPU_OvUt = Avg_CPU_OvUt.iloc[:,1:4]  

multi_ser_dataa = pd.concat([temp, Avg_CPU_OvUt.set_axis(temp.index)], axis=1)

multi_ser_dataa.columns = np.arange(multi_ser_dataa.shape[1])

multi_ser_dataa.iloc[:,8] = 'Avg Utilization Time'
multi_ser_dataa.iloc[:,9] = 900*np.ones(len(multi_ser_dataa))
multi_ser_dataa.iloc[:,10] = 900*np.ones(len(multi_ser_dataa))

for j in [3,4,6,7,9,10,12,13]:
    multi_ser_dataa[j] = multi_ser_dataa[j]/60

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Plotting Bar graph for all parameters

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

sz1 = 18
sz = 14
animals=np.array(("SmartHPA","Kubernetes")) 

t = multi_ser_dataa.iloc[:,3]+multi_ser_dataa.iloc[:,6]
multi_ser_dataa.iloc[:,3] = (multi_ser_dataa.iloc[:,3]/t)*15
multi_ser_dataa.iloc[:,6] =  (multi_ser_dataa.iloc[:,6]/t)*15

t = multi_ser_dataa.iloc[:,4]+multi_ser_dataa.iloc[:,7]
multi_ser_dataa.iloc[:,4] = (multi_ser_dataa.iloc[:,4]/t)*15
multi_ser_dataa.iloc[:,7] =  (multi_ser_dataa.iloc[:,7]/t)*15

bar_colors = px.colors.qualitative.Vivid[0:11]

k1 = multi_ser_data1 # Overutilization CPU
k2 = multi_ser_data2 # Overutilization Time
k3 = multi_ser_data3 # Overutilization Area
k4 = multi_ser_data4 # Utilization CPU
k5 = multi_ser_data5 # Overprovisioned CPU
k6 = multi_ser_data6 # Underprovisioned CPU
k7 = multi_ser_data7 # Supply CPU


fig = make_subplots(
    rows=2, cols=4,
    shared_xaxes=True,
    horizontal_spacing=0.07,
    vertical_spacing=0.01,
    subplot_titles=("Supply CPU","Overutilization", "Overprovision","Underprovision"),
    specs=[[{"type": "bar"}, {"type": "bar"},{"type": "bar"},{"type": "bar"}],[{"type": "table"}, {"type": "table"},{"type": "table"},{"type": "table"}]]
)


for i in range(11): 
    fig.add_trace(go.Bar(x=["2 "],y=[k7.iloc[i,3]],name="SmartHPA",marker_color=bar_colors[i],width=0.4),row=1,col=1)
                  
for i in range(11):     
    fig.add_trace(go.Bar(x=["3 "],y=[k7.iloc[i,4]],name="KHPA",marker_color=bar_colors[i],width=0.4),row=1,col=1)

fig.update_layout(barmode='stack')

fig.add_trace(
    go.Table(
        header=dict(
            values=["{:.2f}".format(15),"{:.2f}".format(15)],
            font=dict(size=sz1),
            align="center")
    ),
    row=2, col=1
)


for i in range(11): 
    fig.add_trace(go.Bar(x=[" 2"],y=[k1.iloc[i,3]],name="SmartHPA",marker_color=bar_colors[i],width=0.4),row=1,col=2)
for i in range(11):     
    fig.add_trace(go.Bar(x=[" 6"],y=[k1.iloc[i,4]],name="KHPA",marker_color=bar_colors[i],width=0.4),row=1,col=2)
fig.update_layout(barmode='stack')
fig.add_trace(
    go.Table(
        header=dict(
            values=[
           "{:.2f}".format(multi_ser_dataa.iloc[case,12]),"{:.2f}".format(multi_ser_dataa.iloc[case,13])
        ],
            font=dict(size=sz1),
            align="center")
    ),
    row=2, col=2
)

for i in range(11): 
    fig.add_trace(go.Bar(x=[" 3"],y=[k5.iloc[i,3]],name="SmartHPA",marker_color=bar_colors[i],width=0.4),row=1,col=3)
for i in range(11):     
    fig.add_trace(go.Bar(x=["5 "],y=[k5.iloc[i,4]],name="KHPA",marker_color=bar_colors[i],width=0.4),row=1,col=3)

fig.update_layout(barmode='stack')
fig.add_trace(
    go.Table(
        header=dict(
            values=["{:.2f}".format(multi_ser_dataa.iloc[case,3]), "{:.2f}".format(multi_ser_dataa.iloc[case,4])],
            font=dict(size=sz1),
            align="center")
    ),
    row=2, col=3
)

if case==8:
    fig.add_trace(go.Bar(y=[]),row=1,col=4)
else:
    for i in range(11): 
        fig.add_trace(go.Bar(x=["2 "],y=[k6.iloc[i,3]],name="SmartHPA",marker_color=bar_colors[i],width=0.4),row=1,col=4)
    for i in range(11):     
        fig.add_trace(go.Bar(x=["1 "],y=[k6.iloc[i,4]],name="KHPA",marker_color=bar_colors[i],width=0.4),row=1,col=4)


fig.update_layout(barmode='stack')
fig.add_trace(
    go.Table(
        header=dict(
        values=[
           "{:.2f}".format(multi_ser_dataa.iloc[case,6]),"{:.2f}".format(multi_ser_dataa.iloc[case,7])
        ],
        font=dict(size=sz1),
        align = "center")
    ),
    row=2, col=4
)

fig.update_traces(width=0.7,selector=dict(name='KHPA'))      
fig.update_traces(width=0.7,marker_pattern_shape="/",selector=dict(name='SmartHPA'))


fig.update_layout(
    autosize=False,
    height=600,
    margin=dict(l=80, r=80, t=100, b=80),
    showlegend = False,
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
    plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot background
)
fig.update_xaxes(
    mirror=True,
    showline=True,
    linecolor='black',
    gridcolor='White'
)
fig.update_yaxes(
    mirror=True,
    ticklen=5,
    showline=True,
    linecolor='black',
    gridcolor='White'
)


fig.update_yaxes(tickfont=dict(size=sz),tickformat='.2s',ticklabelposition="outside", row=1, col=1)
fig.update_yaxes(tickfont=dict(size=sz),tickformat='.2s',ticklabelposition="outside", row=1, col=2)
fig.update_yaxes(tickfont=dict(size=sz),tickformat=',.2s',ticklabelposition="outside", row=1, col=3)
fig.update_yaxes(tickfont=dict(size=sz),tickformat=',.2s',ticklabelposition="outside", row=1, col=4)
if case==8:
    fig.update_yaxes(tickfont=dict(size=sz),showticklabels=False,tickformat=',.2s', row=1, col=4)
    



fig.update_xaxes(tickvals=[])
fig.show()
# fig.write_image("smBar"+current_scenario+".eps")


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Plotting CPU Utilization for SmartHPA

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

data  = pd.read_excel('20.xlsx')
dataK = pd.read_excel('Kubernetes Microservice CPU Utilization.xlsx')
data.head()
random_x = data['Sampled Time']/60

replica = 5
Threshold = 50
st = str(Threshold)+"-"+str(replica);
front_end = pd.DataFrame([data[st+".1"],data[st+".2"],data[st+".3"],data[st+".4"],data[st+".5"],data[st+".6"],data[st+".7"],data[st+".8"],data[st+".9"],data[st+".10"],data[st+".11"]])
front_end = front_end.T
front_end.head()


front_endK = pd.DataFrame([dataK[st+".1"],dataK[st+".2"],dataK[st+".3"],dataK[st+".4"],dataK[st+".5"],dataK[st+".6"],dataK[st+".7"],dataK[st+".8"],dataK[st+".9"],dataK[st+".10"],dataK[st+".11"]])
front_endK = front_endK.T
front_endK.head()



import itertools
import plotly.express as px
from plotly.subplots import make_subplots

mask = front_end > Threshold
maskK = front_endK > Threshold

col_pal = px.colors.sequential.Viridis
col_pal_iterator = itertools.cycle(col_pal) 
fig = go.Figure()

fig = make_subplots(rows=1,cols=2)

labels_to_show_in_legend = np.array(("frontend","adservice","cartsevice","checkout","currency","payment","email","productcatalogue","recommendation","shipping","rediscart"))

for i in range(11):

    new_colour = px.colors.qualitative.Vivid[i]
    fig.add_trace(go.Scatter(x=random_x, y=front_end.iloc[:,i],line = dict(color = new_colour),name=labels_to_show_in_legend[i]),row=1, col=1)
    fig.add_trace(go.Scatter(x=random_x, y=Threshold*np.ones(len(front_end)),
                        mode='lines' , line=dict(dash='dot',color='rgb(255,0,0)'), name='Threshold CPU'),row=1, col=1)
#     fig.add_trace(go.Scatter(x=random_x, y=front_end[mask].iloc[:,i],fill='tonexty',fillcolor='rgba('+new_colour[4:-1]+', 0.1)',line=dict(color='rgba('+new_colour[4:-1]+', 0.1)')),row=1, col=1)    
    fig.update_xaxes(title_text=" ", row=1, col=1)
    fig.update_yaxes(title_text='CPU Utilization (Percentage)', row=1, col=1)
    fig.update_yaxes(rangemode = 'tozero')

for i in range(11):

    new_colour = px.colors.qualitative.Vivid[i]
    fig.add_trace(go.Scatter(x=random_x, y=front_endK.iloc[:,i],line = dict(color = new_colour)),row=1, col=2)
    fig.add_trace(go.Scatter(x=random_x, y=Threshold*np.ones(len(front_endK)),
                        mode='lines' , line=dict(dash='dashdot',color='rgb(255,0,0)'), name='Threshold CPU'),row=1, col=2)
#     fig.add_trace(go.Scatter(x=random_x, y=front_endK[maskK].iloc[:,i],fill='tonexty',fillcolor='rgba('+new_colour[4:-1]+', 0.1)',line=dict(color='rgba('+new_colour[4:-1]+', 0.1)')),row=1, col=2)
    fig.update_xaxes(title_text=" ", row=1, col=2)
    fig.update_yaxes(title_text='CPU Utilization (Percentage)', row=1, col=2)
    fig.update_yaxes(rangemode = 'tozero')


for trace in fig['data']: 
    if (not trace['name'] in labels_to_show_in_legend):
        trace['showlegend'] = False
        
fig.update_layout(legend=dict(orientation='h',bgcolor="White",bordercolor="Black"))
fig.update_layout(legend_traceorder="normal")
    
fig.show()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Capacity and Demand for SmartHPA

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

data  = pd.read_excel('Smart HPA CPU Capacity.xlsx')
dataK = pd.read_excel('Demand CPU of all MS for all scenarios.xlsx')
data.head()

case = 4
scenarios = np.array(("20-2","50-2","80-2","20-5","50-5","80-5","20-10","50-10","80-10"))

replica = int(scenarios[case][3:5])
Threshold = int(scenarios[case][0:2])

st = str(Threshold)+"-"+str(replica);
front_end2 = pd.DataFrame([data[st+".1"],data[st+".2"],data[st+".3"],data[st+".4"],data[st+".5"],data[st+".6"],data[st+".7"],data[st+".8"],data[st+".9"],data[st+".10"],data[st+".11"]])
front_end2 = front_end2.T
front_end2.head()


front_endK2 = pd.DataFrame([dataK[st+".1"],dataK[st+".2"],dataK[st+".3"],dataK[st+".4"],dataK[st+".5"],dataK[st+".6"],dataK[st+".7"],dataK[st+".8"],dataK[st+".9"],dataK[st+".10"],dataK[st+".11"]])
front_endK2 = front_endK2.T
front_endK2.head()

fig = go.Figure()
for i in range(11):
#     maskK = front_end.iloc[:,i] < front_endK.iloc[:,i]
    new_colour = px.colors.qualitative.Vivid[i]
    fig.add_trace(go.Scatter(x=random_x, y=front_end2.iloc[:,i],line = dict(dash='dash',color = new_colour),name=labels_to_show_in_legend[i]))
#     fig.add_trace(go.Scatter(x=random_x, y=front_endK.iloc[:,i],fill='tonexty',fillcolor='rgba('+new_colour[4:-1]+', 0.1)',line=dict(color='rgba('+new_colour[4:-1]+', 0.1)')))
    
    fig.add_trace(go.Scatter(x=random_x, y=front_endK2.iloc[:,i],line = dict(color = new_colour)))
#     fig.add_trace(go.Scatter(x=random_x, y=Threshold*np.ones(len(front_end)),mode='lines' , line=dict(dash='dot',color='rgb(255,0,0)'), name='Threshold CPU'))
   
    fig.update_xaxes(titlefont=dict(size=40),title_text="Time (min)")
    fig.update_yaxes(titlefont=dict(size=40),title_text='CPU Resource (milliCPU)')
fig.update_layout(
    autosize=False,
    height=600,
    margin=dict(l=80, r=80, t=100, b=80),
    showlegend = False,
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
    plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot background
)
fig.update_xaxes(
    tickfont=dict(size=40),
    mirror=True,
    showline=True,
    linecolor='black',
    gridcolor='White'
)
fig.update_yaxes(
    tickfont=dict(size=40),
    mirror=True,
    ticklen=5,
    showline=True,
    linecolor='black',
    gridcolor='White'
)

fig.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 5,
        dtick = 5,
        range = [0.1, 15]
    )
)

        
for trace in fig['data']: 
    if (not trace['name'] in []):
        trace['showlegend'] = False
        
fig.show()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Capacity and Demand for Kubernetes

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

data  = pd.read_excel('Kubernetes CPU Capacity.xlsx')
dataK = pd.read_excel('Kubernetes Acculative CPU Demands.xlsx')
# data.head()

replica = 5
Threshold = 50
st = str(Threshold)+"-"+str(replica);
front_end1 = pd.DataFrame([data[st+".1"],data[st+".2"],data[st+".3"],data[st+".4"],data[st+".5"],data[st+".6"],data[st+".7"],data[st+".8"],data[st+".9"],data[st+".10"],data[st+".11"]])
front_end1 = front_end1.T
front_end1.head()


front_endK1 = pd.DataFrame([dataK[st+".1"],dataK[st+".2"],dataK[st+".3"],dataK[st+".4"],dataK[st+".5"],dataK[st+".6"],dataK[st+".7"],dataK[st+".8"],dataK[st+".9"],dataK[st+".10"],dataK[st+".11"]])
front_endK1 = front_endK1.T
# front_endK1.head()

col_pal = px.colors.sequential.Viridis
col_pal_iterator = itertools.cycle(col_pal) 
fig = go.Figure()

for i in range(11):

    new_colour = px.colors.qualitative.Vivid[i]
    fig.add_trace(go.Scatter(x=random_x, y=front_end1.iloc[:,i],line = dict(dash='dash',color = new_colour),name=labels_to_show_in_legend[i]))
    fig.add_trace(go.Scatter(x=random_x, y=front_endK1.iloc[:,i],line = dict(color = new_colour)))
    fig.update_xaxes(titlefont = dict(size=40),title_text="Time (min)")
    fig.update_yaxes(titlefont = dict(size=40),title_text='CPU Resource (milliCPU)')

fig.update_layout(title=" ",title_x=0.5,
    autosize=False,
    height=600,
    margin=dict(l=80, r=80, t=100, b=80),
    showlegend = False,
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
    plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot background
)
fig.update_xaxes(
    tickfont=dict(size=40),
    mirror=True,
    showline=True,
    linecolor='black',
    gridcolor='White',
#     tickvals = [0,5,10,15]
)
fig.update_yaxes(
    tickfont=dict(size=40),
    mirror=True,
    ticklen=5,
    showline=True,
    linecolor='black',
    gridcolor='White'
)

fig.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 5,
        dtick = 5,
        range = [0.1, 15]
    )
)
        
for trace in fig['data']: 
    if (not trace['name'] in labels_to_show_in_legend):
        trace['showlegend'] = False
        
fig.show()