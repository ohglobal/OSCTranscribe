#OSCTranscibe
#Originally Created by C4E
#Maintained and updated by Andy Carluccio
#Liminal Entertainment Technologies, LLC

#Last updated 7/3/2021

#OSC variables & libraries
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import udp_client 

#Argument management and system
import argparse
import sys

#Print the names of all available audio devices
import pyaudio
p = pyaudio.PyAudio()

print("ALL SYSTEM AUDIO DEVICES:")
print()

for i in range(p.get_device_count()):
	sys.stdout.write(str(i))
	sys.stdout.write(" ")
	sys.stdout.write(p.get_device_info_by_index(i).get("name"))
	sys.stdout.write('\n')

print()
print("Please select the audio device to listen to:")

micIndex = int(input())

#Speech Recognition libraries
import speech_recognition as sr
r = sr.Recognizer()
m = sr.Microphone(micIndex)
stop_listening = None

print("Successfully Bound to Mic")

def callback(recognizer, audio):
	print("Data Received from Mic")
	try:
		data = r.recognize_google(audio)
		print(data)
		client.send_message("/OSCTranscribe/data", data)
	except sr.UnknownValueError:
		print("Failed to recognize voice")
	except sr.RequestError:
		print("Can't reach the web API for learning, check internet / firewall")

def calibrate_threshold(unused_addr, args):
	print("Calibration Received")
	client.send_message("/calibration", "Calibration commenced")
	try:
		with m as source:
			r.adjust_for_ambient_noise(source, duration = 1.0)
			#client.send_message("/calibration", "Minimum threshold set to {}".format(r.energy_threshold))
	except (KeyboardInterrupt):
		print("keyboard interrupt received")
		pass

def start_listening(unused_addr):
	global stop_listening
	print("Starting Listening")
	#client.send_message("/startedListening","Listening thread started")
	stop_listening = r.listen_in_background(m, callback,phrase_time_limit = 5.0,)
	return
	
def stop_listening(unused_addr):
	global stop_listening 
	print("Stopping Listening")
	#client.send_message("/stoppedlistening","stopped mirophone thread")
	stop_listening(wait_for_stop = False)

if __name__ == "__main__":

	#Get the networking info from the user
	print("Would you like to [1] Input network parameters or [2] use default: 127.0.0.1:1234 (send) and 127.0.0.1:7070 (receive)?")
	print("Enter 1 or 2")
	
	send_ip = "127.0.0.1"
	send_port = 1234
	in_port = 7070

	selection = int(input())
	if(selection == 1):
		print("Input network parameters")
		send_ip = str(input("Send ip?: "))
		send_port = int(input("Send port?: "))
		in_port = int(input("Receive port?: "))
	else:
		print("Using default network settings")
	
	#sending osc messages on
	client = udp_client.SimpleUDPClient(send_ip,send_port)
	sys.stdout.write("Opened Client on: ")
	sys.stdout.write(send_ip)
	sys.stdout.write(":")
	sys.stdout.write(str(send_port))
	sys.stdout.write('\n')

	#catches OSC messages
	dispatcher = dispatcher.Dispatcher()
	dispatcher.map("/OSCTranscribe/calibrate", calibrate_threshold)
	dispatcher.map("/OSCTranscribe/startListening", start_listening)
	dispatcher.map("/OSCTranscribe/stopListening", stop_listening)
	
	#set up server to listen for osc messages
	server = osc_server.ThreadingOSCUDPServer((send_ip,in_port),dispatcher)
	print("Starting Server on {}".format(server.server_address))
	
	#Print API
	print("OSC Networking Established")
	print()
	print("OSC API for Controlling OSCTranscribe:")
	print("/OSCTranscribe/calibrate {int thresh}: Setup, establishes the amount of quite space before processing")
	print("/OSCTranscribe/startListening: Setup, begins listening to the mic and sending to the learning system")
	print("/OSCTranscribe/stopListening: Stops listening to the mic and stops sending to the learning system")
	print()
	print("OSC API for Receiving Text from OSCTranscribe:")
	print("/OSCTranscribe/data {string text}: The words recognized from the audio stream in between pauses")
	print()

	#begin the infinite loop
	server.serve_forever()