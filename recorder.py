# recorder.py
import pandas as pd
import os

class Recorder:
    def __init__(self):
        self.records = []

    def record(self, group, block, beat_interval, beat_number, expected_beat_time, reaction_time):
        press_time_sec = expected_beat_time + (reaction_time / 1000.0) if reaction_time is not None else None

        self.records.append({
            'group': group,
            'block': block,
            'beat_interval_ms': int(beat_interval * 1000),
            'beat_index': beat_number,
            'beat_time_sec': round(expected_beat_time, 4),
            'press_time_sec': round(press_time_sec, 4) if press_time_sec is not None else 'F',
            'reaction_time': round(reaction_time / 1000.0, 4) if reaction_time is not None else None
        })

    def record_miss(self, group, block, beat_interval, beat_number, expected_beat_time):
        self.records.append({
            'group': group,
            'block': block,
            'beat_interval_ms': int(beat_interval * 1000),
            'beat_index': beat_number,
            'beat_time_sec': round(expected_beat_time, 4),
            'press_time_sec': 'F',
            'reaction_time': 'F'
        })

    def save_to_csv(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df = pd.DataFrame(self.records)
        df.to_csv(filepath, index=False)