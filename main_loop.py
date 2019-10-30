import sys
from loop import MusicFile


def loop_track(filename):
    try:
        # Load the file
        print("Loading {}...".format(filename))
        track = MusicFile(filename)
        track.calculate_max_frequencies()
        start_offset, best_offset, best_corr = track.find_loop_point()
        print("Found loop starting at {} sample {} and ending {} sample {} ({:.0f}% match)".format(
            format_time(track.time_of_frame(start_offset)),
            track.sample_of_frame(start_offset),
            format_time(track.time_of_frame(best_offset)),
            track.sample_of_frame(best_offset),
            best_corr * 100))
        # write_points_to_file(track.sample_of_frame(start_offset), track.sample_of_frame(best_offset))

    except (TypeError, FileNotFoundError) as e:
        print("Error: {}".format(e))


def format_time(time_sec):
    return "{:02.0f}:{:06.3f}".format(
        time_sec // 60,
        time_sec % 60
    )


def write_points_to_file(start_offset, loop_offset):
    with open("loop_points.txt","w+") as output:
        output.write("%d\r\n" % start_offset)
        output.write("%d\r\n" % loop_offset)
        print("Wrote to file")


if __name__ == '__main__':
    # Load the file
    if len(sys.argv) == 2:
        loop_track(sys.argv[1])
    else:
        print("Error: No file specified.",
              "\nUsage: python3 loop.py file.mp3")