# utils.py
import random
from psychopy import core, event

def clean_exit(win):
    print("🛑 Clean exiting program...")
    win.close()
    core.quit()

def generate_group_sequence(beat_intervals, num_groups):
    sequence = []
    last_interval = None
    for _ in range(num_groups):
        while True:
            seq = random.sample(beat_intervals, 3)
            if last_interval is None or seq[0] != last_interval:
                break
        sequence.append(seq)
        last_interval = seq[-1]

    print(sequence)
    return sequence

def play_beats_during_text(stimulus, message, beat_interval, duration):
    clock = core.Clock()
    next_beat_time = 0

    while clock.getTime() < duration:
        current_time = clock.getTime()
        if current_time >= next_beat_time:
            stimulus.play_beat()
            next_beat_time += beat_interval

        # 持续刷新文字
        stimulus.text_stim.text = message
        stimulus.text_stim.draw()
        stimulus.win.flip()

        try:
            keys = event.getKeys()
            if 'escape' in keys:
                clean_exit(stimulus.win)
        except Exception as e:
            print(f"⚠️ Warning: event.getKeys() failed with {e}")

        core.wait(0.01)

