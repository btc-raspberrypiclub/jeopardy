#!/usr/bin/env python

"""
This is a simple script to calculate the maximum possible time that
a github.com/btc-raspberrypiclub/jeopardy game should take, using the
given variables.
"""


def input_default(prompt: str, default: int) -> int:
    """
    Get input from the user, appending
    f" ({default}): " to the given prompt.

    Cleanly exit script if Ctrl-C is pressed
    """
    try:
        res = input(prompt + f" ({default}): ")

        if res == "":
            return default

        try:
            int_res = int(res)
        except ValueError:
            print(f"Invalid int, using default: {default}")
            return default

        return int_res
    except KeyboardInterrupt:
        print("\nCtrl-C: Exiting")
        exit(0)


print()

player_count =   input_default("Player Count  ", 4)  # The total number of players
answer_time =    input_default("Answer Time   ", 7)  # (seconds) Maximum time the players have to answer (after pressing the buzzer)
clue_count =     input_default("Clue Count   ", 25)  # The total number of clues
clue_timeout =   input_default("Clue Timeout ", 20)  # (seconds) The amount of time it takes for a clue to be skipped automatically. This resets after every buzz-in
animation_time = input_default("Animation Time", 5)  # (seconds) The ammount of time it takes for each clue to be loaded

clue_time = player_count * (answer_time + clue_timeout) + animation_time
total_time = clue_time * clue_count  # (seconds)

total_time_minutes = total_time / 60  # (minutes)

print("\n===================\n")

print(f"Seconds: {total_time}")
print(f"Minutes: {total_time_minutes:.2f}")
