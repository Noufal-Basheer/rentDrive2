from setuptools import setup, find_packages
from cx_Freeze import setup, Executable

setup(
    name="RentDrive",
    version="1.0.0",
    packages=find_packages(),
    executables=[Executable("main.py")],
    options={
        "build_exe": {
            "packages": ["logger", "cli_utils"],  # Add your package names here
            "include_files": ["execute.py","__init__.py","cli_utils"],  # Add any additional files here
        }
    }
)
