#!/usr/bin/env python
import os
import sys
import json
####################################################
#           Code by ZeroKun265, 2022               #
#  You may use this code/script however you like   #
# however crediting would be pretty nice. Code for #
#    the getch function and related classes was    #
#   taken by a stackoverflow answer witch itself   # 
#               mentioned this link:               # 
#   https://code.activestate.com/recipes/134892/   #
###################################################

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

help_menu = """
Program that reads a json lang file and asks you for a translation in another language and automatically saves it to a file
Usage:
json_langfile_translation_aid.py <Original> <New file name>

example:
To translate en_us.json to it_it.json
json_langfile_translation_aid.py en_us.json it_it.json
"""

def main():
    override = False

    args = sys.argv[1:]
    if len(args) == 0:
        print(help_menu)
        return
    elif len(args) == 1:
        print("Only one argument provided, please run the command with no arguments to see help")
        return
    elif len(args) >= 3:
        print("Too many arguments provided, please run the command with no arguments to see help")
        return

    # Actual logic
    original_file = args[0]
    new_file = args[1]
    if os.path.isfile(original_file):
        print("Found original file")
    else:
        print(f"Original file '{original_file}' not found")
        return
    if os.path.isfile(new_file):
        while True:
            print("Found existing new file, try and read and get the progress back[r], overwrite[o]? Type the letter corresponding to the chosen option or press anything else to stop")
            x = getch()
            if x == "o":
                with open(new_file, "w") as f:
                    f.write("{}")
                break
            elif x == "r":
                break
            else:
                return
    else:
        with open(new_file, "x"):
            print(f"Creatine file '{new_file}'")



    f_original = open(original_file, "r")
    f_new = open(new_file, "r")
    json_new = ""
    json_original = ""
    try:
        json_original = json.load(f_original)
        f_original.close()
    except json.decoder.JSONDecodeError:
        print(f"Error in reading '{original_file}': might not be a valid json")
        return
    try:
        json_new = json.load(f_new)
        f_new.close()
    except json.decoder.JSONDecodeErrror:
        print(f"Error in reading '{new_file}': might not be a valid json or got corrupted, you can override it if you run the program again or remove the file entirely")
        return
    
    try:
        
        for key, value in json_original.items():
            if key in json_new:
                print(f"Key '{key}' found in new file")
                if json_new[key]:
                    print(f"Key '{key}' in new file has a value")
                    continue
            else:
                print(f"Found key '{key}' with value '{value}'. Type the new value for this key:\n")
                transl = input()
                json_new[key] = transl

        print(f"No more key value pairs in '{original_file}': Dumping and saving '{new_file}'")
        with open(new_file, "w") as f:
            json.dump(json_new, f, indent=1)
    except KeyboardInterrupt:
        print("keyboardInterrupt detected, saving progress")
        with open(new_file, "w") as f:
            json.dump(json_new, f , indent=2)
            f.write("\n")
        return




if __name__ == "__main__":
    main()
