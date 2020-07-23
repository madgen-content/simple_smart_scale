import PySimpleGUI as sg

layout = [[sg.Text(key='ref', text='',size=(20, 1))],
          [sg.Input(key='in', do_not_clear=False)],
          [sg.Button('read'), sg.Exit()]
          ]

window = sg.Window('Alternative items', layout)

while True:
    event, values = window.Read()
    print(event, values)
    if event is None or event == 'Exit':
        break
    if event == 'read':
        new_label = values['in']
        window['ref'].update(new_label)
window.Close()