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

#--- ML ---
from sklearn.linear_model import LogisticRegression

#--- my files ---
from common_utilities import print_error, print_status
from J_Joint import J_Joint
from J_Skeleton import J_Skeleton
from read_write import read_in_skeletons, write_out_skeletons 
from train_classifier import add_derivatives_to_skeletons



class Beat_interval:

	beat_index = None
	interval_start = None
	interval_end = None

	# Function: constructor
	# ---------------------
	# makes a Beat_interval out of the current index
	def __init__ (self, beat_index, pre_beat_index, next_beat_index):

		self.beat_index = beat_index

		self.interval_start = beat_index - int((self.beat_index - pre_beat_index)*0.5)
		self.interval_end = beat_index + int((next_beat_index - self.beat_index)*0.5)




class Pop_Marker:

	#--- classifier ---
	classifier = None	#classifier for pops

	#--- loaded skeletons ---
	skeletons = None 	#will contain all skeletons in chronological order, 
						#with beats marked, fd and sd filled
	#--- beats ---
	beat_indexes 	= []	#
	beat_intervals 	= []	#list of Beat_interval objects
	#--- pops ---
	pop_indexes = []		#filling this is our main objective

	#--- beat/pop pairs ---
	beat_pop_pairs = []		# a list of (beat_index, correspdonding_pop_index) tuples


	# Function: Constructor
	# ---------------------
	# loads skeletons and the classifier; marks beats and beat intervals
	def __init__ (self, skeletons, classifier_name):

		### Step 1: load classifier ###
		self.classifier = pickle.load (open(classifier_name, 'rb'))

		### Step 2: get skeletons ###
		self.skeletons = add_derivatives_to_skeletons (skeletons, 5, 10, 5, 10)




	# Function: mark_pop_probabilities
	# --------------------------------
	# iterates through all skeletons, marks them with p(pop|feature_vector)
	def mark_pop_probabilities (self):

		### Step 1: mark all skeletons with appropriate p(pop) ###
		for skeleton_index, skeleton in enumerate(self.skeletons):

			feature_vector = skeleton.get_feature_vector ();
			pop_probability = self.classifier.predict_proba(feature_vector)[0][1]
			skeleton.pop_probability = pop_probability



	# Function: get_local_maxima
	# --------------------------
	# given a list (timeseries), this will return the indices of all local maxima
	# excludes the first and last elements of the timeseries
	def get_local_maxima (self, timeseries):

		local_maxima = []

		for i in range(1, len(timeseries) - 1):	
			
			#--- indices ---
			cur_index 	= i
			prev_index 		= cur_index - 1
			next_index 		= cur_index + 1

			#--- values ---
			prev 	= timeseries 	[prev_index]
			cur 	= timeseries 	[cur_index]
			next 	= timeseries	[next_index]

			if (cur > prev) and (cur > next):
				local_maxima.append (cur_index)

		return local_maxima



	# Function: mark_pops
	# -------------------
	# iterates through all skeletons, marks them as pop or otherwise
	# currently implemented by just finding local maxima
	def mark_pops (self):

		### Step 1: mark all pop probabilities ###
		self.mark_pop_probabilities ()

		### Step 1: get a list of all pop probabilities ###
		pop_prob_timeseries = [s.pop_probability for s in self.skeletons]

		### Step 2: get a list of indices of local maxima in pop_prob_timeseries ###
		local_maxima = self.get_local_maxima (pop_prob_timeseries)

		### Step 3: mark the skeletons corresponding to local maxima as pops, others as non-pops ###
		local_maxima = set(local_maxima)
		for index in range (len(self.skeletons)):
			if index in local_maxima:
				self.skeletons[index].pop = 1
			else:
				self.skeletons[index].pop = 0










if __name__ == '__main__':

	### Step 1: manage args ###
	if len(sys.argv) < 4:
		print_error ("Not enough args", "Usage: ./mark_pops.py [infile] [outfile] [classifier_name]")
	infile_name 	= sys.argv[1]
	outfile_name 	= sys.argv[2]
	classifier_name	= sys.argv[3]

	### Step 2: load classifier ###
	marker = Pop_Marker (infile_name, classifier_name)

	### Step 3: mark skeletons as pops or otherwise ###
	marker.mark_pops ()

	### Step 4: get beat intervals ###
	# marked_skeletons = marker.get_marked_skeletons ()


	### Step 5: write them back out to file ###
	write_out_skeletons(marker.skeletons, outfile_name)






