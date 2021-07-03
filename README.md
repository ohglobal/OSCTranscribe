# OSCTranscribe
A python-based audio transcription utility designed to tie to production software via Open Sound Control (OSC). Based on work from Programming for People.

You can see the the original work at: https://www.youtube.com/watch?v=T3jd-894Ar4

## Source Dependencies
You'll need to install these libraries if you plan to build from source:

PythonOSC for using Open Sound Control: https://pypi.org/project/python-osc/

PyAudio for getting data from the mic: https://pypi.org/project/PyAudio/

Python Speech Recognition, which calls the recognition API: https://pypi.org/project/SpeechRecognition/

## OSC Commands

OSC API for Controlling OSCTranscribe:

/OSCTranscribe/calibrate {int thresh}: Setup, establishes the amount of quite space before processing

/OSCTranscribe/startListening: Setup, begins listening to the mic and sending to the learning system

/OSCTranscribe/stopListening: Stops listening to the mic and stops sending to the learning system


By default, you send these commands to port 7070. Then, you should listen for the following OSC message:
/OSCTranscribe/data {string text}: The words recognized from the audio stream in between pauses
