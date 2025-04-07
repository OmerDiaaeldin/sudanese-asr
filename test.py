
import json
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

def floats_to_audio(float_list, mode='frequency', sample_rate=44100, output_file="float_audio.wav"):
    """
    Convert a list of floats to audio with different interpretation modes.
    
    Args:
        float_list (list): List of floating-point numbers
        mode (str): Interpretation mode:
            'frequency' - values are direct frequencies in Hz
            'normalized' - values 0.0-1.0 mapped to 200-2000Hz
            'phase' - values modify phase of carrier frequency
        sample_rate (int): Audio sample rate (default 44100 Hz)
        output_file (str): Output WAV file name
    """
    float_array = np.array(float_list, dtype=float)
    total_duration = len(float_array) * 0.2  # 200ms per value
    t = np.linspace(0, total_duration, int(sample_rate * total_duration), False)
    audio = np.zeros_like(t)
    
    if mode == 'frequency':
        # Direct frequency values (in Hz)
        for i, freq in enumerate(float_array):
            start = int(i * sample_rate)
            end = int((i + 1) * sample_rate)
            segment = 0.5 * np.sin(2 * np.pi * freq * (t[start:end] - t[start]))
            audio[start:end] = segment

    # # Apply fade in/out
    # fade_samples = min(500, len(audio)//10)
    # audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
    # audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    
    # # Normalize
    # audio = 0.9 * audio / np.max(np.abs(audio)) if np.max(np.abs(audio)) > 0 else audio
    
    # Play and save
    print(f"Playing {len(float_list)} floats as audio...")
    sd.play(audio, sample_rate)
    sd.wait()
    write(output_file, sample_rate, (audio * 32767).astype(np.int16))
    print(f"Saved to {output_file}")
    
    # Plot
    plt.figure(figsize=(12, 4))
    plt.plot(t[:2000], audio[:2000])
    plt.title("First 2000 samples of generated audio")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

# Example usage
if __name__ == "__main__":
    # Example list of integers
    numbers = [1, 5, 3, 8, 2, 7, 4, 10, 6, 9]
    ptr = open("miniFinalDataSet.json")
    dc = json.load(ptr)[0]['audio']
    arr = dc['array']
    sr = dc['sampling_rate']
    
    
    # Convert to audio
    floats_to_audio(arr,sample_rate=sr)

