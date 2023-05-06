<b>Real-Time Sax Note Recognition Tool</b>

For the purpose of a project from my university, I created a tool/app, which recognizes notes played on a saxophone in real-time and displays it on the screen. In order to determine which note is played, FFT (Fast Fourier Trasform) is used.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------

This code uses the pyaudio library to open a stream from the microphone and read chunks of audio data.

- It then converts the data to a numpy array of integers and applies the Fast Fourier Transform (FFT) to obtain the frequency spectrum.
- The frequency with the highest amplitude is then used to determine the corresponding musical note.
- The code prints the detected note to the terminal.
