import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time

# Mock audio implementation for testing
class MockAudio:
    """Mock audio class to replace simpleaudio when not available"""
    
    def __init__(self):
        self.is_available = False
        
    def tone(self, duration, frequency=650, sampling_rate=44100):
        """Mock tone generation"""
        return MockWaveObject(duration, frequency)
        
class MockWaveObject:
    """Mock wave object for testing"""
    
    def __init__(self, duration, frequency):
        self.duration = duration
        self.frequency = frequency
        
    def play(self):
        """Mock play method - just wait for the duration"""
        time.sleep(self.duration)
        return self

# Morse code dictionary
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..',
    "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
    '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.',
    '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.',
    ' ': ' '  # Space between words
}

class CWTrainerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CW Trainer - Morse Code Practice")
        self.root.geometry("600x500")
        
        # Initialize audio system
        self.audio = self.initialize_audio()
        
        # Control variables
        self.volume = tk.DoubleVar(value=0.7)
        self.tone_freq = tk.DoubleVar(value=600)
        self.wpm = tk.DoubleVar(value=20)
        
        # Transmission state
        self.is_transmitting = False
        
        self.create_widgets()
        
    def initialize_audio(self):
        """Initialize audio system, fall back to mock if dependencies not available"""
        try:
            import numpy as np
            import simpleaudio as sa
            return self.create_real_audio_system(np, sa)
        except ImportError:
            print("Audio dependencies not available, using mock audio system")
            return MockAudio()
    
    def create_real_audio_system(self, np, sa):
        """Create real audio system when dependencies are available"""
        class RealAudio:
            def __init__(self):
                self.np = np
                self.sa = sa
                self.is_available = True
                
            def tone(self, duration, frequency=650, sampling_rate=44100):
                """Generate actual audio tone"""
                samples = self.np.sin(2*self.np.pi*self.np.arange(sampling_rate*duration)*frequency/sampling_rate)
                samples *= 32767 / self.np.max(self.np.abs(samples))  # Normalize to 16 bit range
                samples = samples.astype(self.np.int16)
                wave = self.sa.WaveObject(samples, 1, 2, sampling_rate)
                return wave
                
        return RealAudio()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="CW Trainer", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Input text area
        ttk.Label(main_frame, text="Message to transmit:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.text_input = scrolledtext.ScrolledText(main_frame, height=4, width=50)
        self.text_input.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_text)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.submit_button = ttk.Button(button_frame, text="Submit", command=self.transmit_message)
        self.submit_button.pack(side=tk.LEFT)
        
        # Controls frame
        controls_frame = ttk.LabelFrame(main_frame, text="Transmission Controls", padding="10")
        controls_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        controls_frame.columnconfigure(1, weight=1)
        
        # Volume control
        ttk.Label(controls_frame, text="Volume:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        volume_scale = ttk.Scale(controls_frame, from_=0, to=1, variable=self.volume, orient=tk.HORIZONTAL)
        volume_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.volume_label = ttk.Label(controls_frame, text="70%")
        self.volume_label.grid(row=0, column=2)
        volume_scale.configure(command=self.update_volume_label)
        
        # Tone frequency control
        ttk.Label(controls_frame, text="Tone (Hz):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        tone_scale = ttk.Scale(controls_frame, from_=400, to=900, variable=self.tone_freq, orient=tk.HORIZONTAL)
        tone_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        self.tone_label = ttk.Label(controls_frame, text="600 Hz")
        self.tone_label.grid(row=1, column=2, pady=(10, 0))
        tone_scale.configure(command=self.update_tone_label)
        
        # WPM control
        ttk.Label(controls_frame, text="WPM:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        wpm_scale = ttk.Scale(controls_frame, from_=5, to=40, variable=self.wpm, orient=tk.HORIZONTAL)
        wpm_scale.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        self.wpm_label = ttk.Label(controls_frame, text="20 WPM")
        self.wpm_label.grid(row=2, column=2, pady=(10, 0))
        wpm_scale.configure(command=self.update_wpm_label)
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(side=tk.RIGHT, padx=(10, 0))
        
    def update_volume_label(self, value):
        """Update volume label"""
        self.volume_label.config(text=f"{int(float(value) * 100)}%")
        
    def update_tone_label(self, value):
        """Update tone frequency label"""
        self.tone_label.config(text=f"{int(float(value))} Hz")
        
    def update_wpm_label(self, value):
        """Update WPM label"""
        self.wpm_label.config(text=f"{int(float(value))} WPM")
        
    def clear_text(self):
        """Clear the input text area"""
        self.text_input.delete(1.0, tk.END)
        
    def text_to_morse(self, text):
        """Convert text to morse code"""
        morse_message = []
        for char in text.upper():
            if char in MORSE_CODE:
                morse_message.append(MORSE_CODE[char])
            elif char == ' ':
                morse_message.append(' ')  # Word space
            # Ignore characters not in morse code dictionary
        return ' '.join(morse_message)
        
    def calculate_timing(self):
        """Calculate timing based on WPM"""
        # Standard: PARIS = 50 units, so 1 WPM = 50 units per minute
        # 1 unit = 60 / (WPM * 50) seconds
        wpm_value = self.wpm.get()
        unit_time = 60 / (wpm_value * 50)
        return unit_time
        
    def transmit_message(self):
        """Transmit the message in morse code"""
        if self.is_transmitting:
            messagebox.showwarning("Warning", "Transmission already in progress")
            return
            
        message = self.text_input.get(1.0, tk.END).strip()
        if not message:
            messagebox.showwarning("Warning", "Please enter a message to transmit")
            return
            
        # Disable submit button and start progress indicator
        self.submit_button.config(state='disabled')
        self.progress.start()
        self.is_transmitting = True
        
        # Convert to morse code
        morse_code = self.text_to_morse(message)
        self.status_label.config(text=f"Transmitting: {morse_code}")
        
        # Start transmission in separate thread
        thread = threading.Thread(target=self.transmit_morse_code, args=(morse_code,))
        thread.daemon = True
        thread.start()
        
    def transmit_morse_code(self, morse_code):
        """Transmit morse code in a separate thread"""
        try:
            unit_time = self.calculate_timing()
            frequency = self.tone_freq.get()
            volume = self.volume.get()
            
            for symbol in morse_code:
                if not self.is_transmitting:  # Allow for interruption
                    break
                    
                if symbol == '.':
                    # Dot: 1 unit
                    tone_obj = self.audio.tone(unit_time, frequency)
                    if hasattr(tone_obj, 'play'):
                        play_obj = tone_obj.play()
                        if hasattr(play_obj, 'wait_done'):
                            play_obj.wait_done()
                    time.sleep(unit_time)  # Space between elements
                    
                elif symbol == '-':
                    # Dash: 3 units
                    tone_obj = self.audio.tone(3 * unit_time, frequency)
                    if hasattr(tone_obj, 'play'):
                        play_obj = tone_obj.play()
                        if hasattr(play_obj, 'wait_done'):
                            play_obj.wait_done()
                    time.sleep(unit_time)  # Space between elements
                    
                elif symbol == ' ':
                    # Space between words: 7 units (we already have 1 unit from previous character)
                    time.sleep(6 * unit_time)
                    
                else:
                    # Space between characters: 3 units (we already have 1 unit from previous element)
                    time.sleep(2 * unit_time)
                    
        except Exception as e:
            print(f"Error during transmission: {e}")
        finally:
            # Re-enable controls
            self.root.after(0, self.transmission_complete)
            
    def transmission_complete(self):
        """Called when transmission is complete"""
        self.submit_button.config(state='normal')
        self.progress.stop()
        self.is_transmitting = False
        self.status_label.config(text="Transmission complete")
        
        # Clear status after 3 seconds
        self.root.after(3000, lambda: self.status_label.config(text="Ready"))

def main():
    root = tk.Tk()
    app = CWTrainerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()