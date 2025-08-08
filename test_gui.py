#!/usr/bin/env python3
"""
Test script to verify CW Trainer GUI functionality
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cw_trainer_gui import CWTrainerGUI, MORSE_CODE
import tkinter as tk
import time

def test_morse_conversion():
    """Test morse code conversion functionality"""
    print("Testing morse code conversion...")
    
    # Create a minimal GUI instance for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window for testing
    app = CWTrainerGUI(root)
    
    # Test cases
    test_cases = [
        ("HELLO", ".... . .-.. .-.. ---"),
        ("SOS", "... --- ..."),
        ("CQ", "-.-. --.-"),
        ("123", ".---- ..--- ...--"),
        ("HELLO WORLD", ".... . .-.. .-.. ---   .-- --- .-. .-.. -..")
    ]
    
    for text, expected in test_cases:
        result = app.text_to_morse(text)
        print(f"Text: '{text}' -> Morse: '{result}'")
        if result == expected:
            print("✓ PASS")
        else:
            print(f"✗ FAIL - Expected: '{expected}'")
    
    # Test timing calculation
    app.wpm.set(20)
    unit_time = app.calculate_timing()
    expected_unit_time = 60 / (20 * 50)  # Should be 0.06 seconds
    print(f"\nTiming test (20 WPM): {unit_time:.4f}s (expected: {expected_unit_time:.4f}s)")
    if abs(unit_time - expected_unit_time) < 0.001:
        print("✓ PASS")
    else:
        print("✗ FAIL")
    
    root.destroy()
    print("\nMorse code conversion tests completed!")

def test_gui_components():
    """Test GUI component creation"""
    print("Testing GUI component creation...")
    
    root = tk.Tk()
    root.withdraw()  # Hide the window for testing
    
    try:
        app = CWTrainerGUI(root)
        
        # Test that all components are created
        components = [
            'text_input', 'clear_button', 'submit_button',
            'volume', 'tone_freq', 'wpm',
            'volume_label', 'tone_label', 'wpm_label',
            'status_label', 'progress'
        ]
        
        for component in components:
            if hasattr(app, component):
                print(f"✓ {component} created successfully")
            else:
                print(f"✗ {component} missing")
        
        # Test default values
        assert app.volume.get() == 0.7, "Volume default should be 0.7"
        assert app.tone_freq.get() == 600, "Tone frequency default should be 600"
        assert app.wpm.get() == 20, "WPM default should be 20"
        
        print("✓ Default values correct")
        
        root.destroy()
        print("GUI component tests completed!")
        
    except Exception as e:
        print(f"✗ GUI creation failed: {e}")
        root.destroy()

if __name__ == '__main__':
    print("CW Trainer GUI Test Suite")
    print("=" * 30)
    
    test_morse_conversion()
    print()
    test_gui_components()
    
    print("\nAll tests completed!")