import pyaudio, pyautogui
import wave
import scipy.io.wavfile as wavfile
import numpy as np

audio = pyaudio.PyAudio()
config = {}
pressedKeys = {}
mouseMovements = ["up", "down", "left", "right"]


def loadConfig():
    conf = {}
    for line in open('config'):
        line = line.split()
        conf[line[0]] = [int(line[1]), int(line[2])]
    return conf


def pressKey(freq):
    mouseSensitivity = 50
    for x in config:
        if x in mouseMovements:
            if x == "up" and config["up"][0] < freq < config["up"][1]:
                pyautogui.move(0, -mouseSensitivity)
            elif x == "down" and config["down"][0] < freq < config["down"][1]:
                pyautogui.move(0, mouseSensitivity)
            elif x == "right" and config["right"][0] < freq < config["right"][1]:
                pyautogui.move(mouseSensitivity, 0)
            elif x == "left" and config["left"][0] < freq < config["left"][1]:
                pyautogui.move(-mouseSensitivity, 0)
        if x == "click" and config["click"][0] < freq < config["click"][1]:
            posX, posY = pyautogui.position()
            pyautogui.click(posX, posY, button="left")
            # elif x == "mouseDown" and config["mouseDown"][0] < freq < config["mouseDown"][1]:
            #     pyautogui.mouseDown(posX, posY, button="left")
        elif config[x][0] < freq < config[x][1]:
            pyautogui.keyDown(x)
            pressedKeys[x] = True


def checkKeys():
    for x in pressedKeys:
        if not pressedKeys[x]:
            pyautogui.keyUp(x)


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

def getMaxFreq(file):
    rate, data = wavfile.read('output.wav')
    # print(len(data))
    if len(data) != 0:
        p = 20 * (np.abs(np.fft.rfft(data[:2048, 0])) ** 2)
        f = np.linspace(0, rate / 2.0, len(p))
        dict = {f: p for (f, p) in zip(f, p)}
        freq = max(dict, key=dict.get)
        print(freq)
        return freq
    else:
        print("za krótki sygnał")
        return 0

    # pl.plot(f[5:], p[5:])
    # pl.xlabel("Frequency(Hz)")
    # pl.ylabel("Power(dB)")


config = loadConfig()
print(config)
while True:
    pressedKeys = {x: False for x in pressedKeys}
    recordSound(0.55, "output.wav")
    freq = getMaxFreq("output.wav")
    pressKey(freq)
    checkKeys()
