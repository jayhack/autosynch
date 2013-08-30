#!/usr/bin/python
# ---------------------------------------------------------- #
# Script: run.py
# ---------------------
# Takes care of all front-end for the program, including calling 
# scripts and everything else
#
#
#
# ---------------------------------------------------------- #
#--- Standard ---
import os
import sys
from optparse import OptionParser

#--- My files ---
sys.path.append (os.path.join (os.getcwd(), 'python_backend'))
from common_utilities import print_status, print_error, print_message, print_welcome
from Recording import Recording
from Trainer import Trainer
from Autosynch import Autosynch


#--- MODES ---
mode_map = {
	
	#--- content creation ---
	'r': 	'record',			#record a dance, with beats indicated on screen
	't': 	'train',			#use a dance as a perfect example
	's': 	'sync',				#apply synchronization procedures to it

}

#--- RECORDINGS ---
recordings_dir = os.path.join (os.getcwd(), 'Recordings')
existing_recordings = [l.split('.')[0] for l in os.listdir (recordings_dir)]



class Autosynch_Interface:

	#--- General Recordings Info ---
	recordings_dir = None
	all_recordings = []

	#--- Selected Recording ---
	selected_recording = None




	#####################################################################################
	#####################[ --- Constructor ---] #########################################
	#####################################################################################

	# Function: constructor
	# ---------------------
	# initializes the recordings_dir, all_recordings
	def __init__ (self):

		print_welcome ("Autosynch", "Jay Hack", "Summer 2013")

		### Step 1: get the recordings directory ###
		self.recordings_dir = os.path.join (os.getcwd(), 'Recordings')
		if not os.path.exists (self.recordings_dir):
			print_error ("Autosynch_Interface Initialization", "cannot find recordings directory")

		### Step 2: get all of the recordings ###
		self.get_all_recordings ()








	#####################################################################################
	#####################[ --- Dealing with recordings ---] #############################
	#####################################################################################

	# Function: get_recordings
	# ---------------------------
	# gets a recording object for each recording in recordings_dir
	def get_all_recordings (self):

		self.all_recordings = []

		recording_names = [r.split('.')[0] for r in os.listdir (self.recordings_dir)]
		for recording_name in recording_names:
			new_recording = Recording (recording_name, os.path.join (self.recordings_dir, recording_name + '.sync'))
			self.all_recordings.append (new_recording)


	# Function: list_recordings
	# -------------------------------
	# lists all recordings that are already in existence,
	# two to a row
	def list_recordings (self):
	
		print_message ("########## Exising recordings: ##########")

		num_printed = 0
		for recording in existing_recordings:
			print recording,
			if num_printed % 2 == 0:
				print "\n",
			else:
				print "				",
			num_printed += 1
		print "\n"


	# Function: select_recording ():
	# ------------------------------
	# returns the recording that the user has selected
	# (creates a new one if necessary)
	def select_recording (self):

		recording_names = [r.__str__() for r in self.all_recordings]
		names_and_recordings = zip (recording_names, self.all_recordings)

		### Step 1: ask them what they want to do ###
		print_message ("Would you like to work with an existing recording? (y/n)")
		answer = raw_input ("---> ")

		if answer == 'y':
			self.list_recordings ()
			print_message ("Enter the name of the recording you wish to work with")
			recording_name = raw_input ("---> ")
			if not recording_name in set(existing_recordings):
				print_message ("Error: the recording you entered, " + recording_name + ", doesn't exist yet.")
				self.select_recording ()
			else:
				print_message ("Opening " + recording_name)
				index = recording_names.index (recording_name)
				self.selected_recording = self.all_recordings[index]

		if answer == 'n':
			print_message ("Enter the name of the new recording")
			recording_name = raw_input ("---> ")
			self.selected_recording = self.create_new_recording (recording_name)


	# Function: create_new_sync_file
	# -----------------------------
	# creates the shell of a new recording and returns a Recording object that contains it
	def create_new_recording (self, recording_name):
		
		recording_filepath = os.path.join (recordings_dir, recording_name + '.sync')
		if (os.path.exists (recording_filepath)):
			print_error ("create_new_sync_dir", "specified file already exists")


		### Step 2: create the top-level '.sync' directory ###
		os.mkdir (recording_filepath)

		### Step 2: make the raw/marked/synced directories, along with jvid directories ###
		os.mkdir (os.path.join (recording_filepath, "Raw"))
		os.mkdir (os.path.join (recording_filepath, "Raw/video.jvid"))
		os.mkdir (os.path.join (recording_filepath, "Marked"))
		os.mkdir (os.path.join (recording_filepath, "Marked/video.jvid"))
		os.mkdir (os.path.join (recording_filepath, "Synced"))
		os.mkdir (os.path.join (recording_filepath, "Synced/video.jvid"))

		new_recording = Recording (recording_name, recording_filepath)
		self.all_recordings.append (new_recording)
		return new_recording








	#####################################################################################
	#####################[ --- Main Operation ---] ######################################
	#####################################################################################
	# Function: run
	# -------------
	# this function continuously applies the selected operation to your dance
	def run (self):

		### Step 1: record something if the file is new ###
		if self.selected_recording.is_new ():
			print_message ("Beginning recording")
			self.record ()
			print_message ("Finished recording")

		### Step 2: have the user select an operation to apply to the file ###
		selected_operation = self.select_operation ()

		print_message ("Beginning operation: " + selected_operation.__name__)
		selected_operation ()
		print_message ("Finished operation: " + selected_operation.__name__)



	# Function: select_operation
	# --------------------------
	# gets the user to select an option to apply to the existing file
	def select_operation (self):

		operations_map = {	'r': self.record,
							't': self.train,
							's': self.synchronize,
							'w': self.watch,
							'q': exit
		}


		print_message ("Select an operation to apply to this file")
		print "	[ r ]: (re-)record something for this file\n"
		print "	[ t ]: train a classifier based on this recording\n"
		print "	[ s ]: mark and synchronize this recording\n"
		print "	[ w ]: watch one of the recorings\n"
		print "	[ q ]: quit\n"
		selected_operation = raw_input ("--->")

		if not selected_operation in operations_map.keys ():
			print_message ("Error: didn't recognize that operation")
			return self.select_operation ()
		else:
			if selected_operation == 'q':
				print_message ("### EXITING PROGRAM ###")
				exit ()
			else:
				return operations_map[selected_operation]


	# Function: record
	# ----------------
	# runs the recording program, then returns
	def record (self):

		### Step 1: change into the correct directory ###
		os.chdir (os.path.join (os.getcwd(), "Bin"))

		### Step 2: build the correct command and use it ###
		system_command = "./x64-release/Autosynch record " + self.selected_recording.full_filepath
		os.system (system_command)

		### Step 3: update the recording's status ###
		self.selected_recording.set_recorded ()

		### Step 4: change back into the original directory ###
		os.chdir (os.path.join (os.getcwd(), ".."))


	# Function: train
	# ---------------
	# trains a classifier based on the raw recording 
	def train (self):

		Autosynch (self.selected_recording.full_filepath, self.selected_recording.name + '.obj', 'train')


	# Function: synchronize
	# ---------------------
	# synchronize this recording
	def synchronize (self):

		### Step 1: create the autosynch ###
		autosynch = Autosynch (self.selected_recording.full_filepath, 'toprock_front_training.obj', 'synchronize')

		### Step 2: get correspondences (which pop maps to which beat, and mark pops appropriately) ###
		autosynch.get_correspondences ()

		### Step 3: write out the pops ###
		autosynch.write_pops_marked_jvid ()

		### Step 3: get synchronized_skeletons ###
		autosynch.synchronize ()

		### Step 4: write the output to a file ###
		autosynch.write_synchronized_jvid ()


	# Function: watch
	# ---------------
	# entry point for watching a recording.
	def watch (self):

		jvids_map = {	'r': 'observe_raw',
						'm': 'observe_marked',
						's': 'observe_synced'
		}


		print_message ("Select a jvid file to play: ")
		print "	[ r ]: raw recording\n"
		print "	[ m ]: with pops marked\n"
		print "	[ s ]: synchronized\n"
		selection = raw_input ("--->")
		
		if not selection in jvids_map.keys ():
			print_message ("Error: didn't recognize that option")
			return self.watch ()

		else:
			
			### Step 1: change into the correct directory ###
			os.chdir (os.path.join (os.getcwd(), "Bin"))

			### Step 2: build the correct command and use it ###
			system_command = "./x64-release/Autosynch " + jvids_map[selection] + " " + self.selected_recording.full_filepath
			os.system (system_command)

			### Step 4: change back into the original directory ###
			os.chdir (os.path.join (os.getcwd(), ".."))	

			return



















if __name__ == "__main__":

	### Step 1: initialize the interface ###
	interface = Autosynch_Interface ()

	### Step 2: determine the recording they are working with ###
	interface.select_recording ()

	### Step 3: run indefinitely ###
	while True:
		interface.run ()









