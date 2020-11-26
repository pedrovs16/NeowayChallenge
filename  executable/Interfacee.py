import PySimpleGUI as sg
import functions as ft



class Interface:
    def __init__(self):

        # Layout

        sg.theme('dark teal 9')
        layout = [
            # Linha 1
            [sg.Text('=' * 120)],
            # Linha 2
            [sg.Text(" " * 40), sg.Text("COMPILADOR DE CEP", )],
            # Linha 3
            [sg.Text("Escolha os estado(s):"), sg.Checkbox('AC', key='AC'), sg.Checkbox('AL', key='AL')
                , sg.Checkbox('AP', key='AP'), sg.Checkbox('AM', key='AM')
                , sg.Checkbox('BA', key='BA'), sg.Checkbox('CE', key='CE')
                , sg.Checkbox('DF', key='DF')],
            # Linha 4
            [sg.Checkbox('ES  ', key='ES'), sg.Checkbox('GO  ', key='GO')
                , sg.Checkbox('MA  ', key='MA'), sg.Checkbox('MG  ', key='MG')
                , sg.Checkbox('MS  ', key='MS'), sg.Checkbox('MT  ', key='MT')
                , sg.Checkbox('PA  ', key='PA'), sg.Checkbox('PB  ', key='PB')],
            # Linha 5
            [sg.Checkbox('PR  ', key='PR'), sg.Checkbox('PE  ', key='PE')
                , sg.Checkbox('PI  ', key='PI'), sg.Checkbox('RJ  ', key='RJ')
                , sg.Checkbox('RN  ', key='RN'), sg.Checkbox('RS  ', key='RS')
                , sg.Checkbox('RO  ', key='RO'), sg.Checkbox('RR  ', key='RR')],
            # Linha 6
            [sg.Checkbox('SC  ', key='SC'), sg.Checkbox('SP  ', key='SP')
                , sg.Checkbox('SE  ', key='SE'), sg.Checkbox('TO  ', key='TO')],
            # Linha 7
            [sg.Text('Nome para o arquivo JSONL:'), sg.Input(key='arquivonome')],
            [sg.Button('Compilar', key='compilar')],
            # Linha 8
            [sg.Output(size=(71, 28))],
        ]

        # JANELA

        window = sg.Window('Neoway', size=(550, 620)).layout(layout)


        # Analisando estados escolhidos

        while True:
            num = 1
            try:
                event, values = window.read()
                if event == sg.WINDOW_CLOSED:  # Se o X da interface for clicado finalizar o programa
                    break
                elif event == 'compilar':
                    for uf in values:
                        if values[uf] is True:
                            num = ft.StateChoice(uf, num, values['arquivonome'])
                print('JSON formado.')

            except Exception as error:
                print(error)



interface = Interface()
