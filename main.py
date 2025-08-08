#!/usr/bin/env python3
"""
CW Trainer - Morse Code Practice Tool
Main launcher with both CLI and GUI interfaces
"""
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='CW Trainer - Morse Code Practice Tool')
    parser.add_argument('--gui', action='store_true', help='Launch GUI interface (default)')
    parser.add_argument('--cli', action='store_true', help='Use command line interface')
    parser.add_argument('--message', '-m', type=str, help='Message to transmit (CLI mode only)')
    parser.add_argument('--wpm', type=int, default=20, help='Words per minute (5-40, default: 20)')
    parser.add_argument('--frequency', '-f', type=int, default=650, help='Tone frequency in Hz (400-900, default: 650)')
    
    args = parser.parse_args()
    
    # Default to GUI if no specific interface is chosen
    if not args.cli:
        launch_gui()
    else:
        launch_cli(args)

def launch_gui():
    """Launch the TKinter GUI interface"""
    try:
        import tkinter as tk
        from cw_trainer_gui import CWTrainerGUI
        
        root = tk.Tk()
        app = CWTrainerGUI(root)
        root.mainloop()
        
    except ImportError as e:
        print(f"GUI dependencies not available: {e}")
        print("Please install tkinter: sudo apt-get install python3-tk")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching GUI: {e}")
        sys.exit(1)

def launch_cli(args):
    """Launch the command line interface"""
    try:
        from morse_code import transmit
        
        if args.message:
            # Validate parameters
            wpm = max(5, min(40, args.wpm))
            frequency = max(400, min(900, args.frequency))
            
            transmit(args.message, wpm, frequency)
        else:
            # Interactive mode
            print("CW Trainer - Command Line Interface")
            print("Enter your message (Ctrl+C to exit):")
            
            try:
                while True:
                    message = input('Message: ')
                    if message.strip():
                        wpm = max(5, min(40, args.wpm))
                        frequency = max(400, min(900, args.frequency))
                        transmit(message, wpm, frequency)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                
    except ImportError as e:
        print(f"CLI dependencies not available: {e}")
        print("Please install required packages: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error in CLI mode: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()