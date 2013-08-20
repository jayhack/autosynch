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
from common_utilities import print_error, print_inner_status
from J_Joint import J_Joint
from J_Skeleton import J_Skeleton




class Beat_Interval:

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


	def __str__ (self):
		return str(self.beat_index) + ": (" + str(self.interval_start) +  ", " + str(self.interval_end) + ")"



# Function: mark_pop_probabilities
# --------------------------------
# iterates through all skeletons, marks them with p(pop|feature_vector)
def mark_pop_probabilities (skeletons, classifier):

	### Step 1: mark all skeletons with appropriate p(pop) ###
	for skeleton_index, skeleton in enumerate(skeletons):

		feature_vector = skeleton.get_feature_vector ();
		pop_probability = classifier.predict_proba(feature_vector)[0]
		skeleton.pop_probability = pop_probability

	return skeletons



# Function: get_local_maxima
# --------------------------
# given a list (timeseries), this will return the indices of all local maxima
# excludes the first and last elements of the timeseries
def get_local_maxima (timeseries):

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
# given a list of skeletons and a classifier, this function will
# return a new list of skeletons with only the true pops marked
def mark_pops (skeletons, classifier):

	marked_skeletons = skeletons

	### Step 1: get a list of all pop probabilities ###
	pop_prob_timeseries = [s.pop_probability for s in marked_skeletons]
	# print "##########[ --- POP PROB TIMESERIES --- ]##########"
	# print pop_prob_timeseries

	### Step 2: get a list of indices of local maxima in pop_prob_timeseries ###
	local_maxima = get_local_maxima (pop_prob_timeseries)
	# print "##########[ --- LOCAL MAXIMA --- ]##########"
	# for l in local_maxima:
		# print l, ": ", marked_skeletons[l].pop_probability


	### Step 3: mark the skeletons corresponding to local maxima as pops, others as non-pops ###
	local_maxima = set(local_maxima)
	for index in range (len(marked_skeletons)):
		if index in local_maxima:
			marked_skeletons[index].pop = 1
		else:
			marked_skeletons[index].pop = 0

	return marked_skeletons












