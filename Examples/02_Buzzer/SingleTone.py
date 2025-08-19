#!/usr/bin/env/python
# File name   : SingleTone.py
# Website     : www.Adeept.com
# Author      : Adeept
# Date        : 2025/03/5
from gpiozero import TonalBuzzer
from time import sleep

# Initialize a TonalBuzzer connected to GPIO18 (BCM)
tb = TonalBuzzer(18)

# Define a single note
SINGLE_NOTE = [["C4", 0.5]]

# Define 7 musical notes
SEVEN_NOTES = [
    ["C4", 0.5], ["D4", 0.5], ["E4", 0.5], ["F4", 0.5],
    ["G4", 0.5], ["A4", 0.5], ["B4", 0.5]
]

# Define the "Happy Birthday" song
HAPPY_BIRTHDAY_SONG = [
    ["G4", 0.3], ["G4", 0.3], ["A4", 0.3], ["G4", 0.3], ["C5", 0.3], ["B4", 0.6],
    ["G4", 0.3], ["G4", 0.3], ["A4", 0.3], ["G4", 0.3], ["D5", 0.3], ["C5", 0.6],
    ["G4", 0.3], ["G4", 0.3], ["C5", 0.3], ["B4", 0.3], ["C5", 0.3], ["B4", 0.3], ["A4", 0.6],
    ["F5", 0.3], ["F5", 0.3], ["B4", 0.3], ["C5", 0.3], ["D5", 0.3], ["C5", 0.6]
]

def play(tune):
    """
    Play a musical tune using the buzzer.
    :param tune: List of tuples (note, duration), 
    where each tuple represents a note and its duration.
    """
    for note, duration in tune:
        print(note)  # Output the current note being played
        tb.play(note)  # Play the note on the buzzer
        sleep(float(duration))  # Delay for the duration of the note
    tb.stop()  # Stop playing after the tune is complete

if __name__ == "__main__":
    try:
        # First demo: Play a single note
        print("Demo: Playing a single note")
        play(SINGLE_NOTE)

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt for graceful termination
        tb.stop()
        print("Program terminated by user.")
