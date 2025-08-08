#!/usr/bin/env python3
"""
Script to take a screenshot of the CW Trainer GUI
"""
import sys
import os
import time
import tkinter as tk
from tkinter import ttk
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cw_trainer_gui import CWTrainerGUI

def take_screenshot():
    """Create GUI and take a screenshot"""
    root = tk.Tk()
    app = CWTrainerGUI(root)
    
    # Add some sample text to show the interface in use
    app.text_input.insert(1.0, "HELLO WORLD CQ CQ CQ")
    
    # Position the window
    root.geometry("600x500+100+100")
    root.update()
    
    # Give it a moment to render
    time.sleep(2)
    
    # Take screenshot using import command
    os.system('DISPLAY=:99 import -window root /tmp/cw_trainer_gui_screenshot.png')
    
    print("Screenshot saved as /tmp/cw_trainer_gui_screenshot.png")
    
    # Keep the window open for a few seconds
    root.after(3000, root.quit)
    root.mainloop()

if __name__ == '__main__':
    take_screenshot()