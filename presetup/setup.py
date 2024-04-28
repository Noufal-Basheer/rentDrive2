from setuptools import setup, find_packages
from cx_Freeze import setup, Executable

setup(
    name="RentDrive presetup",
    version="1.0.0",
    packages=find_packages(),
    executables=[Executable("main.py",target_name="setup")],
    options={
        "build_exe": {
            "packages": ["logger", "utils"],  # Add your package names here
            "include_files": ["execute.py","__init__.py","utils","logger"],  # Add any additional files here
        }
    }
)
