# ---------------------------------------------------------- #
# Class: Recording
# ----------------
# contains all of the information relevant to a single sync file
#
#
#
# ---------------------------------------------------------- #
import os
import sys
import pickle


class File_Status:

	is_new 				= True
	is_recorded 		= False
	is_marked			= False
	is_synchronized 	= False

	def __init__ (self):
		pass



class Recording:

	#--- name/location ---
	name = None				#the name of the recording
	full_filepath = None	#its full filepath

	#--- individual files location ---
	jvid_raw = None
	jvid_marked = None
	jvid_synchronized = None

	#--- status ---
	file_status_filepath = None
	file_status = None

	#--- stats ---
	num_frames_raw = 0
	num_frames_marked = 0
	num_frames_synced = 0



	def __init__ (self, name, full_filepath):

		self.name = name
		self.full_filepath = full_filepath

		### Step 1: get this recording's file_status ###
		self.load_status ()

		### Step 2: get the individual jvids' locations ###
		self.jvid_raw 			= os.path.join (full_filepath, 'Raw/video.jvid')
		self.jvid_marked 		= os.path.join (full_filepath, 'Marked/video.jvid')
		self.jvid_synchronized 	= os.path.join (full_filepath, 'Synced/video.jvid')				



	#####################################################################################
	#####################[ --- Dealing with File Status ---] ############################
	#####################################################################################
	# Function: load_status
	# ---------------------
	# loads this recording's file_status object from a pickle file
	# (creates a new one if it doesn't already exist)
	def load_status (self):
		self.file_status_filepath = os.path.join (self.full_filepath, 'file_status.obj')
		if not os.path.exists (self.file_status_filepath):
			self.file_status = File_Status ()
		else:
			self.file_status = pickle.load (open(self.file_status_filepath, 'r'))


	# Function: save_status
	# ---------------------
	# saves this recording's status in a pickle file
	def save_status (self):
		
		pickle.dump (self.file_status, open(self.file_status_filepath, 'w'))







	#####################################################################################
	#####################[ --- Public Interface ---] ####################################
	#####################################################################################
	# Getter: is_new
	# --------------
	# returns wether anything has been recorded for this file yet
	def is_new (self):

		return self.file_status.is_new

	# Getter: is_marked
	# --------------
	# returns wether this file has been marked yet
	def is_marked (self):

		return self.file_status.is_marked

	# Getter: is_synchronized
	# -----------------------
	# returns wether the sychnronization procedure has been applied to this file yet
	def is_synchronized (self):

		return self.file_status.is_synchronized


	# Setter: set_recorded
	# --------------------
	# call this function after you have just recorded
	def set_recorded (self):

		self.file_status.is_new = False
		self.save_status ()



	# Function: string representation
	# -------------------------------
	# returns a string representation of the current recording 
	def __str__ (self):
		
		return self.name
