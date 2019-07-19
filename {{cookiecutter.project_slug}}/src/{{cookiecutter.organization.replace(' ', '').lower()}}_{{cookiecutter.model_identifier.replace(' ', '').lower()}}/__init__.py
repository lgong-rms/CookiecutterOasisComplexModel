import os

__version__ = "{{cookiecutter.model_version.replace(' ', '').lower()}}"

trasformations_files_path = os.path.join(os.path.dirname(__file__), "Files")

from .lookup import *