from scipy.signal import filtfilt, hilbert, firwin
import numpy as np


class FilterHilbert:

    def __init__(self, x, n_cycles, fsample, freq_lim, width_lim, nfreq):
        self.x = x
        self.n_cycles = n_cycles
        self.fsample = fsample
        self.freq_lim = freq_lim
        self.width_lim = width_lim
        self.nfreq = nfreq
        self.frequencies, _ = self._frequencies()
        self.nsample = x.shape[-1]
        self.ntrials = x.shape[0]

    def filter_hilbert(self):
        """

        :return:
        """
        freq, width = self._frequencies()
        x_hilb = np.zeros((self.nfreq, self.ntrials, self.nsample), dtype="complex")
        for i, (f, w) in enumerate(zip(freq, width)):
            print(f"filtering: {f - w / 2}-{f + w / 2}Hz")
            x_filt = self._filter([f - w / 2, f + w / 2])
            x_hilb[i] = hilbert(x_filt, axis=-1)

        return x_hilb

    def power(self, x_hilb):

        pow = np.abs(x_hilb)

        return pow

    def _frequencies(self):
        freq = np.logspace(np.log10(self.freq_lim[0]), np.log10(self.freq_lim[1]), self.nfreq)
        width = np.logspace(np.log10(self.width_lim[0]), np.log10(self.width_lim[1]), self.nfreq)

        return freq, width

    def _filter(self, cutoff):
        lkernel = int(self.n_cycles * self.fsample / cutoff[0]) + 1
        b = firwin(lkernel, [cutoff[0], cutoff[1]], fs=self.fsample, pass_zero='bandpass'), 1
        try:
            x_filt = filtfilt(b[0], b[1], self.x, axis=-1)
        except:
            print('padlen manual')
            x_filt = filtfilt(b[0], b[1], self.x, axis=-1, padlen=self.x.shape[-1] - 1)
    



        return x_filt


