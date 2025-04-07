import os
import librosa
import numpy as np
from datasets import Dataset, DatasetDict
from sklearn.model_selection import train_test_split
def create_whisper_hf_dataset(audio_dir, transcript_dir):
    """
    Creates a dataset with EXACT Hugging Face format:
    {
        'audio': {
            'path': str, 
            'array': np.ndarray(dtype=float32),
            'sampling_rate': int
        },
        'sentence': str
    }
    """
    data = []
    
    # Get all audio files
    audio_files = [f for f in os.listdir(audio_dir) 
                 if f.endswith(('.wav', '.mp3', '.flac'))]
    
    for audio_file in audio_files:
        audio_path = os.path.join(audio_dir, audio_file)
        transcript_path = os.path.join(
            transcript_dir, 
            os.path.splitext(audio_file)[0] + ".txt"
        )
        
        if not os.path.exists(transcript_path):
            continue
            
        try:
            # Load audio exactly as Whisper expects
            audio, _ = librosa.load(audio_path, sr=16000, dtype=np.float32)
            
            # Load transcript
            with open(transcript_path, 'r', encoding='utf-8') as f:
                transcript = f.read().strip()
            
            # Build the exact structure
            data.append({
                'audio': {
                    'path': audio_path,
                    'array': audio,  # numpy.float32 array
                    'sampling_rate': 16000
                },
                'sentence': transcript
            })
            
            
        except Exception as e:
            print(f"Skipping {audio_file}: {str(e)}")
    
    trainData, testData = train_test_split(data, train_size=0.8,random_state=42)

    # Convert to Hugging Face Dataset
    hf_dataset = DatasetDict({
        "train": Dataset.from_list(trainData),
        "test": Dataset.from_list(testData)
    })
    
    
    return hf_dataset

# Usage

dataset_path = "Sudanese_dialect_speech_dataset/SDN Dialect Corpus v1.0/Dataset files"
dataset = create_whisper_hf_dataset(os.path.join(dataset_path,"audio"), os.path.join(dataset_path,"transcript"))
dataset.save_to_disk("whisper_dataset")