# Typing Speed Test

A modern, desktop-based Typing Speed Test application built in Python using standard Tkinter GUI. Features real-time WPM/accuracy feedback, multiple passage difficulties, customizable timed sessions, visual keypress tracking, and historical performance statistics.

## Features
- **Real-Time Speed & Accuracy**: Instant tracking of Gross WPM, Net WPM, Accuracy (%), and CPM (Characters Per Minute).
- **Visual Text Feedback**: Live color-coded character highlighting (correct, incorrect, current cursor position).
- **Difficulty & Duration Selection**: Test yourself across Easy, Medium, and Hard texts for 15s, 30s, or 60s.
- **Performance History**: Local JSON storage recording past sessions with a visual tabular summary.
- **Clean Modern UI**: Dark-themed responsive interface inspired by modern typing tools.

## Project Structure
```
. 
├── data/
│   └── passages.json       # Categorized passages database
├── src/
│   ├── __init__.py
│   ├── engine.py           # Core logic for typing metrics and test state
│   └── ui.py               # Tkinter GUI implementation
├── tests/
│   └── test_main.py        # Pytest unit test suite
├── .gitignore
├── main.py                 # Application entry point
└── requirements.txt
```

## Setup and Running

### Prerequisites
- Python 3.8+
- `tkinter` (included by default in standard Python installations on Windows and macOS; on Linux install via `sudo apt install python3-tk`).

### Installation
1. Clone or extract the repository.
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install test dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Launching the Application
Run `main.py` to start the GUI:
```bash
   python main.py
   ```

### Running Unit Tests
Run test suite using `pytest`:
```bash
   pytest tests/
   ```
