# stimulus.py
from psychopy import visual, sound, core


class Stimulus:
    def __init__(self, win, sound_file, volume=1.0):
        self.win = win
        self.beat = sound.Sound(sound_file)
        self.beat.setVolume(volume)
        self.text_stim = visual.TextStim(win, text="", color="white", height=0.06)

    def show_text(self, message, duration=None):
        self.text_stim.text = message
        self.text_stim.draw()
        self.win.flip()
        if duration:
            core.wait(duration)

    def show_countdown(self, message, duration):
        countdown_timer = core.CountdownTimer(duration)
        while countdown_timer.getTime() > 0:
            remaining_time = int(countdown_timer.getTime()) + 1
            self.text_stim.text = f"{message}\n\nRemaining Time: {remaining_time} s"
            self.text_stim.draw()
            self.win.flip()
            core.wait(0.1)

    def play_beat(self):
        self.beat.play()