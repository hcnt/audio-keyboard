import pyaudio, pyautogui
import wave
import scipy.io.wavfile as wavfile
import numpy as np
import matplotlib.pyplot as pl

audio = pyaudio.PyAudio()
config = {}


def loadConfig():
    conf = {}
    for line in open('conf'):
        line = line.split()
        conf[line[0]] = [int(line[1]), int(line[2])]
    return conf


def pressKey(freq):
    for x in config:

        


def recordSound(seconds, file):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = seconds
    WAVE_OUTPUT_FILENAME = file

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    # print("* recording")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        if i > 20:
            # print(data)
            frames.append(data)

    # print("* done recording")

    stream.stop_stream()
    stream.close()
    # audio.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


# t = np.arange(len(data[:, 0])) * 1.0 / rate
# pl.plot(t, data[:, 0])
# pl.show()
def getMaxFreq(file):
    rate, data = wavfile.read('output.wav')
    p = 20 * (np.abs(np.fft.rfft(data[:2048, 0])) ** 2)
    f = np.linspace(0, rate / 2.0, len(p))
    xd = zip(p, f)
    dict = {f: p for (f, p) in zip(f, p)}
    freq = max(dict, key=dict.get)
    print(freq)
    return freq
    # pl.plot(f[5:], p[5:])
    # pl.xlabel("Frequency(Hz)")
    # pl.ylabel("Power(dB)")


while True:
    recordSound(0.7, "output.wav")
    freq = getMaxFreq("output.wav")
    pressKey(freq)
