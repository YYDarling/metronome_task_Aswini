
===========================
Metronome Task Experiment
===========================

📌 Description:
---------------
This is a PsychoPy-based behavioral experiment designed to measure participants' synchronization tapping accuracy with auditory beats at varying intervals (450ms, 750ms, 1000ms). Participants respond by pressing the SPACE BAR in sync with each beat.

📂 Folder Structure:
--------------------
- main.py           → Main entry point to launch the task
- config.py         → Experiment settings (intervals, durations, keys, sound file path)
- stimulus.py       → Handles display and sound
- recorder.py       → Saves trial-wise responses to CSV
- utils.py          → Helper functions for beat generation and instruction playback
- resources/        → Contains the audio file `beat.wav`
- output/           → Output folder for CSV results

🖥️ Requirements:
----------------
- Python 3.10
- PsychoPy >= 2023.2
- pandas

Install requirements via:
```bash
pip install psychopy pandas
```

If you're on macOS and experience black screen issues in fullscreen:
- Set `waitBlanking=False` in `main.py`
- Avoid `size=(...)` with `fullscr=True`

🚀 How to Run:
--------------
1. Open terminal in the `metronome_task` folder.
2. Run:

```bash
python main.py
```

3. You'll be prompted to enter:
   - Subject ID (e.g., 001)
   - Session (e.g., sham)

4. Follow on-screen instructions:
   - Press 't' to start, 'esc' to quit.
   - Practice: Listen to beats without tapping
   - Tapping: Press SPACE BAR in sync with beats
   - 3 groups × 3 blocks = 9 total tapping blocks
   - Each block contains:
     - ~3 seconds of passive listening
     - 19 seconds of active tapping
     - 18 seconds of rest

5. Press 't' to start, Press `ESC` at any time to exit.

📄 Output File:
---------------
Saved under `output/{SubjectID}_{Session}_results.csv`

Each row contains:

| Column              | Description                                      |
|---------------------|--------------------------------------------------|
| group               | Group number (1-3)                               |
| block               | Block number within the group (1-3)              |
| beat_interval_ms    | Beat interval for this block (e.g., 450)         |
| beat_index          | Index of the beat (starting from 1)              |
| beat_time_sec       | Time when the beat occurred (ideal time)         |
| press_time_sec      | Calculated as beat_time_sec + reaction_time      |
| reaction_time       | Participant's RT in seconds (F if missed)        |

Missed responses will show:
- press_time_sec = 'F'
- reaction_time = 'F'

🎧 Notes:
---------
- Auditory beats are played from `resources/beat.wav`
- Sound volume is configured in `config.py`
- Default key for tapping: SPACE
- Start trigger key: 't'

👩‍💻 Author:
-----------
This experiment was developed by Yun☁️.

🛠 Troubleshooting:
-------------------
- If PsychoPy throws black screen in fullscreen on macOS:
  → Use `fullscr=False` or `waitBlanking=False`
- To escape fullscreen when stuck, press `ESC`

Have fun syncing!
