# Countdown Timer

A Python 3.13 CLI countdown that sleeps between updates (no busy-looping), supports Ctrl+C cancellation, and prints an audible terminal bell plus a completion message when time expires. The duration parsing and formatting helpers can be tested independently.

## Run

```powershell
python main.py
python main.py 90
python main.py 02:30
python main.py 01:02:03
```

Accepted forms are whole seconds, `MM:SS`, or `HH:MM:SS`; duration must be greater than zero and at most 99:59:59. Clock-format minute and second fields must be below 60.

## Test

```powershell
python -m unittest -v
```