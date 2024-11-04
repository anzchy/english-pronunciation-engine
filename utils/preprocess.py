from pydub import AudioSegment
import os

def convert_audio(input_file, output_file):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Convert to mono, 16-bit, 16 kHz
    audio = audio.set_channels(1)
    audio = audio.set_sample_width(2)  # 16-bit is 2 bytes
    audio = audio.set_frame_rate(16000)

    # Export the converted audio with a proper RIFF header
    audio.export(output_file, format="wav", codec='pcm_s16le')

if __name__ == "__main__":
    input_file = "abandon.mp3"  # Change this to your input file
    output_file = "abandon.wav"  # Change this to your desired output file

    if not os.path.exists(input_file):
        print(f"Input file {input_file} does not exist.")
    else:
        convert_audio(input_file, output_file)
        print(f"Converted audio saved to {output_file}")