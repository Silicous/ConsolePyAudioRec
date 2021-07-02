# Python AudioRec

---
This simple Python program can record audio input from your mic. Run in console.
Can be used as module in bigger project. 
Tested on Windows/Linux.

Following libraries were used:

####*Sound*
- **SoundDevice** - to handle input/output. Also uses PyAudio inside.
- **SoundFile**   - to read/write audio files.
	
####*System*
- **sys**
- **os**
- **timeit**

---
##How it works

At the beginning, user should specify path where to save file and filename. 
Otherwise, file will be saved in current folder with default name as **record.wav**.

After that, program asks user to type **start** or **quit** program. 

If user starts program, following cases can be:
* User can stop program at any time by typing **stop**, but if it didn't record 5 seconds of audio, 
program automatically stops when 5 seconds is reached.
* Another case, if program runs more than 60 seconds. 
In this case program will shut down itself automatically and asks to press any button.
  
At the end of any case, program will print record time, path and filename.

## Files in repository 

- **recorder.py** - this is the main module. Just import it and use wherever you want.
- **main.py** - example program. Uses *start, stop, show_active_devices, set_default_device* methods 
  to showcase recorder's functionality