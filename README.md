# Pomodoro Timer

A simple pomodoro timer with adjustable time made in Python.

## Screenshots

![Screenshot 1](https://i.imgur.com/pGWwhgj.png)

## Notes

The time periods go up to 60 minutes. The timer will not go past 60 minutes.

If the 'Notify on Complete' checkbox is checked, the timer will notify you when the time period is complete with audio and with the window popping to view if hidden.

## Requirements

- Python 3.6 or higher
- Tkinter
- ttkthemes

## How to Run

### Run with Python

Run the following command in the repository directory

`python pomodoro.py`

## Compile to Executable

Install pyInstaller with
`pip install pyinstaller`

Run (Replace \<repo-dir> with the repository directory)

`pyinstaller --noconfirm --onefile --windowed --icon "<repo-dir>/resources/icon.ico" --add-data "<repo-dir>/resources;resources/"  "<repo-dir>/pomodoro.py" `

You can also download the executable from the releases page or use auto-py-to-exe to compile the program.
