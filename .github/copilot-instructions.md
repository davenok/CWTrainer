# CWTrainer (Morse Code Trainer)

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the information here.

CWTrainer is an educational Python project for learning and implementing Morse code (CW - Continuous Wave) audio generation. The project consists of a single Python file where students implement morse code translation and audio transmission functions.

## Working Effectively

### Initial Setup
**CRITICAL**: Set timeouts to 300+ seconds for all installation commands. NEVER CANCEL any installation process.

Install system dependencies (takes ~10 seconds on Ubuntu):
```bash
sudo apt-get update
sudo apt-get install -y python3-dev libasound2-dev
```

Install Python dependencies (takes ~15 seconds, may take 5+ minutes on slower networks):
```bash
pip3 install numpy simpleaudio
```

Alternative system package installation for numpy (faster, takes ~10 seconds):
```bash
sudo apt-get install -y python3-numpy
```

**Note**: `simpleaudio` is not available as a system package and must be installed via pip.

### Verify Installation
Test that all dependencies are properly installed:
```bash
python3 -c "import numpy, simpleaudio; print('Dependencies installed successfully')"
```

Test audio functionality (will fail in headless environments - this is expected):
```bash
python3 -c "import simpleaudio.functionchecks as fc; fc.LeftRightCheck.run()"
```
If you see ALSA errors in headless environments, this is normal and expected.

### Running the Application
The main application is in `morse_code.py`:
```bash
python3 morse_code.py
```

**Note**: The original code has skeleton functions that need to be implemented. The `morse_code()` and `transmit()` functions are incomplete in the original file.

## Project Structure

### Repository Files
```
.
├── README.md                  # Main project description
├── Morse_code_README.md       # Detailed tutorial/assignment instructions
├── morse_code.py              # Main Python file (educational skeleton)
├── LICENSE                    # GNU GPL v3 license
└── .gitignore                 # Standard Python gitignore
```

### Key Code Components
- `tone(duration, frequency=650, sampling_rate=44100)`: Generates audio wave objects (already implemented)
- `morse_code(letter)`: Convert letter to morse code pattern (skeleton - needs implementation)
- `transmit(message)`: Play morse code audio for message (skeleton - needs implementation)

## Validation

### Audio Testing Limitations
- Audio playback will NOT work in headless environments (CI/CD, containers, etc.)
- ALSA errors like "cannot find card '0'" are expected and normal in headless environments
- For testing in headless environments, modify the transmit function to print dots/dashes instead of playing audio

### Manual Testing Scenarios
Always test these scenarios after making changes:

1. **Basic Function Test**:
```bash
python3 -c "import morse_code; print('Import successful')"
```

2. **Tone Generation Test**:
```bash
python3 -c "
import morse_code
result = morse_code.tone(0.1)
print('Tone function works, type:', type(result))"
```

3. **Interactive Application Test**:
```bash
echo 'sos' | python3 morse_code.py
```

4. **Extended Message Test**:
```bash
echo 'hello world' | python3 morse_code.py
```

### Implementation Requirements
If implementing the missing functions, follow these morse code timing rules:
- Dot (dit): 1 time unit (0.06 seconds)
- Dash (dah): 3 time units (0.18 seconds) 
- Space between elements within a letter: 1 time unit
- Space between letters: 3 time units
- Space between words: 7 time units

## Dependencies and Timing

### Installation Times (measured on Ubuntu 24.04)
- System dependencies: ~10 seconds
- Python dependencies via pip: 15 seconds to 5+ minutes (network dependent)
- System numpy package: ~10 seconds

### Runtime Performance
- Application startup: < 1 second
- Short message (3 characters): ~1 second
- Long message (11 characters): ~3 seconds

## Common Tasks

### Testing Without Audio
In headless environments, create a test version that prints morse code patterns:
```python
# Replace audio playback with text output for testing
if mark == '.':
    print('dot', end='')
elif mark == '-':
    print('dash', end='')
```

### Verifying Dependencies
```bash
# Check Python version (requires 3.x)
python3 --version

# Verify numpy installation and version
python3 -c "import numpy; print('numpy version:', numpy.__version__)"

# Verify simpleaudio installation
python3 -c "import simpleaudio; print('simpleaudio available')"
```

### Troubleshooting Common Issues
1. **"No module named 'numpy'"**: Install numpy via pip or apt
2. **"No module named 'simpleaudio'"**: Install simpleaudio via pip (requires build tools)
3. **Audio errors in containers**: Expected behavior, test with text output instead
4. **Build failures for simpleaudio**: Ensure python3-dev and libasound2-dev are installed

## Environment Limitations
- **Audio playback**: Only works on systems with audio hardware and drivers
- **Headless systems**: Audio will fail, but morse code logic can still be tested
- **Container environments**: Audio typically unavailable, use text-based testing
- **Network dependencies**: simpleaudio requires internet access for pip installation

## File Locations
- Main code: `/path/to/repo/morse_code.py`
- Documentation: `/path/to/repo/README.md` and `/path/to/repo/Morse_code_README.md`
- Educational materials: See `Morse_code_README.md` for detailed implementation assignment

**CRITICAL REMINDERS**:
- NEVER CANCEL installation commands - they may take 5+ minutes
- Audio testing will fail in headless environments (this is expected)
- Always test with both audio and text-based validation methods
- The original code is a skeleton for educational purposes - functions need implementation