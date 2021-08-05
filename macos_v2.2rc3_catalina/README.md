# Packaging Instructions

## Information
- Packaging OS: macOS Catalina
- DLC Version: v2.2rc3
- Executable Works on: none
- Executable Errors on: macOS Catalina
   - Reason: tensorpack related errors on launch
- Status: work in progress

## Step by Step Instructions
0. Secure a Mac with macOS Catalina
1. Follow steps from DLC to install the DLC-CPU conda environment, and
   activate it.
2. Install `pyinstaller` using `pip install pyinstaller` (not conda)
3. Run `pyinstaller --windowed DLC.py` (no hidden imports needed)
4. Copy `libpng16.16.dylib` (follow instructions
   [here](https://stackoverflow.com/questions/61824188/issue-converting-python-script-with-pyinstaller-import-error-incompatible-libr)
   to download the library) into `dist/DLC.app/Contents/MacOS/` to resolve
   the library version conflict error
5. Copy the `deeplabcut` folder into `dist/DLC.app/Contents/MacOS/` to fill
   in the missing media
6. Copy the `tensorpack` folder into `dist/DLC.app/Contents/MacOS/` to fill
   in missing files from the library
7. ...

## Detailed Troubleshooting Steps
Steps are pretty similar to those for v2.1.9 packaging on Catalina, with
the exception that there is no need for hidden imports. 