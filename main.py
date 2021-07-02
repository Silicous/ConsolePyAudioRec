from recorder import Recorder

if __name__ == '__main__':

    recorder = Recorder()

    # recorder.show_active_devices()
    # recorder.set_default_device('pulse')

    recorder.start()
    recorder.stop()