from models.file_manager import FileManager
from models.keyboard_listener import KeyboardListener


file_manager = FileManager()

keyboard_listener = KeyboardListener(file_manager)
keyboard_listener.start()
