import os
import sys
import logging
from audiocraft.models import musicgen
from audiocraft.utils.notebook import display_audio
import torch
import torchaudio

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to INFO to capture all levels of logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("audio_generation.log"),  # Log to a file
        logging.StreamHandler()  # Also print to console
    ]
)

def generate_audio(prompt):
    # Create the output directory if it doesn't exist
    output_dir = './static/audio_output'
    os.makedirs(output_dir, exist_ok=True)
    logging.info("Output directory created or already exists.")

    # Load the pre-trained MusicGen model
    model = musicgen.MusicGen.get_pretrained('medium', device='cuda')
    model.set_generation_params(duration=8)
    logging.info("MusicGen model loaded.")

    # Generate audio using the provided prompt
    res = model.generate([prompt], progress=True)
    logging.info("Audio generation started for prompt: '%s'", prompt)

    # Save generated audio files
    for i, audio in enumerate(res):
        output_file = os.path.join(output_dir, f'generated_audio_medium_{i + 1}.wav')
        
        # Move the audio tensor to the CPU
        audio_cpu = audio.cpu()
        logging.info(f"Audio tensor shape before saving: {audio_cpu.shape}")

        # Check if the audio is 1D and add the channel dimension if necessary
        if audio_cpu.dim() == 1:  # If it is a 1D tensor
            audio_cpu = audio_cpu.unsqueeze(0)  # Convert to shape (1, num_samples)
        
        # Ensure it is 2D before saving
        if audio_cpu.dim() == 2:
            torchaudio.save(output_file, audio_cpu, sample_rate=32000)  # Use the appropriate sample rate
            logging.info(f"Saved: {output_file}")
        else:
            logging.warning(f"Skipping saving for audio {i + 1}, unexpected shape: {audio_cpu.shape}")

    # Optional: Display the first audio file in the notebook (if using a Jupyter notebook)
    display_audio(res, 32000)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python generate_audio.py '<prompt>'")
        sys.exit(1)

    prompt = sys.argv[1]
    generate_audio(prompt)
