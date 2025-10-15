import os

import vosk
import sounddevice as sd

path = os.path.abspath("../models/vosk-model-small-en-us-0.15")
model = vosk.Model(path)
rec = vosk.KaldiRecognizer(model, 16000)

with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1) as stream:
    while True:
        data = stream.read(4000)[0]
        if rec.AcceptWaveform(bytes(data)):
            print(rec.Result())
        if rec.Result().__contains__("hello"):
            print("Heyo")