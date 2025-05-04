from pydub import AudioSegment
from pydub.generators import Sine

# Constants
SAMPLE_RATE = 44100  # Sample rate (samples per second)
AMPLITUDE = 16000  # Amplitude of the sine wave (max for 16-bit PCM audio)
DURATION = 1.0  # Duration of each note in seconds

# Mapping note names to frequencies (in Hz)
NOTE_FREQUENCIES = {
    'do': 261.63, 're': 293.66, 'mi': 329.63, 'fa': 349.23, 'sol': 392.00, 
    'la': 440.00, 'si': 493.88
}

# Generate sine wave for a given frequency using pydub's Sine generator
def generate_sine_wave(frequency, duration=DURATION, sample_rate=SAMPLE_RATE):
    sine = Sine(frequency)
    return sine.to_audio_segment(duration=duration * 1000)  # Duration in milliseconds

# Class to handle the music interpretation
class MusicInterpreter:
    def __init__(self, parsed_data):
        self.parsed_data = parsed_data
        self.tempo = 120  # Default tempo (beats per minute)
        self.volume = 80  # Volume (0 to 127)
        self.final_audio = AudioSegment.silent(duration=0)  # Start with an empty audio segment
    
    def fraction_to_duration(self, fraction, tempo):
        beat_duration_in_ms = (60 / tempo) * 1000
        return beat_duration_in_ms * eval(fraction)

    def generate_music(self):
        for chunk in self.parsed_data:
            for statement in chunk['statements']:
                if statement['type'] == 'TIME_SIGNATURE':
                    pass  # Handle time signature if needed
                elif statement['type'] == 'TEMPO':
                    self.tempo = int(statement['value'].split('=')[1])
                elif statement['type'] == 'VOLUME':
                    self.volume = int(statement['value'].split('=')[1])
                elif statement['type'] == 'PIANO':
                    self.handle_piano(statement)
                elif statement['type'] == 'GUITAR':
                    self.handle_guitar(statement)
                elif statement['type'] == 'SYNC':
                    self.handle_sync(statement['statements'])
                elif statement['type'] == 'LOOP':
                    self.handle_loop(statement)

    def handle_piano(self, statement):
        note_name = statement['identifier2']
        fraction = statement['fraction']
        frequency = NOTE_FREQUENCIES.get(note_name)
        if frequency:
            duration_ms = self.fraction_to_duration(fraction, self.tempo)
            sine_wave_segment = generate_sine_wave(frequency, duration=duration_ms / 1000)
            self.final_audio += sine_wave_segment

    def handle_guitar(self, statement):
        note_name = statement['identifier2']
        fraction = statement['fraction']
        frequency = NOTE_FREQUENCIES.get(note_name)
        if frequency:
            duration_ms = self.fraction_to_duration(fraction, self.tempo)
            sine_wave_segment = generate_sine_wave(frequency, duration=duration_ms / 1000)
            self.final_audio += sine_wave_segment

    def handle_sync(self, sync_statements):
        for statement in sync_statements:
            if statement['type'] == 'PIANO':
                self.handle_piano(statement)
            elif statement['type'] == 'GUITAR':
                self.handle_guitar(statement)

    def handle_loop(self, loop_data):
        loop_start_value = loop_data['start_value']
        loop_condition = loop_data['condition_value']
        loop_increment = int(loop_data['increment_value'])
        loop_body = loop_data['body']
        
        loop_start_frequency = NOTE_FREQUENCIES.get(loop_start_value)
        loop_condition_frequency = NOTE_FREQUENCIES.get(loop_condition)
        
        if loop_start_frequency is None or loop_condition_frequency is None:
            raise ValueError(f"Invalid note in loop: {loop_start_value} or {loop_condition}")

        current_frequency = loop_start_frequency

        while current_frequency <= loop_condition_frequency:
            for action in loop_body:
                if action['type'] == 'PIANO':
                    self.handle_piano(action)
                elif action['type'] == 'GUITAR':
                    self.handle_guitar(action)
            current_frequency += loop_increment * (loop_condition_frequency - loop_start_frequency) / 7

    def save_to_mp3(self, filename="output.mp3"):
        self.final_audio.export(filename, format="mp3")  # Export final composition to MP3
