# my_package/__init__.py
print("Initializing my_package...")

VERSION = "1.0.0"
AUTHOR = "zxc4we"

from .file_manager import FileManager

def greet():
    print("Hello from my_package!")