import sounddevice as sd
import soundfile as sf

def play_wav(file_path, duration_s):
    try:
        # Read the WAV file
        data, sample_rate = sf.read(file_path)
        sample_rate = 48000

        # Calculate the number of samples to play for the specified duration
        num_samples_to_play = int(duration_s * sample_rate)

        # Trim the audio data to the desired duration
        audio_data_to_play = data[:num_samples_to_play]

        # Play the audio data
        sd.play(audio_data_to_play, sample_rate)
        # sd.wait()  # Wait for the playback to finish

    except Exception as e:
        print(f"An error occurred: {e}")
