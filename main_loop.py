import sys
import os
from loop import MusicFile
from loop import UnsuccessfulLoop


def loop_track(filename):
    try:
        # Load the file
        print("Loading {}...".format(filename))
        track = MusicFile(filename)
        track.calculate_max_frequencies()
    # handles errors in loading the file
    except (TypeError, FileNotFoundError) as e:
        print("Error: {}".format(e))
    # try to loop the file
    try:
        start_offset, best_offset, best_corr = track.find_loop_point()
        print("Found loop starting at {} and ending {} ({:.0f}% match)".format(
            format_time(track.time_of_frame(start_offset)),
            format_time(track.time_of_frame(best_offset)),
            best_corr * 100))
        write_points_to_file(track.sample_of_frame(start_offset), track.sample_of_frame(best_offset), filename)
    # if a loop isn't found, retry with different inputs
    except UnsuccessfulLoop:
        try:
            print("Trying again")
            start_offset, best_offset, best_corr = track.find_loop_point(10, 200)
            print("Found loop starting at {} and ending {} ({:.0f}% match)".format(
                format_time(track.time_of_frame(start_offset)),
                format_time(track.time_of_frame(best_offset)),
                best_corr * 100))
            write_points_to_file(track.sample_of_frame(start_offset), track.sample_of_frame(best_offset), filename)
        # if a loop still isn't found, give up
        except UnsuccessfulLoop:
            print("Failed to find loop")


def loop_all_tracks():
    files = os.listdir('.')
    songs = []
    for fn in files:
        if os.path.splitext(fn)[1].lower() == '.mp3':
            songs.append(fn)
    if not songs:
        print('No songs found!')
        exit(1)
    for filename in songs:
        loop_track(filename)
    print("Wrote to file")


# returns time from seconds in the form of MM:SS.mlS
def format_time(time_sec):
    return "{:02.0f}:{:06.3f}".format(
        time_sec // 60,
        time_sec % 60
    )


def write_points_to_file(start_offset, loop_offset, filename):
    with open("loop.txt", "a") as output:
        output.write("\n%d " % start_offset)
        output.write("%d " % loop_offset)
        output.write(filename)


if __name__ == '__main__':
    # Load the file
    if len(sys.argv) == 2:
        input_arg = sys.argv[1]
        if input_arg == "all":
            loop_all_tracks()
        else:
            loop_track(input_arg)
    elif len(sys.argv) == 1:
        loop_all_tracks()
    else:
        print("Error: No file specified.",
              "\nUsage: python3 loop.py file.mp3")
