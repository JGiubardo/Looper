# Instructions for Windows
 These instructions provide a detailed guide on how to install all pre-requisites and use the program on Windows 10.

## Python
 Hit the windows button and type cmd into `cmd` into the search bar to find command prompt, right click the command 
 prompt result and select `Run as administrator`.
 In the command prompt window type `python` and hit enter.  If a Windows store window appears select install, if `>>>` 
 appears this means python is already installed and you can type `exit()` to leave the shell.  

## Python packages
 On the github page for this program, use the green Code button and select `Download ZIP` to download.  Extract the zip
 to a folder.  Open the folder in Windows File Explorer select the address bar, and copy the text.  If this address does
 not start with `C:\`, in your command prompt type the letter that it starts with followed by a colon, for example `d:`.
 Use Enter and it should change drives
 then type `cd` use a space, and right click the command prompt to paste the address, and hit Enter. Use this command to
 install packages by copy-pasting it into your command prompt:
  
  ```
pip install -r requirements.txt
  ```

## mpg123
 To install the library on Windows use the mpg123 downloads page: https://www.mpg123.de/download.shtml
 
 In the section marked `Win32 and Win64 Binaries` follow the link to compiled binaries marked as **for 64 bit**. 
 Download the version that is in the form of `mpg123-[VERSION]-x86-64.zip`. Extract the zip and select `libmpg123-0.dll`
 copy this file. In Windows File Explorer navigate to `C:\Windwos` and paste this file into the folder.
 
## Using the program 
 Double clicking `main_loop.py` will cause it to run on every mp3 in the folder. From command prompt it can run on 
 individual files by typing:
 ```
 python main_loop.py track.mp3
``` 
 Where `track.mp3` is replaced with the name of a valid .mp3 file.  Loop points will be output into `loop.txt`, to use 
 this with [Looping Audio Converter](https://github.com/libertyernie/LoopingAudioConverter/releases) extract that program
 to the same folder so that `LoopingAudioConverter.exe` is in the same directory as `loop.txt`.  To use with BRSTM
 Converter, you can manually input loop points to the numeric values listed in `loop.txt`.