# This code uses the pyaudio library to open a stream from the microphone and read chunks of audio data.
# It then converts the data to a numpy array of integers and applies the Fast Fourier Transform (FFT) to obtain the frequency spectrum.
# The frequency with the highest amplitude is then used to determine the corresponding musical note using the formula note = int(round(12 * np.log2(freq / 440) + 78)), where 440 is the frequency of A4 (the A note above middle C) and 69 is the MIDI note number for A4.
# The code prints the detected note to the terminal.

import pyaudio
import numpy as np
import tkinter as tk

notes = [                           #in Hz, for sax alto [note, freq, recorded_freq_2_channels, recorded_note_1_channel]
    # ['A#3/Bb3', 233.08],
    # ['B3', 246.94, 562],
    ['C4', 261.63, 304, 60],
    ['C#4/Db4', 277.18, 328, 61],
    ['D4', 293.66, 351, 62],
    ['D#4/Eb4', 311.13, 562, 63],
    ['E4', 329.63, 585, 64],
    ['F4', 349.23, 421, 65],
    ['F#4/Gb4', 369.99, 445, 66],
    ['G4', 392.00, 234, 67],
    ['G#4/Ab4', 415.30, 492, 68],
    ['A4', 440.00, 257, 69],
    ['A#4/Bb4', 466.16, 281, 70],
    ['B4', 493.88, 304, 71],
    ['C5', 523.25, 632, 72],
    ['C#5/Db5', 554.37, 328, 73],
    ['D5', 587.33, 351, 74],
    ['D#5/Eb5', 622.25, 375, 75],
    ['E5', 659.25, 398, 76],
    ['F5', 698.46, 421, 77],
    ['F#5/Gb5', 739.99, 445, 78],
    ['G5', 783.99, 492, 79],
    ['G#5/Ab5', 830.61, 515, 80],
    ['A5', 880.00, 539, 81],
    ['A#5/Bb5', 932.33, 562, 82],
    ['B5', 987.77, 609, 83],
    ['C6', 1046.50, 632, 84],
    ['C#6/Db6', 1108.73, 679, 85],
    ['D6', 1174.66, 726, 86],
    ['D#6/Eb6', 1244.51	, 773, 87],
    ['E6', 1318.51, 796, 88],
    ['F6', 1396.91, 843, 89],
    ['F#6/Gb6', 1479.98, 914, 90],
    ['G6', 1567.98, 890, 91]
]

#----------------------------------------------------Functions---------------------------------------------------------------------------------------------------------------------------------------------------
def find_closest_key(value, keys):
    """
    Finds the key from the array that has the closest value to the given value.

    Args:
        value (float or int): The value to be matched.
        keys (list): The array of keys to search.

    Returns:
        Key from the array with the closest value to the given value.
    """
    closest_key = None
    min_difference = float('inf')  # Set initial difference to infinity
    
    for key in keys:
        difference = abs(key - value)
        if difference < min_difference:
            min_difference = difference
            closest_key = key

    return closest_key
#-----------------------------------
def find_key_by_value(notes, value):
    for x in notes:
        if x[3] == value:
            return x[0]
    return None
#------------------------------------------------------------------------
def start_recognition():
    root.start_button.destroy()
    
    frequencies = [note[3] for note in notes]

    CHUNK = 2048 * 16 # the smaller, the more frequent displays/outputs
    FORMAT = pyaudio.paInt16 # format of the audio samples
    CHANNELS = 1 # with 2, there is no way to differentiate G4 from G5
    RATE = 48000

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, # format of the audio samples
                    channels=CHANNELS, # number of audio channels
                    rate=RATE, # sample rate of the audio in Hz
                    input=True, # for audio input
                    frames_per_buffer=CHUNK # number of audio frames per buffer
                    )

    data = stream.read(CHUNK) # reads audio data from the stream
    data_int = np.frombuffer(data, dtype=np.int16) # converts the binary audio data in data into an array of signed 16-bit integers
    fft_np = np.fft.fft(data_int) # calculate fast fourier transform (FFT)

    power_np = np.abs(fft_np) ** 2 # calculate power spectrum
    max_power_idx = np.argmax(power_np) # find index of maximum power
    freq = max_power_idx * RATE / CHUNK # calculate frequency of maximum power

    noise_floor = np.mean(power_np[:int(max_power_idx*0.9)]) # perform spectral subtraction to remove noise
    power_np[power_np < noise_floor] = noise_floor
    power_np -= noise_floor
    
    # invert FFT to get denoised signal
    denoised_fft_np = fft_np * (power_np / (power_np + noise_floor))
    denoised_np = np.fft.ifft(denoised_fft_np).real
    fft_np = np.fft.fft(denoised_np)

    # calculate power spectrum
    power_np = np.abs(fft_np) ** 2
    # find index of maximum power
    max_power_idx = np.argmax(power_np)
    # calculate frequency of maximum power
    freq = max_power_idx * RATE / CHUNK   

    # This is used to convert the frequency to a MIDI note number, where A4 (440 Hz) is MIDI note number 69. The formula calculates the number of semitones above or below A4 based on the frequency ratio (freq / 440), and then adds 69 to obtain the corresponding MIDI note number.
    # In my case, I had to add 78 (instead of 69), to match the recorded sound with the correct MIDI number.
    note = int(round(12 * np.log2(freq / 440) + 78))

    closest_freq = find_closest_key(note, frequencies)
    closest_note = find_key_by_value(notes, closest_freq)

    root.note.config(text=closest_note)

    update(root.note, closest_note) # update the displayed note

def update(label, value):
    label.config(text=value)
    label.after(100, start_recognition)

#-----------------------------------------------------------Create main app----------------------------------------------------------
root = tk.Tk()
frame = tk.Frame(root)
frame.pack()
root.title("Real-Time Sax Note Recognition Tool")
root.iconbitmap("1.ico") # provide path to icon

#----------------------------------------------------Create and center the window----------------------------------------------------
# Calculate the window's width and height
window_width = 400
window_height = 300
# Calculate the screen's width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# Calculate the x and y coordinates for centering the window
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2    
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

#-----------------------------------------------------------Create Widgets-----------------------------------------------------------
# Create the starting menu with a button
root.start_menu = tk.Frame()
root.start_menu.pack(pady=10)
root.label = tk.Label(root.start_menu, text="Real-Time Sax \U0001F3B7 Note Recognition Tool", font=("Helvetica", 16))  
root.label.pack(pady=20)

root.note = tk.Label(root.start_menu, text="[Played note]", font=("Helvetica", 50))
root.note.pack()

root.start_button = tk.Button(root.start_menu, text="Start", font=("Helvetica", 14), command=(start_recognition))
root.start_button.pack(pady=15)


root.mainloop()
