import os
import numpy as np
from mpg123 import Mpg123


class UnsuccessfulLoop(Exception):
    pass


class MusicFile:
    def __init__(self, filename):
        # Load the file, if it exists and is an mp3 file
        if os.path.exists(filename) and os.path.isfile(filename):
            if filename[-3:].lower() == 'mp3':
                mp3 = Mpg123(filename)
            else:
                raise TypeError(
                        "This script can currently only handle MP3 files.")
        else:
            raise FileNotFoundError("Specified file not found.")

        # Get the waveform data from the mp3 file
        frames = list(mp3.iter_frames())
        self.frames = frames

        # Get the metadata from the mp3 file
        self.rate, self.channels, self.encoding = mp3.get_format()

    def calculate_max_frequencies(self):
        """Uses the real Fourier transform to get the frequencies over
        time for the file. Records the strongest frequency over time from
        a "fingerprint" region associated with the song's melody.
        """

        # Fourier transform each frame of the file
        frame_ffts = []

        # The first 1 and last 2 frames are omitted since they are
        # frequently of different lengths than the rest of the file
        start_frame, end_frame = (1, len(self.frames) - 2)
        for i in range(start_frame, end_frame):
            # Decode the frame (stored as a byte array)
            # into a numpy int16 array
            # (NOTE: this assumes a 16-bit encoding, which was true
            # for the files tested, but won't necessarily always be true
            arr = np.frombuffer(self.frames[i], dtype=np.int16)

            # Take just the first channel, so that we only need
            # to work with one time series
            arr = arr[::self.channels]

            # Perform the Fourier transform
            frame_fft = np.abs(np.fft.rfft(arr))
            frame_ffts.append(frame_fft)

        # Convert the list of ffts to a numpy.ndarray (easier to work with)
        fft_2d = np.stack(frame_ffts)

        # Get frequency information
        # (Should be identical for each frame, except sometimes
        # the first and last frames, which we omitted)
        frame_freq = np.fft.rfftfreq(len(arr))

        # Clip the data to a smaller range of frequencies. For the files
        # tested, this range corresponded to a "fingerprint" region
        # where the actual melody resides.
        clip_start, clip_end = (1, 25)
        frame_freq_sub = frame_freq[clip_start:clip_end]
        fft_2d_sub = fft_2d[:, clip_start:clip_end]

        # Mask out low-amplitude frequencies so that we don't match to noise
        # (this is done on a proportional threshold
        # since absolute magnitudes vary)
        fft_2d_denoise = np.ma.masked_where(
            (fft_2d_sub.T < fft_2d_sub.max() * 0.25),
            fft_2d_sub.T, False)

        # Finally, get the dominant frequency for each frame
        # (and mask it to omit any points where the dominant frequency is
        # just the baseline frequency)
        max_freq = frame_freq_sub[np.argmax(fft_2d_denoise, axis=0)]
        self.max_freq = np.ma.masked_where(max_freq == frame_freq_sub[0], max_freq)

    def sig_corr(self, s1, s2, comp_length):
        """Calculates the auto-correlation of the track (as compressed into
        max_freq) with itself, based on sub-samples starting at frames
        s1 and s2, each comp_length frames long."""

        # np.corrcoef returns an array of coefficients -
        # the simple 'R' value is at row 1, col 0
        return np.corrcoef(
                self.max_freq[s1:s1+comp_length],
                self.max_freq[s2:s2+comp_length])[1, 0]

    def pct_match(self, s1, s2, comp_length):
        """Calculates the percentage of matching notes between
        two subsamples of self.max_freq, each one comp_length notes long,
        one starting at s1 and one starting at s2
        """

        matches = (self.max_freq[s1:s1+comp_length] == self.max_freq[s2:s2+comp_length])
        return np.ma.sum(matches) / np.ma.count(matches)

    def find_loop_point(self, start_offset=0, test_len=600):
        """Finds matches based on auto-correlation over a portion
        of the music track."""

        # Using heuristics for the test length and "loop to" point.
        # NOTE: this algorithm is arbitrary and could certainly be improved,
        # especially for cases where the loop point is not totally clear

        # Number of points to test for start, the larger the number, the more points
        # will be tested giving a better loop, but also taking longer to calculate
        num_start_iterations = 25

        max_corr = 0
        best_start = None
        best_end = None
        max_end = len(self.max_freq)-test_len
        step = int((max_end-test_len-start_offset) / num_start_iterations)
        for start in range(start_offset, max_end-test_len, step):
            for end in range(start + test_len, max_end):
                best_start, best_end, max_corr = self.test_points(start, end, test_len, max_corr, best_start, best_end)
        if max_corr <= 0:
            raise UnsuccessfulLoop
        return best_start, best_end, max_corr

    def test_points(self, start, end, test_len, max_corr, best_start, best_end):
        """Tests a particular set of start and end points against the stored current best
        If these points are better than the current best, then make them the new best"""
        # Uses a slight bias to prefer earlier loop points, this keeps filesize down
        # Default of -0.0003 gives 96.5% after 2 minutes, 91% after 5 minutes
        bias = -0.0003

        sc = self.sig_corr(start, end, test_len)
        if sc > max_corr:
            # Check against bias, protecting against unassigned values first
            if best_start is None or \
                    np.exp(bias * self.time_of_frame(end)) * sc > \
                    np.exp(bias * self.time_of_frame(best_end)) * max_corr:
                best_start = start
                best_end = end
                max_corr = sc
        return best_start, best_end, max_corr

    def time_of_frame(self, frame):
        samples_per_sec = self.rate * self.channels

        # NOTE: division by 2 assumes 16-bit encoding
        samples_per_frame = len(self.frames[1]) / 2

        frames_per_sec = samples_per_sec / samples_per_frame
        time_sec = frame / frames_per_sec
        return time_sec

    def sample_of_frame(self, frame):
        # NOTE: division by 2 assumes 16-bit encoding
        samples_per_frame = len(self.frames[1]) / 2 / self.channels
        sample = frame * samples_per_frame
        return int(sample)
