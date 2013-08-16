#!/usr/bin/python
# ---------------------------------------------------------- #
# Script: mark_pops.py
# ---------------------
# contains a class that will mark all of the pops in a skeleton
# timeseries if the beats have been labelled
#
#
#
# ---------------------------------------------------------- #
#--- Standard ---
import sys
import os
import shutil
import math
import random
import pickle
from operator import itemgetter 

#--- ML ---
from sklearn.linear_model import LogisticRegression

#--- my files ---
from common_utilities import print_error, print_status
from J_Joint import J_Joint
from J_Skeleton import J_Skeleton
from read_write import read_in_skeletons, write_out_skeletons 
from train_classifier import add_derivatives_to_skeletons
from mark_pops import Pop_Marker


class Synchronizer:

	#--- File Names ---
	jvid_filename_raw 			= None
	jvid_filename_pops_marked 	= None
	jvid_filename_synchronized 	= None

	#--- Pop_Marker ---
	marker = None

	#--- Skeletons ---
	original_skeletons 		= None	#the original 			(input)
	synchronized_skeletons	= None	#synchronized version 	(output)

	#--- correspondences between beats and pops ---
	correspondences = None	#list of (beat_index, corresponding pop_index)
	beat_indices 	= None	#just the beat indeces
	pop_indices 	= None	#just the pop indeces

	#--- synchronized_indeces ---
	synchronized_indeces = None 	#List of the indexes of the skeletons that are in the synced recording

	# Function: constructor
	# ---------------------
	# reads in all the relevant information, then will synchronize
	def __init__ (self, sync_directory, classifier_name):
		
		### Step 1: filename management ###
		print_status ("Synchronizer", "looking at file " + sync_directory);
		self.jvid_filename_raw 			= os.path.join(sync_directory, 'Marked/video.jvid')
		self.jvid_filename_pops_marked 	= os.path.join(sync_directory, 'Marked/video_with_pops.jvid')
		self.jvid_filename_synchronized 	= os.path.join(sync_directory, 'Synced/video.jvid')
		# print "	### Raw jvid: " + self.jvid_filename_raw
		# print "	### Pops_Marked jvid: " + self.jvid_filename_pops_marked
		# print "	### Synchronized jvid: " + self.jvid_filename_synchronized


		### Step 1: get the original skeletons ###
		self.skeletons = read_in_skeletons (self.jvid_filename_raw)
		# for skeleton in self.skeletons:
			# print skeleton.joints

		### Step 1: set up the pop marker, get back marked skeletons ###
		self.marker = Pop_Marker (self.skeletons, classifier_name)
		self.marker.mark_pops ()
		self.skeletons_marked = self.marker.skeletons

		### Step 2: save the intermediary skeletons ###
		write_out_skeletons(self.skeletons_marked, self.jvid_filename_pops_marked)

		### Step 2: find the correspondance between beats and pops ###
		self.get_correspondences_naive ()




	# Function: get_closest_element
	# -----------------------------
	# given integer pivot and a list of integers int_list, this returns
	# the element in int_list closest to int_1
	def get_closest_element (self, pivot, int_list):

		min_distance = 10000000
		best_element = None
		for element in int_list:
			distance = abs(pivot - element)
			if distance < min_distance:
				min_distance = distance
				best_element = element
		return best_element


	# Function: get_closest_elements
	# ------------------------------
	# given a beat index and a list of (pop_index, pop_probability), this will return
	# a sorted list of pops by proximity of pop_index
	def get_closest_elements (self, beat_index, pops_list):

		### Step 1: get a list of distances, append it ###
		distances = [abs(p[0] - beat_index) for p in pops_list]
		pops_with_distances = [(distances[i], pops_list[i]) for i in range(len(pops_list))]

		### Step 2: get a sorted version of pops_with_distances ###
		pops_with_distances = sorted(pops_with_distances, key=itemgetter(1))
		print pops_with_distances

		### Step 3: get a sorted version of pops_list and return it ###
		pops_list_sorted = [p[1] for p in pops_with_distances]
		return pops_list_sorted


	# Function: get_correspondences_naive
	# -------------------------------------------
	# gets the best possible pairing between beats/pops in a naive fashion;
	# (Greedy algorithm, where each beat choooses in sequence the best pop by proximity alone)
	# fills self.correspondances, self.beat_indices, self.pop_indices 
	def get_correspondences_naive (self):

		self.correspondences = []

		### Step 1: get lists of raw beat, pop indices ###
		beat_indeces_raw 	= [i for i in range(len(self.skeletons)) if self.skeletons[i].beat]
		pop_indices_raw 	= [i for i in range(len(self.skeletons)) if self.skeletons[i].pop]

		pop_list = [(i, self.skeletons[i].pop_probability) for i in range(len(self.skeletons)) if self.skeletons[i].pop]

		### Step 2: for each beat, find the corresponding pop ###
		for beat_index in beat_indeces_raw:
			closest_pop = self.get_closest_element (beat_index, pop_indices_raw)
			self.correspondences.append ((beat_index, closest_pop))
			pop_indices_raw.remove (closest_pop)

		### Step 3: fill in self.beat_indices, self.pop_indices ###
		self.beat_indices 	= [c[0] for c in self.correspondences]
		self.pop_indices 	= [c[1] for c in self.correspondences]

		### Step 4: mark only true 'pop' skeletons as having pops ###
		for index, skeleton in enumerate(self.skeletons):
			if index in set(self.pop_indices):
				skeleton.pop = True
			else:
				skeleton.pop = False


	# Function: get_correspondences_less_naive
	# -------------------------------------------
	# gets the best possible pairing between beats/pops in a *less* naive fashion;
	# (Greedy algorithm, where each beat choooses in sequence the best pop by proximity
	# *and* the value of the pop
	def get_correspondences_less_naive (self):

		self.correspondences = []

		### Step 1: get lists of raw beat, pop indices ###
		beat_indeces_raw 	= [i for i in range(len(self.skeletons)) if self.skeletons[i].beat]
		pop_indices_raw 	= [i for i in range(len(self.skeletons)) if self.skeletons[i].pop]

		pop_list = [(i, self.skeletons[i].pop_probability) for i in range(len(self.skeletons)) if self.skeletons[i].pop]

		### Step 2: for each beat, find the corresponding pop ###
		for beat_index in beat_indeces_raw:
			closest_pop = self.get_closest_element (beat_index, pop_indices_raw)
			self.correspondences.append ((beat_index, closest_pop))
			pop_indices_raw.remove (closest_pop)

		### Step 3: fill in self.beat_indices, self.pop_indices ###
		self.beat_indices 	= [c[0] for c in self.correspondences]
		self.pop_indices 	= [c[1] for c in self.correspondences]

		### Step 4: mark only true 'pop' skeletons as having pops ###
		for index, skeleton in enumerate(self.skeletons):
			if index in set(self.pop_indices):
				skeleton.pop = True
			else:
				skeleton.pop = False


	# Function: get_synchronized_indeces
	# ---------------------------
	# ----- THE ACTUAL SYNCHRONIZATION ALGORITHM -----
	# goes to work on beat_pop_pairs, filling up self.synchronized_indeces with the correct sequence so that
	# the two are realigned
	# 
	def get_synchronized_indeces (self):

		self.synchronized_indeces = []

		prev_beat	= 0
		prev_pop 	= 0
		for (current_beat, current_pop) in self.correspondences:


			### get distances ###
			# beat_dist = distance between this beat and the previous beat
			beat_dist 	= current_beat - prev_beat

			# pop_dist = distance between this pop and the previous pop
			pop_dist 	= current_pop - prev_pop

			### add in/subtract the right number of frames ###
			for frame_index in range(beat_dist):
				new_frame_index = prev_pop + ((float(frame_index) / float(beat_dist)) * pop_dist)
				self.synchronized_indeces.append(int(new_frame_index))

			### udpate iterators ###
			prev_beat = current_beat
			prev_pop = current_pop


	# Function: synchronize
	# ---------------------
	# will fill self.synchronized_skeletons so that it contains the synchronized
	# version
	def synchronize (self):

		### Step 1: get the synchronized indexes (fills self.synchronized_indeces) ###
		self.get_synchronized_indeces ()

		### Step 2: fill up synchronized_skeletons ###
		self.synchronized_skeletons = []
		for index in self.synchronized_indeces:
			self.synchronized_skeletons.append (self.skeletons[index])

		### Step 3: Set all beat values to false ###
		for skeleton in self.synchronized_skeletons:
			skeleton.beat = False

		### Step 3: put the beats in where they should be ###
		for i in range (len(self.synchronized_skeletons)):
			if i in set(self.beat_indices):
				self.synchronized_skeletons[i].beat = True

		return


	# Function: write_synchronized_jvid
	# ---------------------------------
	# once synchronize() has already been called, this will write out the synchronized version
	def write_synchronized_jvid (self):

		for index, skeleton in enumerate(self.synchronized_skeletons):

			original_index = skeleton.original_index

			#--- get filenames ---
			skeleton_filename_new 	= os.path.join (self.jvid_filename_synchronized, str(index) + '.s')
			color_filename_new 		= os.path.join (self.jvid_filename_synchronized, str(index) + '.c')
			depth_filename_new 		= os.path.join (self.jvid_filename_synchronized, str(index) + '.d')			

			color_filename_old 		= os.path.join (self.jvid_filename_raw, str(original_index) + '.c')
			depth_filename_old 		= os.path.join (self.jvid_filename_raw, str(original_index) + '.d')

			#--- write out skeleton ---
			skeleton_file = open(skeleton_filename_new, 'w')
			skeleton_file.write(skeleton.__str__())
			skeleton_file.close ()

			#--- copy over the synced files ---
			print color_filename_old + " -> " + color_filename_new
			# shutil.copy (color_filename_old, color_filename_new)
			# shutil.copy (depth_filename_old, depth_filename_new)
			if (os.path.exists (color_filename_new)): 
				os.remove (color_filename_new)
			if (os.path.exists (depth_filename_new)):
				os.remove (depth_filename_new)
			os.symlink (color_filename_old, color_filename_new);
			os.symlink (depth_filename_old, depth_filename_new);






if __name__ == "__main__":

	### Step 1: manage args ###
	if len(sys.argv) < 3:
		print_error ("Not enough args", "Usage: ./synchronize.py [.sync file] [classifier_name]")
	sync_dir 			= sys.argv[1]
	classifier_name		= sys.argv[2]

	
	### Step 2: get the synchronizer ###
	synchronizer = Synchronizer (sync_dir, classifier_name)


	#--- FOR DEBUGGING ---
	print "\n\n##########[ --- SYNCHRONIZER OUTPUT --- ]##########"
	pops = [i for i in range(len(synchronizer.skeletons)) if synchronizer.skeletons[i].pop]
	beats = [i for i in range(len(synchronizer.skeletons)) if synchronizer.skeletons[i].beat]
	print "--- correspondences ---"
	print synchronizer.correspondences
	print "--- BEATS ---"
	print beats
	print "--- POPS ---"
	print pops
	print "\n\n"


	### Step 3: get synchronized_skeletons ###
	synchronizer.synchronize ()

	### Step 4: write the output to a file ###
	synchronizer.write_synchronized_jvid ()






























