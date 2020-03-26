from enum import IntEnum
import os


class FileManagerWriteMode(IntEnum):
    INLINE = 0
    OUTLINE = 1


class FileManagerException(BaseException):
    def __init__(self, message):
        super().__init__(message)


class FileManager:
    def __init__(self, file_path="", mode=FileManagerWriteMode.INLINE):
        """
        Initializes attributes and gives a default file_path if it is an empty value.
        :param file_path:
        :param mode:
        """
        if file_path == "":
            self._file_path = os.path.join(os.getcwd(), "john_the_text")
        else:
            self._file_path = file_path

        self._mode = mode

    def _is_file_exists(self):
        """
        Simply checks if the file path exists and if it is a file.
        :return:
        """
        return os.path.exists(self._file_path) and os.path.isfile(self._file_path)

    def _write_as_inline(self, key):
        """
        Gets the last text line of the file, appends the key at the end and writes it.
        :param key:
        :return:
        """
        with open(self._file_path, "a+") as f:
            lines = f.readlines()

            if len(lines) == 0:
                f.write(key)
            else:
                lines[-1] = "{0}{1}".format(lines[-1], key)
                f.writelines(lines)

    def _write_as_outline(self, key):
        """
        Adds a new line to the file with the given key.
        :param key:
        :return:
        """
        with open(self._file_path, "a") as f:
            f.write(key)

    def write(self, key, mode=None):
        """
        Public method that switch between mode to use for writing.
        :param key:
        :param mode:
        :return:
        """
        if not self._is_file_exists():
            self._write_as_outline(key)

        if mode is None:
            mode = self._mode

        if mode == FileManagerWriteMode.INLINE:
            self._write_as_inline(key)

        if mode == FileManagerWriteMode.OUTLINE:
            self._write_as_outline(key)
