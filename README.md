# Looper
A script for repeating music seamlessly and endlessly,
designed with video game music in mind.  This has been modified to output a text file with loop points, 
instead of playing the file.

## Installation
This script requires Python 3 to run, along with the NumPy and mpg123 packages.
Once you have Python 3 installed, and this repository cloned or downloaded,
you can install any needed packages using the following command:

```sh
pip install -r requirements.txt
```

This program also requires the external library `mpg123`, which is available
here: https://www.mpg123.de/download.shtml

## Usage
Looper is run from the command line as follows:

```sh
python3 main_loop.py track.mp3
```

If track.mp3 is a valid .mp3 file, then Looper will find as good a loop
point as it can, and will output those loop points to the terminal.

## Limitations
At this point, Looper only supports .mp3 files.
If you would like to see support for other audio formats,
such as .ogg or .flac, let me know - or, better
yet, feel free to send a pull request!

Looper currently requires an extended period of time (about 20 seconds)
where the song already repeats itself, in order to confirm the
precise loop point. If the song does not repeat, or it repeats less
than that (or not at all), then it will loop, but it may do so at
strange points (such as repeatedly looping over a few seconds.)
If there is a song that you think Looper should be able to handle but
find it cannot, please feel free to contact me (or, again,
to fork this repository and improve upon it.)
