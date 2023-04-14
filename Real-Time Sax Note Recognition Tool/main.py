# This code uses the pyaudio library to open a stream from the microphone and read chunks of audio data. It then converts the data to a numpy array of integers and applies the Fast Fourier Transform (FFT) to obtain the frequency spectrum. The frequency with the highest amplitude is then used to determine the corresponding musical note using the formula note = int(round(12 * np.log2(freq / 440) + 69)), where 440 is the frequency of A4 (the A note above middle C) and 69 is the MIDI note number for A4.
# The code prints the detected note to the terminal.

import tkinter as tk
import notes_recognition

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Value Display App")

        #----------------------------------------------------Create and center the window----------------------------------------------------
        # Calculate the window's width and height
        window_width = 400
        window_height = 300
        
        # Calculate the screen's width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate the x and y coordinates for centering the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.create_widgets()
        #--------------------------------------------------------------------------------------------------------------------------------------

    def create_widgets(self):
        start_recognition = notes_recognition.start_recognition()
        # Create the starting menu with a button
        self.start_menu = tk.Frame(self)
        self.start_menu.pack(pady=50)
        
        self.label = tk.Label(self.start_menu, text="Real-Time Sax \U0001F3B7 Note Recognition Tool", font=("Helvetica", 16))
       
        self.label.pack(pady=70)
        
        self.start_button = tk.Button(self.start_menu, text="Start", font=("Helvetica", 14), command=notes_recognition.start_recognition)
        self.start_button.pack()
        
        # Create a label to display the values
        self.value_label = tk.Label(self, text="", font=("Helvetica", 24))
        self.value_label.pack(pady=50)
        
        # Initialize variables
        self.value = 0
        self.is_displaying = True
    
if __name__ == "__main__":
    app = App()
    app.mainloop()
