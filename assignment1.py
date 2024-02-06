import PySimpleGUI as sg 
import numpy as np
import matplotlib.pyplot as plt
import wave
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

layout = [
    [sg.Text("Welcome to the .wav and .tiif reader: \n")],
    [sg.Text("Input File:"), sg.Input(key="-IN-"), sg.FileBrowse(file_types=(("Wav Files", "*.wav*"),))],
    [sg.Exit(), sg.Button("Go")]
]

def read_wav(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        print("File Data:")
        print("Num Channels: " + str(wav_file.getnchannels()))
        print("Sample Width: " + str(wav_file.getsampwidth()))
        print("Frame Rate: " + str(wav_file.getframerate()))
        print("Number of Frames: " + str(wav_file.getnframes()))
        audio_data = wav_file.readframes(wav_file.getnframes())
        audio_data = np.frombuffer(audio_data, dtype=np.int16)
        
        channel1 = audio_data[::wav_file.getnchannels()]
        channel2 = audio_data[1::wav_file.getnchannels()] 
        
        print("Channel 1: ", channel1)
        print("Channel 2: ", channel2)
        for i in range(len(channel1)-1):
            plt.plot([i, i+1], [channel1[i], channel1[i+1]], linestyle='-',  color='b')
            plt.plot([i, i+1], [channel2[i], channel2[i+1]], linestyle='-',  color='r')
        plt.xlabel('Sample No.')
        plt.ylabel('Amplitude')
        
        layout1 = [
            [sg.Text(".wav Plot")],
            [sg.Text("Sample No.:" + str(wav_file.getnframes()))],
             [sg.Text("Sample Freq.:" + str(wav_file.getframerate()))],
            [sg.Canvas(key="-CANVAS1-", background_color='white')]
        ]
        
        window1 = sg.Window(".wav Display + Graph,", layout1, finalize=True, size=(1000, 800))
        draw_figure(window1['-CANVAS1-'], plt.gcf())
        while True:
            event, values = window1.read()
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break

        window.close()
        
        
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas.Widget)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def read_tif(file_path):
    im = Image.open(file_path)
    layout2 = [
        [sg.Text(".tiff ")],
        [sg.Text("Current File Path: " + file_path)],
        [sg.Text("Select new file:"), sg.Input(key="-INIMG-"), sg.FileBrowse(), sg.Button("Go")],
        [sg.Image(key='IMAGE')], 
        [sg.Button("Exit")]
    ]

    window2 = sg.Window(".tif Image displayer", layout2, finalize=True)
    image = ImageTk.PhotoImage(image=im)
    window2['IMAGE'].update(data=image)
    window2.finalize()
    while True:
        event, values = window2.read()

        if event in (sg.WINDOW_CLOSED, "Exit"):
            break

        if event == "Go":
            input_file_path = values["-INIMG-"]
            im = Image.open(input_file_path) 
            image = ImageTk.PhotoImage(image=im)
            window2['IMAGE'].update(data=image)

    window2.close()



window = sg.Window("Assignment1 .wav Converter", layout)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    if event == "Go":
        input_file_path = values["-IN-"]
        if input_file_path.lower().endswith('.wav'):
            read_wav(input_file_path)
        elif input_file_path.lower().endswith('.tif'):
            read_tif(input_file_path)
        else:
            sg.popup_error("File type is not .wav or .tif. Please retry.")
window.close()


