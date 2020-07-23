import PySimpleGUI as sg

# location the weight graph gets saved
graph_loc = './weight_graph.png'

# this whole section builds the skeleton for the GUI layout
graphcol = [
    [sg.Text('Weight Graph', key='graphlabel', auto_size_text=True)],
    [sg.Image(key="-IMAGE-")]
]

buttoncol = [
    [sg.Button('read')],
    [sg.Button('calibrate (20kg)')],
    [sg.Button('weigh')],
    [sg.Button('save and classify')]
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



classifications = [item for pair in classifications for item in pair]
buttoncol.extend([[sg.HorizontalSeparator()], classifications[0:6], classifications[6:]])

# finalize and render the starting layout
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
window = sg.Window("Image Viewer", layout)
window.finalize()
window["-IMAGE-"].update(filename=graph_loc)


while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # just update the image every time
    try:
        window["-IMAGE-"].update(filename=graph_loc)
    except:
        pass

window.close()