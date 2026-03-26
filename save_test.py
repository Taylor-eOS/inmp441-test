import serial
import wave
import numpy as np

SAMPLE_RATE = 16000
RECORD_SECONDS = 5

ser = serial.Serial('/dev/ttyACM0', 921600)
total_bytes = SAMPLE_RATE * RECORD_SECONDS * 4

print(f"Recording {RECORD_SECONDS}s...")
chunks = []
received = 0
while received < total_bytes:
    chunk = ser.read(min(1024, total_bytes - received))
    data = np.frombuffer(chunk, dtype=np.int32)
    received += len(chunk)
    rms = int(np.sqrt(np.mean(data.astype(np.float64) ** 2))) if len(data) else 0
    bar = "#" * min(40, rms // 200000)
    print(f"{received}/{total_bytes}  rms={rms:12d}  {bar}")
    chunks.append(data)

samples_32 = np.concatenate(chunks).astype(np.float64)
peak = np.abs(samples_32).max()
samples_16 = (samples_32 / peak * 32767).clip(-32768, 32767).astype(np.int16)

with wave.open("test.wav", "w") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(samples_16.tobytes())

print("Saved test.wav")
