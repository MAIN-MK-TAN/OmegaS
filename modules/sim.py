import numpy as np
import matplotlib.pyplot as plt
import json
from scipy.fft import fft, fftfreq
import re

def parse_time(timestr):
    minutes, seconds = timestr.split(":")[1:]
    return float(minutes) * 60 + float(seconds)

def parse_hz(hz_string):
    return float(re.sub(r'[^\d.]', '', hz_string))

def simulate(payload):
    duration = parse_time(payload["exposure_time"])
    sampling_rate = 1000
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

    freqs = payload["frequencies"]
    delivery = payload.get("delivery", "mono")
    mod_freq = parse_hz(payload.get("amplitude_modulation", "0Hz"))

    modulator = 0.5 * (1 + np.sin(2 * np.pi * mod_freq * t)) if mod_freq > 0 else 1

    if delivery == "binaural alternation" and len(freqs) >= 2:
        left = np.sin(2 * np.pi * freqs[0] * t) * modulator
        right = np.sin(2 * np.pi * freqs[1] * t) * modulator
        signal = (left + right) / 2
    else:
        signal = np.sum([np.sin(2 * np.pi * f * t) for f in freqs], axis=0) * modulator / len(freqs)

    N = len(signal)
    xf = fftfreq(N, 1 / sampling_rate)
    yf = fft(signal)
    amp = np.abs(yf[:N // 2])

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(t, signal, linewidth=0.7)
    plt.title(f"Waveform: {freqs} Hz")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    plt.subplot(1, 2, 2)
    plt.plot(xf[:N // 2], amp)
    plt.title("FFT Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.xlim(0, 500)

    plt.suptitle(f"[ID {payload['frequency_id']}] {payload['expected_effect']} — {payload['tags']}", fontsize=10)
    plt.tight_layout()
    plt.show()

class Module:
    def __init__(self):
        self.name = "Payload Sim"
        self.help = "This is an example payload simulator."

    def run(self, payload):
        simulate(payload)
        # print(json.dumps(payload, indent=2))