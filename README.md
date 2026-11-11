# SpeedReader

A simple Python speed-reading application that is easy on the eyes, built with Tkinter. SpeedReader displays text one word at a time and waits for punctuation.

## Features

- PDF and TXT support
- Adjustable reading speed
- Punctuation-aware pacing
- Pause and resume
- Clear and restart

### Reading speed

The delay is specified in milliseconds.

For example, a delay of `250` results in:

- 250 ms between ordinary words.
- 500 ms after the specified punctuation marks.
- 750 ms after full stops.

Lower values produce faster reading speeds.

## Requirements

- Python 3
- Tkinter
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF text extraction

## Install and Run

Clone the repository:

```bash
git clone https://github.com/sinan-steinhardt/speedreader.git
cd speedreader
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install PyMuPDF:

```bash
python -m pip install PyMuPDF
```

Run the application:

```bash
python speedreader.py
```

## Project Structure

```text
speedreader/
├── speedreader.py
├── .gitignore
└── .venv/   
```

## Technologies

- **Python** – Application logic
- **Tkinter** – Graphical user interface
- **PyMuPDF** – PDF text extraction

## License

MIT License
