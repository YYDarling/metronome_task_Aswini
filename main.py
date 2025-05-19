# main.py
from psychopy import visual, event, core, gui, prefs
from config import *
from stimulus import Stimulus
from recorder import Recorder
from collections import OrderedDict
from utils import generate_group_sequence, play_beats_during_text
import os

prefs.hardware['audioLib'] = ['ptb', 'pyo', 'sounddevice']
prefs.hardware['audioLatencyMode'] = '3'

def clean_exit(win):
    print("🛑 Clean exiting program...")
    win.close()
    core.quit()

def wait_for_trigger(win):
    stim = visual.TextStim(win, text="Waiting for trigger (press 't')", color="white")
    stim.draw()
    win.flip()
    keys = event.waitKeys(keyList=[TRIGGER_KEY, 'escape'])
    if 'escape' in keys:
        clean_exit(win)

def main():
    win = visual.Window(size=(1500, 1200), fullscr=False, color="black", units="norm", waitBlanking=True)
    win.flip()  # 💡 强制刷新，确保窗口显示！

    # 📋 获取受试者信息
    info = OrderedDict([('Subject ID', ''), ('Session', 'sham')])
    dlg = gui.DlgFromDict(dictionary=info, title='Metronome Task Setup')
    if not dlg.OK:
        clean_exit(win)

    subject_id = info['Subject ID']
    session_num = info['Session']

    # 在main()函数启动前增加
    if not os.path.exists(BEAT_SOUND_FILE):
        raise FileNotFoundError(f"音频文件 {BEAT_SOUND_FILE} Not Found")

    stim = Stimulus(win, BEAT_SOUND_FILE, BEAT_SOUND_VOLUME)
    recorder = Recorder()
    group_sequence = generate_group_sequence(BEAT_INTERVALS, NUM_GROUPS)

    # ⭐ Start Instruction ⭐
    start_instruction = (
        "Start instructions:\n\n"
        "You will tap your finger in sync with sounds played through headphones.\n"
        "The beats may be 'fast', 'moderate', or 'slow'.\n\n"
        "Each block has '3' seconds of listening (no tapping) and '20' seconds of tapping, \n"
        "followed by around '18' seconds of rest.\n"
        "You will complete '9' blocks in total.\n\n\n\n"
    )
    stim.show_text(start_instruction)

    # ✅ 等待受试者按 't' 开始 or 'ESC' 退出
    keys = event.waitKeys(keyList=[TRIGGER_KEY, 'escape'])
    if 'escape' in keys:
        clean_exit(win)

    # 🕒 开始总计时
    total_clock = core.Clock()

    for group_idx, beat_seq in enumerate(group_sequence):
        for block_idx, beat_interval in enumerate(beat_seq):

            practice_instruction = (
                "Practice instruction:\n\n"
                # "Listen to the beats for 3 seconds.\n\n"
                "Do NOT press any key during this practice.\n\n"
                "In the next part, press the 'SPACE BAR' in sync with the beats."
            )
            play_beats_during_text(stim, practice_instruction, beat_interval, PRACTICE_DURATION)

            # 细节调整
            core.wait(beat_interval)

            # 3秒倒计时
            for countdown in range(3, 0, -1):
                stim.text_stim.text = f"Starting in {countdown}..."
                stim.text_stim.draw()
                win.flip()
                core.wait(1)

            tapping_instruction = (
                "Tapping:\n\n"
                "Press the 'SPACE BAR' in sync with the beats."
            )
            # stim.show_text(tapping_instruction, duration=1.0)
            stim.show_text(tapping_instruction)

            tapping_clock = core.Clock()

            beat_times = [1.0]
            while beat_times[-1] + beat_interval <= TAPPING_DURATION:
                beat_times.append(beat_times[-1] + beat_interval)

            # beat_idx = 0
            # handled_beats = set()
            # while tapping_clock.getTime() < TAPPING_DURATION:
            #     current_time = tapping_clock.getTime()
            #
            #     if beat_idx < len(beat_times) and current_time >= beat_times[beat_idx]:
            #         stim.play_beat()
            #         beat_idx += 1
            #
            #     keys = event.getKeys(timeStamped=tapping_clock)
            #     for key, t in keys:
            #         if key == 'escape':
            #             clean_exit(win)
            #         if key != TAPPING_KEY:
            #             continue
            #
            #         nearest_beat_time = min(beat_times, key=lambda bt: abs(bt - t))
            #         nearest_idx = beat_times.index(nearest_beat_time) + 1
            #         if nearest_idx not in handled_beats:
            #             recorder.record(group_idx+1, block_idx+1, beat_interval, nearest_idx, nearest_beat_time, t)
            #             handled_beats.add(nearest_idx)
            #
            # for idx, expected_time in enumerate(beat_times, start=1):
            #     if idx not in handled_beats:
            #         recorder.record_miss(group_idx + 1, block_idx + 1, beat_interval, idx, expected_time)
            #
            # if not (group_idx == NUM_GROUPS - 1 and block_idx == 2):
            #     stim.show_countdown("Rest", duration=BREAK_DURATION)
            #     if 'escape' in keys:
            #         clean_exit(win)

            beat_idx = 0
            keypress_records = {}

            while tapping_clock.getTime() < TAPPING_DURATION:
                current_time = tapping_clock.getTime()

                if beat_idx < len(beat_times) and current_time >= beat_times[beat_idx]:
                    stim.play_beat()
                    beat_idx += 1

                keys = event.getKeys(timeStamped=tapping_clock)
                for key, t in keys:
                    if key == 'escape':
                        clean_exit(win)
                    if key != TAPPING_KEY:
                        continue

                    nearest_beat_time = min(beat_times, key=lambda bt: abs(bt - t))
                    nearest_idx = beat_times.index(nearest_beat_time) + 1
                    if nearest_idx not in keypress_records:
                        keypress_records[nearest_idx] = (nearest_beat_time, t - 1.0)

            for idx, expected_time in enumerate(beat_times, start=1):
                if idx in keypress_records:
                    nearest_beat_time, keypress_time = keypress_records[idx]
                    recorder.record(group_idx+1, block_idx+1, beat_interval, idx, nearest_beat_time, keypress_time)
                else:
                    recorder.record_miss(group_idx+1, block_idx+1, beat_interval, idx, expected_time)

            if not (group_idx == NUM_GROUPS - 1 and block_idx == 2):
                stim.show_countdown("Rest", duration=BREAK_DURATION)

    # save information
    os.makedirs('output', exist_ok=True)
    output_filename = f'output/{subject_id}_{session_num}_results.csv'
    recorder.save_to_csv(output_filename)

    # 🕒 显示总耗时
    total_time_sec = total_clock.getTime()
    minutes = int(total_time_sec // 60)
    seconds = int(total_time_sec % 60)
    print(f"🕒 Total experiment time: {minutes} min {seconds} sec")

    stim.show_text("Congratulations! Task Completed.\n\n\n")
    keys = event.waitKeys(keyList=[TRIGGER_KEY, 'escape'])
    if 'escape' in keys:
        clean_exit(win)
    elif 't' in keys:
        win.close()
        main()



    clean_exit(win)

if __name__ == "__main__":
    main()