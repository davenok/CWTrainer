# CWTrainer - Morse Code Learning Application

CWTrainer is a Python-based Morse code (CW) training application that generates audio tones for dots and dashes using precise mathematical timing. The application supports both standard and Farnsworth timing methods for learning Morse code.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Environment Setup (REQUIRED - NEVER SKIP)
Follow these commands in exact order:

```bash
# System dependencies (REQUIRED for audio support)
sudo apt-get update                                    # ~9 seconds
sudo apt-get install -y python3-dev libasound2-dev    # ~3 seconds  
sudo apt-get install -y python3-numpy python3-pyaudio # ~13 seconds

# Verify installations
python3 --version    # Should show Python 3.12+
python3 -c "import numpy, pyaudio; print('Dependencies ready')"
```

### Audio Dependencies: Critical Notes
- **simpleaudio installation FAILS** due to network connectivity issues: `pip install simpleaudio` times out consistently
- **PyAudio works as replacement**: Available via `python3-pyaudio` system package
- **Audio hardware limitation**: Application requires audio device - headless servers will fail with `OSError: Invalid output device`
- **NEVER CANCEL**: Dependency installation takes 15-25 seconds total. Set timeout to 60+ seconds.

### Running the Application

#### Current State - Learning Exercise
The repository contains an **incomplete implementation** designed as a learning exercise:
- `morse_code.py` has placeholder comments: "Write Your Morse Code Function Here" and "Your Code Goes Here" 
- Students must implement the `morse_code()` function and complete the `transmit()` function
- The tone generation framework is provided but conversion logic is missing

#### Testing Without Audio (Recommended for Development)
Create a test version for environments without audio hardware:

```bash
# Test morse code logic without audio requirements
python3 -c "
MORSE_CODE_DICT = {'S': '...', 'O': '---', 'A': '.-', 'E': '.', 'T': '-'}
def morse_code(letter): return MORSE_CODE_DICT.get(letter.upper(), '')
print('Testing:', morse_code('S'), morse_code('O'), morse_code('S'))
"
```

#### Running Complete Application (Requires Audio Hardware)
```bash
# Only works with audio device available
echo 'SOS' | python3 morse_code.py
```
**Expected behavior**: Plays audio tones for dots (0.06s) and dashes (0.18s) with proper spacing

## Build and Test Process

### No Build Required
- Pure Python application - no compilation needed
- Dependencies install in ~25 seconds total
- **NEVER CANCEL**: Always wait for apt-get and pip commands to complete

### Testing Strategy
```bash
# Test imports (5 seconds)
time python3 -c "import time, numpy; print('Core dependencies OK')"

# Test audio availability (will fail in headless environment)  
python3 -c "import pyaudio; p=pyaudio.PyAudio(); print('Audio devices:', p.get_device_count()); p.terminate()"

# Test application structure
python3 -c "exec(open('morse_code.py').read().split('if __name__')[0]); print('Script structure OK')"
```

### Validation Scenarios (MANDATORY)
After making any changes, ALWAYS run these validation steps:

1. **Import Test**: Verify all required modules load correctly
2. **Audio Test**: Check audio system availability (expect failure in CI/headless)
3. **Logic Test**: Validate morse code conversion logic with known patterns
4. **Timing Test**: Confirm dot/dash duration ratios (1:3) and spacing (1:3:7 units)
5. **Message Test**: Process complete messages including multi-word inputs

**NEVER CANCEL**: Testing takes 10-30 seconds. Always wait for completion.

## Key Technical Details

### Morse Code Timing Specification
- **Time unit**: 0.06 seconds (base duration)
- **Dot (dit)**: 1 time unit (0.06s)
- **Dash (dah)**: 3 time units (0.18s) 
- **Inter-element gap**: 1 time unit (0.06s)
- **Inter-letter gap**: 3 time units (0.18s)
- **Inter-word gap**: 7 time units (0.42s)

### Audio Implementation
- **Frequency**: 650 Hz sine wave
- **Sample rate**: 44,100 Hz
- **Bit depth**: 16-bit signed integers
- **Library**: PyAudio (system package) - simpleaudio unavailable

### Known Issues and Workarounds
- **Network connectivity**: `pip install` commands fail with timeouts - use system packages only
- **Audio hardware**: Application fails in headless environments - create silent test versions for development
- **Dependencies**: `python3-dev` and `libasound2-dev` required before installing PyAudio

## Repository Structure
```
/home/runner/work/CWTrainer/CWTrainer/
├── README.md              # Project overview and Morse code theory
├── Morse_code_README.md    # Detailed tutorial and assignment instructions  
├── morse_code.py           # Main application (incomplete - learning exercise)
├── LICENSE                 # GPL v3 license
└── .gitignore             # Standard Python gitignore
```

## Common Commands Reference
```bash
# Complete setup from fresh environment
sudo apt-get update && sudo apt-get install -y python3-dev libasound2-dev python3-numpy python3-pyaudio

# Quick dependency check  
python3 -c "import numpy, pyaudio; print('Ready')"

# Test application structure
head -20 morse_code.py | grep -E "(import|def|#)"

# Run with input
echo "HELLO WORLD" | python3 morse_code.py   # Requires audio hardware
```

### File Operations Timing
- **Repository clone**: ~2 seconds
- **Read documentation files**: ~1 second each
- **Dependency installation**: 15-25 seconds total
- **Application execution**: Immediate (plus audio playback time)

## Development Notes
- Application designed as educational tool - implementation is intentionally incomplete
- Focus on audio timing precision for proper Morse code training
- Supports both individual character practice and full message transmission
- Mathematical timing ensures compatibility with standard Morse code receivers

Always test audio functionality in environments with sound hardware before deployment. For CI/automated testing, create audio-free validation versions.