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

	#--- Pop_Marker ---
	marker = None

	#--- Skeletons ---
	skeletons 				= None	#the original 			(input)
	synchronized_skeletons	= None	#synchronized version 	(output)

	#--- correspondences between beats and pops ---
	correspondences = None	#list of (beat_index, corresponding pop_index)
	beat_indices 	= None	#just the beat indeces
	pop_indices 	= None	#just the pop indeces



	# Function: constructor
	# ---------------------
	# reads in all the relevant information, then will synchronize
	def __init__ (self, infile_name, intermediary_file_name, classifier_name):
		
		### Step 1: set up the pop marker, get back marked skeletons ###
		self.marker = Pop_Marker (infile_name, classifier_name)
		self.marker.mark_pops ()
		self.skeletons = self.marker.skeletons

		### Step 2: save the intermediary skeletons ###
		write_out_skeletons(self.skeletons, intermediary_file_name)


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



if __name__ == "__main__":

	### Step 1: manage args ###
	if len(sys.argv) < 4:
		print_error ("Not enough args", "Usage: ./mark_pops.py [infile] [intermediary file] [outfile] [classifier_name]")
	infile_name 			= sys.argv[1]
	intermediary_file_name 	= sys.argv[2]
	outfile_name 			= sys.argv[3]
	classifier_name			= sys.argv[4]

	
	### Step 2: get the synchronizer ###
	synchronizer = Synchronizer (infile_name, intermediary_file_name, classifier_name)



	#--- FOR DEBUGGING ---
	# pops = [i for i in range(len(synchronizer.skeletons)) if synchronizer.skeletons[i].pop]
	# beats = [i for i in range(len(synchronizer.skeletons)) if synchronizer.skeletons[i].beat]
	# print "--- correspondences ---"
	# print synchronizer.correspondences
	# print "--- BEATS ---"
	# print beats
	# print "--- POPS ---"
	# print pops


	# synchronizer.correspondences = [(5, 4), (10, 11), (15, 14), (20, 21), (25, 24)]
	# synchronizer.beat_indices = [b[0] for b in synchronizer.correspondences]
	# synchronizer.pop_indices = [b[1] for b in synchronizer.correspondences]

	### Step 3: synchronize ###
	synchronizer.synchronize ()
	# print "--- synchronized indeces: ---"
	# print synchronizer.synchronized_indeces
	# print len(synchronizer.synchronized_indeces)

	### Step 4: write the output to a file ###
	write_out_skeletons (synchronizer.synchronized_skeletons, outfile_name)





























