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
from common_utilities import print_error, print_status

#--- MODES ---
RECORD_MODE = 0
PLAY_MODE = 1
MARK_BEATS_MODE = 2
MARK_POPS_MODE = 3
SYNCHRONIZE_MODE = 4
mode_map = {
	'r': 'record',
	'm': 'mark',
	'o': 'observe_marked',
	's': 'sync',
	'q': 'observe_synced'
}


#--- RECORDINGS ---
recordings_dir = os.path.join (os.getcwd(), 'Recordings')


# Function: create_new_sync_dir
# -----------------------------
# creates the shell of a .sync dir for a new recording
def create_new_sync_dir (sync_dir_path):
		
	### Step 1: create the top-level '.sync' directory ###
	os.mkdir (sync_dir_path)

	### Step 2: make the raw/marked/synced directories, along with jvid directories ###
	os.mkdir (os.path.join (sync_dir_path, "Raw"))
	os.mkdir (os.path.join (sync_dir_path, "Raw/video.jvid"))
	os.mkdir (os.path.join (sync_dir_path, "Marked"))
	os.mkdir (os.path.join (sync_dir_path, "Marked/video.jvid"))	
	os.mkdir (os.path.join (sync_dir_path, "Synced"))
	os.mkdir (os.path.join (sync_dir_path, "Synced/video.jvid"))


if __name__ == "__main__":


	### Step 1: set up the parser/get arguments ###
	parser = OptionParser ()
	#--- [-f filename]: specifies where to play from/record to ---
	parser.add_option("-f", "--filename", action="store", type="string", dest="filename")
	#--- [(-r|-p|-s)]: (play|record|synchronize) mode ---
	parser.add_option ("-r", "--record", 		action="store_const", const=RECORD_MODE,		dest="mode", help="Instructs the program to make a new recording")
	parser.add_option ("-p", "--play",			action="store_const", const=PLAY_MODE, 			dest="mode", help="Instructs the program to play a certain file; also allows you to mark the file")
	parser.add_option ("-s", "--synchronize", 	action="store_const", const=SYNCHRONIZE_MODE, 	dest="mode", help="Instructs the program to perform synchronization on the recording")
	(options, args) = parser.parse_args (sys.argv)

	### Step 2: Get mode ###
	if options.mode == None:
		selected_mode = raw_input ("--- AVAILABLE MODES ---\n- r = record mode\n- m = mark mode\n- o = observe marked mode\n- s = synchronize mode\n- q = observe synchronized mode\nEnter a mode: ")
		if not selected_mode in mode_map.keys ():
			print_error ("Invalid mode", "Enter one of the options listed above. exiting.")
		else:
			options.mode = mode_map[selected_mode]

	### Step 3: Get filenames ###
	if options.filename == None:
		selected_filename = raw_input ("Enter the name of a recording:\n(new one if you are recording, existing one otherwise): ")
		options.filename = selected_filename

	### Step 4: make sure filename is valid for this operation ###
	sync_dir_path = os.path.join (os.path.join (recordings_dir, options.filename + ".sync"))
	if options.mode == 'record':
		if os.path.exists (sync_dir_path):
			print_error ("the filename you entered already exists", "delete that shit and try again")
		else:
			create_new_sync_dir (sync_dir_path)
	else:
		if not os.path.exists (sync_dir_path):
			print_error ("the filename you entered does not exist", "gotta record that shit first, breh")








	### Step 5: get the arguments to pass to the C++ program ###
	print_status ("CLI", "starting program")

	cpp_args = [options.mode, sync_dir_path]
	os.chdir (os.path.join(os.getcwd(), "Bin"))
	system_command = "./x64-release/ni_template " + ' '.join(cpp_args)
	print_status ("CLI", "Executing command: " + system_command)
	os.system(system_command);






