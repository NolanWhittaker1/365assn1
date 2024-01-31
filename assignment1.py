import PySimpleGUI as sg #
import numpy as np
import matplotlib.pyplot as plt
import wave
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# GUI Definition
layout = [
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
    
    if wav_file.getsampwidth() == 1:
        audio_data = np.frombuffer(audio_data, dtype=np.int8)
    else:
        audio_data = np.frombuffer(audio_data, dtype=np.int16)
    
    time = np.arange(0,wav_file.getnframes())/wav_file.getframerate()
    
    if wav_file.getnchannels() == 2:
        channel1 = audio_data[::wav_file.getnchannels()]
        channel2 = audio_data[1::wav_file.getnchannels()]
        plt.subplot(2,1,1)
        plt.plot(time, channel1)
        plt.title('Channel 1')
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        
        plt.subplot(2, 1, 2)
        plt.plot(time, channel2)
        plt.title('Channel 2')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
    else:
        print("Meow")
    
    # Create the PySimpleGUI plot window
    layout = [[sg.Text('Plot test')], [sg.Canvas(key='-CANVAS-')], [sg.Button('Ok')]]
    window = sg.Window('Audio Plot', layout, finalize=True, size=(800, 600))
    canvas_elem = window['-CANVAS-']
    canvas = canvas_elem.Widget

     # Create Matplotlib figure and draw it on the canvas
    fig, ax = plt.subplots(figsize=(3, 2), dpi=100)
    ax.plot(time, channel1)  # You can choose to plot channel1 or channel2 here
    draw_figure(canvas, fig)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Ok'):
            break
    
    window.close()
    return file_path

def draw_figure(canvas, figure):
    tkcanvas = FigureCanvasTkAgg(figure, canvas)
    tkcanvas.draw()
    tkcanvas.get_tk_widget().pack(side='top', fill='both', expand=1)

def read_tiff(file_path):
    return "block"


window = sg.Window("Assignment1 .wav Converter", layout)

while True:
    event, values = window.read()
    #print(event, values)
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    if event == "Go":
        input_file_path = values["-IN-"]
        if input_file_path.lower().endswith('.wav'):
            read_wav(input_file_path)
        elif input_file_path.lower().endswith('.tiif'):
            read_tiif(input_file_path)
        else:
            sg.popup_error("File type is not .wav. Please retry.")
window.close()


