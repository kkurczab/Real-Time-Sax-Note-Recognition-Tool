import pyaudio
import numpy as np
import notes, other_functions

def start_recognition():
    frequencies = [note[1] for note in notes.notes]

    CHUNK = 2048 #the smaller, the more frequent displays/outputs
    FORMAT = pyaudio.paInt16 #format of the audio samples
    CHANNELS = 1
    RATE = 48000

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, #format of the audio samples
                    channels=CHANNELS, #number of audio channels
                    rate=RATE, #sample rate of the audio in Hz
                    input=True, #for audio input
                    frames_per_buffer=CHUNK #number of audio frames per buffer
                    )
    #print: <pyaudio.PyAudio.Stream object at 0x00000131CEFB5F90>


    while True:
        data = stream.read(CHUNK) #reads audio data from the stream
    #print: b'\x00\x00\x00\x00...'
        data_int = np.frombuffer(data, dtype=np.int16) #converts the binary audio data in data into an array of signed 16-bit integers
    #print: [0 0 0 ... 0 0 0]...
        fft_data = np.fft.rfft(data_int)
    #print:   2.48699788e+04-1.07654254e+03j  1.97056338e+04-2.52214304e+03j
        freqs = np.fft.rfftfreq(len(data_int), d=1./RATE)
    #print: 43927.734375  44013.8671875 44100. ...
        idx = np.argmax(np.abs(fft_data))
    #print: 0 0 0 0 ...
        freq = freqs[idx]
    #print: Note: 129.19921875 Note: 172.265625 Note: 172.265625


    #This is used to convert the frequency to a MIDI note number, where A4 (440 Hz) is MIDI note number 69. The formula calculates the number of semitones above or below A4 based on the frequency ratio (freq / 440), and then adds 69 to obtain the corresponding MIDI note number.
    #In my case, I had to add 78 (instead of 69), to match the recorded sound with the correct MIDI number.
        note = int(round(12 * np.log2(freq / 440) + 90))

        
    #print: Note: 53
        # print("Note:", freq)
        closest_freq = other_functions.find_closest_key(freq, frequencies)
        closest_note = other_functions.find_key_by_value(notes.notes, closest_freq)
        print(closest_freq, closest_note)
