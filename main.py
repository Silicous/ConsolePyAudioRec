from recorder import Recorder
import sys

if __name__ == '__main__':

    recorder = Recorder(*sys.argv)

    # recorder.show_active_devices()
    # recorder.set_default_device('pulse')

    recorder.start()
    recorder.stop()
