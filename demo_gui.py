#!/usr/bin/env python3
"""
Demo script showing CW Trainer GUI functionality
"""
import sys
import os
import time
import tkinter as tk
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cw_trainer_gui import CWTrainerGUI

def demo_gui():
    """Demo the GUI with sample interactions"""
    root = tk.Tk()
    app = CWTrainerGUI(root)
    
    print("CW Trainer GUI Demo")
    print("==================")
    
    # Demo morse code conversion
    test_messages = ["SOS", "HELLO WORLD", "CQ CQ CQ DE W1ABC K"]
    
    for i, message in enumerate(test_messages):
        print(f"\nDemo {i+1}: Converting '{message}'")
        morse = app.text_to_morse(message)
        print(f"Morse code: {morse}")
        
        # Set the text in the GUI
        app.text_input.delete(1.0, tk.END)
        app.text_input.insert(1.0, message)
        
        # Update controls for demo
        app.wpm.set(15 + i * 5)  # 15, 20, 25 WPM
        app.tone_freq.set(500 + i * 100)  # 500, 600, 700 Hz
        app.volume.set(0.5 + i * 0.2)  # 50%, 70%, 90%
        
        root.update()
        time.sleep(1)
    
    print("\nDemo completed! GUI is ready for use.")
    print("Controls demonstrated:")
    print("- Text input with sample messages")
    print("- WPM adjustment (15-25)")  
    print("- Tone frequency adjustment (500-700 Hz)")
    print("- Volume adjustment (50-90%)")
    
    # Keep window open for viewing
    root.after(5000, root.quit)
    root.mainloop()

if __name__ == '__main__':
    demo_gui()