import time
import numpy as np 
import simpleaudio as sa 

# This function generates the audio tone by creating a 650hz SIN wave
def tone(duration, frequency=650, sampling_rate=44100):
    """
    Generates a simple audio wave object from a specified frequency and duration.
    """
    samples = np.sin(2*np.pi*np.arange(sampling_rate*duration)*frequency/sampling_rate)
    samples *= 32767 / np.max(np.abs(samples))  # Normalize to 16 bit range
    samples = samples.astype(np.int16)
    wave = sa.WaveObject(samples, 1, 2, sampling_rate)
    return wave


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

def text_to_morse(text):
    """Convert text to morse code"""
    morse_message = []
    for char in text.upper():
        if char in MORSE_CODE:
            morse_message.append(MORSE_CODE[char])
        elif char == ' ':
            morse_message.append(' ')  # Word space
        # Ignore characters not in morse code dictionary
    return ' '.join(morse_message)


# <-- Complete The Transmit Function -->
def transmit(message, wpm=20, frequency=650):
    """
    Transmit a message in morse code
    
    Args:
        message (str): Text message to transmit
        wpm (int): Words per minute transmission speed
        frequency (int): Tone frequency in Hz
    """
    # Convert text to morse code
    morse_code = text_to_morse(message)
    
    # Calculate timing based on WPM
    # Standard: PARIS = 50 units, so 1 WPM = 50 units per minute
    # 1 unit = 60 / (WPM * 50) seconds
    unit_time = 60 / (wpm * 50)
    
    # see README.md for use
    dot_tone = tone(unit_time, frequency)  
    dash_tone = tone(3 * unit_time, frequency)

    print(f"Transmitting: {message}")
    print(f"Morse code: {morse_code}")
    print(f"WPM: {wpm}, Frequency: {frequency}Hz")
    
    for symbol in morse_code:
        if symbol == '.':
            # Dot: 1 unit
            play_obj = dot_tone.play()
            play_obj.wait_done()
            time.sleep(unit_time)  # Space between elements
            
        elif symbol == '-':
            # Dash: 3 units
            play_obj = dash_tone.play()
            play_obj.wait_done()
            time.sleep(unit_time)  # Space between elements
            
        elif symbol == ' ':
            # Space between words: 7 units (we already have 1 unit from previous character)
            time.sleep(6 * unit_time)
            
        else:
            # Space between characters: 3 units (we already have 1 unit from previous element)
            time.sleep(2 * unit_time)


# <-- Do Not Modify or Move -->
if __name__ == '__main__':
    message = input('Message: ') 
    transmit(message)
