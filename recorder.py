import os
import queue
import sys
import timeit
from threading import Thread, Event
from time import sleep

import sounddevice as sd
import soundfile as sf


class Recorder:
    def __init__(self, file_path=os.getcwd() + '/record.wav'):
        self.save_to = file_path
        self.sound_input = queue.Queue()

        self.user_thread = Thread(target=self._run_user)
        self.timer_thread = Thread(target=self._run_timer)
        self.audio_thread = Thread(target=self._run_audio)

        self.user_event = Event()
        self.timer_event = Event()
        self.audio_event = Event()

    @staticmethod
    def show_active_devices():
        print(sd.query_devices())

    @staticmethod
    def set_default_device(device: str):
        sd.default.device = device

    def _run_user(self):
        while True:

            if input().lower() == 'stop':

                self.user_event.set()
                break
            else:
                if self.timer_event.isSet():
                    self.user_event.set()
                    break

    def _run_timer(self):
        start_time = timeit.default_timer()

        while True:
            current_time = timeit.default_timer() - start_time
            if current_time > 5.0:

                if current_time > 60.0:
                    break

                if self.user_event.wait(0.1):
                    print("\nRecord stopped. Final record time:", current_time)
                    self.timer_event.set()
                    return
            else:
                sleep(0.1)

        print("Record stopped (over 60 sec). Please, enter any button")
        self.timer_event.set()

    def _run_audio(self):
        print("Audio recording is started")

        def callback(indata, outdata, frames, time, status):
            if status:
                print(status, file=sys.stderr)

            indata *= 2  # to increase volume make smth like 'x * data", where 'x' is a multiplier

            outdata[:] = indata
            self.sound_input.put(indata.copy())

        with sf.SoundFile(self.save_to, mode='w+', samplerate=44100, subtype='PCM_24', channels=2) as file:
            with sd.Stream(samplerate=44100, channels=2, callback=callback):
                print("\nRecording started...\n")
                while True:
                    if self.timer_event.wait(0.1):
                        self.audio_event.set()
                        break
                while not self.sound_input.empty():
                    file.write(self.sound_input.get())

        print(f"Finished. Your file is saved in {''.join(self.save_to)} file\n")

    def start(self):
        print('\n', '\\' * 80, f"\n{' ' * 30}Python AudioRec\n", '\\' * 80, '\n')

        key = input("Type 'start' to begin recording or 'quit' to exit program: ")
        while key.lower() not in ['start', 'quit']:
            key = input("Please, enter 'start' or 'quit': ")

        if key.lower() == 'quit':
            sys.exit("Goodbye...\n")

        print("Type stop to terminate program and save file")

        self.user_thread.start()
        self.timer_thread.start()
        self.audio_thread.start()

    def stop(self):
        self.user_thread.join()
        self.timer_thread.join()
        self.audio_thread.join()

