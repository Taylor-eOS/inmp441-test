import serial
import struct
import wave
import numpy as np

SAMPLE_RATE = 16000
RECORD_SECONDS = 5

ser = serial.Serial('/dev/ttyACM0', 921600)
total_bytes = SAMPLE_RATE * RECORD_SECONDS * 4

print(f"Recording {RECORD_SECONDS}s...")
raw = ser.read(total_bytes)

samples = np.frombuffer(raw, dtype=np.int32) >> 8
samples_16 = (samples >> 8).clip(-32768, 32767).astype(np.int16)

with wave.open("test.wav", "w") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(samples_16.tobytes())

print("Saved test.wav")
