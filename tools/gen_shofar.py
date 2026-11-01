#!/usr/bin/env python3
"""Synthesizes a placeholder shofar blast (a tekiah gedolah style held note) and encodes it as Ogg Vorbis.
Replace src/main/resources/assets/shalomcraft/sounds/shofar.ogg with a real recording whenever you have one."""
import os, subprocess, sys, wave
import numpy as np

SR = 44100
DUR = 3.0
rng = np.random.default_rng(613)
t = np.arange(int(SR * DUR)) / SR

# pitch: starts low, climbs quickly to the held note, then drifts up a little (a shofar tightens as the player pushes air)
f0 = 168 + 52 * (1 - np.exp(-t / 0.18)) + 9 * np.clip((t - 1.2) / 1.5, 0, 1)
f0 *= 1 + 0.004 * np.sin(2 * np.pi * 5.2 * t)                 # slight wobble from the lips
phase = 2 * np.pi * np.cumsum(f0) / SR

# harmonic stack, bright and slightly rough like a horn
sig = np.zeros_like(t)
for n in range(1, 19):
    formant = 1.0 + 1.6 * np.exp(-((n * 215 - 900) / 700.0) ** 2)   # brass-like bump near 900 Hz
    amp = formant / n ** 0.85
    detune = 1 + rng.normal(0, 0.0012)
    drift = 1 + 0.003 * np.sin(2 * np.pi * (0.3 + 0.11 * n) * t + n)
    sig += amp * np.sin(phase * n * detune * drift + rng.uniform(0, 2 * np.pi))

# breath: broadband noise that is strong in the attack and a little present while held
noise = rng.normal(0, 1, t.size)
kernel = np.ones(6) / 6
noise = np.convolve(noise, kernel, mode="same")
breath_env = 0.9 * np.exp(-t / 0.09) + 0.06
sig = sig / np.max(np.abs(sig)) + 0.35 * noise * breath_env

# loudness shape: quick but soft attack, long hold, gentle fall at the end
env = np.minimum(1, t / 0.16) ** 1.5
env *= np.where(t > DUR - 0.55, np.clip((DUR - t) / 0.55, 0, 1) ** 1.4, 1)
env *= 1 + 0.05 * np.sin(2 * np.pi * 6.0 * t)                  # small tremolo
sig *= env

# a touch of room: two short echoes
for delay, gain in ((0.045, 0.32), (0.11, 0.18), (0.19, 0.09)):
    d = int(delay * SR)
    sig[d:] += gain * sig[:-d]

sig = np.tanh(sig * 0.9)                                         # soft clip, keeps it brassy without harsh peaks
sig = sig / np.max(np.abs(sig)) * 0.8
pcm = (sig * 32767).astype(np.int16)

out_dir = os.path.join("src", "main", "resources", "assets", "shalomcraft", "sounds")
os.makedirs(out_dir, exist_ok=True)
wav = os.path.join(os.environ.get("TMPDIR", "/tmp"), "shofar_tmp.wav")
with wave.open(wav, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
ogg = os.path.join(out_dir, "shofar.ogg")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libvorbis", "-q:a", "4", ogg], check=True)
print("wrote", ogg, os.path.getsize(ogg), "bytes,", DUR, "seconds")
