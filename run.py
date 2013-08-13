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
	'r': RECORD_MODE,
	'p': PLAY_MODE,
	'b': MARK_BEATS_MODE,
	'm': MARK_POPS_MODE,
	's': SYNCHRONIZE_MODE,
}

play_options_map = {
	'r': 'Raw',
	'b': 'Marked/skeleton_just_beats.skel',
	'p': 'Marked/skeleton.skel',
	's': 'Synced/skeleton.skel'
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
	#--- [(-r|-p|-s)]: play or record mode ---
	parser.add_option ("-r", "--record", 		action="store_const", const=RECORD_MODE,		dest="mode", help="Instructs the program to make a new recording")
	parser.add_option ("-p", "--play",			action="store_const", const=PLAY_MODE, 			dest="mode", help="Instructs the program to play a certain file; also allows you to mark the file")
	parser.add_option ("-b", "--mark_beats", 	action="store_const", const=MARK_BEATS_MODE, 	dest="mode", help="Instructs the program to play a file and mark the beats for you")
	parser.add_option ("-m", "--mark_pops", 	action="store_const", const=MARK_POPS_MODE, 	dest="mode", help="Instructs the program to play a file and allow you to mark pops.")
	parser.add_option ("-s", "--synchronize", 	action="store_const", const=SYNCHRONIZE_MODE, 	dest="mode", help="Instructs the program to perform synchronization on the recording")
	(options, args) = parser.parse_args (sys.argv)


	### Step 2: Get mode ###
	if options.mode == None:
		selected_mode = raw_input ("--- AVAILABLE MODES ---\n- r = record \n- p = play\n- s = synchronize\n- b = mark beats\n- m = mark pops\nEnter a mode: ")
		if not selected_mode in mode_map.keys ():
			print_error ("Dafuq was that", "Enter one of the options listed above, breh")
		else:
			options.mode = mode_map[selected_mode]


	### Step 3: Get filenames ###
	if options.filename == None:
		selected_filename = raw_input ("Enter the name of a recording:\n(new one if you are recording, existing one otherwise): ")
		options.filename = selected_filename


	### Step 4: make sure filename is valid for this operation ###
	sync_dir_path = os.path.join (os.path.join (recordings_dir, options.filename + ".sync"))
	if options.mode == RECORD_MODE:
		if os.path.exists (sync_dir_path):
			print_error ("the filename you entered already exists", "delete that shit and try again")
		else:
			create_new_sync_dir (sync_dir_path)
	else:
		if not os.path.exists (sync_dir_path):
			print_error ("the filename you entered does not exist", "gotta record that shit first, breh")


	### Step 5: get the arguments to pass to the C++ program ###
	print_status ("CLI", "starting program")
	system_command = None
	if options.mode == RECORD_MODE:	
		cpp_args = ['record', sync_dir_path]
		os.chdir (os.path.join(os.getcwd(), "Bin"))
		system_command = "./x64-Release/ni_template " + ' '.join(cpp_args)

	elif options.mode == PLAY_MODE:

		### Query what to play ###
		play_file_name = None
		selected_file = raw_input ("Which file would you like to play?\n- r = raw\n- b = just beats marked\n- p = both beats and pops marked\n- s = synchronized\nFile choice: ")
		if not selected_file in play_options_map:
			print_error ("Dafuq was that", "enter one of the above options")

		cpp_args = ['play', sync_dir_path];
		os.chdir (os.path.join(os.getcwd(), "Bin"))
		system_command = "./x64-Release/ni_template " + ' '.join(cpp_args)

	elif options.mode == MARK_BEATS_MODE:
		cpp_args = ['play', os.path.join(sync_dir_path, "Raw/skeleton.skel"), os.path.join(sync_dir_path, "Marked/skeleton_just_beats.skel"), os.path.join (sync_dir_path, "Raw/video.oni")]
		os.chdir (os.path.join (os.getcwd(), "Bin"))
		system_command = "./x64-Release/ni_template " + ' '.join(cpp_args)	

	elif options.mode == MARK_POPS_MODE:
		cpp_args = ['play', os.path.join(sync_dir_path, "Marked/skeleton_just_beats.skel"), os.path.join(sync_dir_path, "Marked/skeleton.skel"), os.path.join (sync_dir_path, "Raw/video.oni")]		
		os.chdir (os.path.join (os.getcwd(), "Bin"))
		system_command = "./x64-Release/ni_template " + ' '.join(cpp_args)	

	elif options.mode == SYNCHRONIZE_MODE:
		python_args = [	os.path.join (sync_dir_path, "Marked/skeleton_just_beats.skel"), 	#just the beats
						os.path.join (sync_dir_path, "Marked/skeleton.skel"),				#will contain beats/pops
						os.path.join (sync_dir_path, "Synced/skeleton.skel"), 				#synchronizec
						'./python_backend/classifiers/two_of_each_deriv.obj'				#classifier
					]
		system_command = "./python_backend/synchronize.py " + ' '.join(python_args)

	print system_command
	os.system (system_command)





