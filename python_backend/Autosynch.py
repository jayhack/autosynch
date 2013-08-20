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
from sklearn.cluster import KMeans

#--- my files ---
from common_utilities import print_error, print_inner_status, print_message
from J_Joint import J_Joint
from J_Skeleton import J_Skeleton
from read_write import read_in_skeletons, write_out_skeletons 
from Trainer import add_derivatives_to_skeletons
from mark_pops import mark_pop_probabilities, Beat_Interval


class Autosynch:

	#--- File Names ---
	jvid_filename_raw 			= None
	jvid_filename_pops_marked 	= None
	jvid_filename_synchronized 	= None

	#--- Classifier ---
	classifier_filename = None
	classifier = None

	#--- Skeletons ---
	original_skeletons 		= None	#the original 			(input)
	marked_skeletons		= None	#the marked 			(intermediate)
	synchronized_skeletons	= None	#synchronized version 	(output)

	#--- correspondences between beats and pops ---
	correspondences = None	#list of (beat_index, corresponding pop_index)
	beat_indeces	= None
	pop_indeces		= None

	#--- synchronized_indeces ---
	synchronized_indeces = None 	#List of the indexes of the skeletons that are in the synced recording

	#--- data for training ---
	all_examples 		= None
	positive_examples 	= None
	negative_examples 	= None 




	# Function: constructor
	# ---------------------
	# reads in all of the skeletons, adds derivatives and pop_probabilities to them
	def __init__ (self, sync_directory, classifier_name, mode):

		### Step 1: filename management ###
		print_inner_status ("Initialization", "Looking at file " + sync_directory)
		self.jvid_filename_raw 				= os.path.join(sync_directory, 'Raw/video.jvid')
		self.jvid_filename_pops_marked 		= os.path.join(sync_directory, 'Marked/video.jvid')
		self.jvid_filename_synchronized 	= os.path.join(sync_directory, 'Synced/video.jvid')

		### Step 2: get the original skeletons ###
		print_inner_status ("Initialization", "Getting input skeletons")
		self.original_skeletons = read_in_skeletons (self.jvid_filename_raw)

		### Step 3: add derivatives to them ###
		print_inner_status ("Initialization", "Adding derivatives to skeletons")		
		self.original_skeletons = add_derivatives_to_skeletons(self.original_skeletons, 5, 10, 5, 10)

		### Step 4: set up the classifier filename ###
		self.classifier_filename = os.path.join (os.getcwd(), 'python_backend/classifiers/' + classifier_name)

		### Step 5.0: if synchronize mode, load the classifier and mark probabilities ###
		if mode == 'synchronize':
	
			print_inner_status ("Initialization", "Loading the classifier")
			self.load_classifier ('/Users/jhack/Programming/NI/ni_template/python_backend/classifiers/toprock_front_training.obj')

			print_inner_status ("Initialization", "Adding pop probabilities to skeletons")			
			self.original_skeletons = mark_pop_probabilities (self.original_skeletons, self.classifier)

		### Step 5.1: if train mode, train the classifier and save it ###
		elif mode == 'train':

			print_inner_status ("Initialization", "Training the classifier")
			self.train_classifier ()

			print_inner_status ("Initialization", "Saving the classifier")
			self.save_classifier ()

		return






	#####################################################################################
	#####################[ --- Classification ---] ######################################
	#####################################################################################

	# Function: train_classifier
	# --------------------------
	# trains a classifier
	def train_classifier (self):

		### Step 1: get the training data, print stats on it ###
		self.get_training_data ()
		self.print_training_data_stats ()

		### Step 2: train the actual classifier ###
		X_train = [s[0] for s in self.all_examples]
		Y_train = [s[1] for s in self.all_examples]
		self.classifier = LogisticRegression().fit(X_train, Y_train)


	# Function: get_training_data
	# ---------------------------
	# fills self.all_examples from self.training_data
	def get_training_data (self):

		self.negative_examples = []		# all the negative examples
		self.positive_examples = []		# all the positive examples, but without labels

		### Step 1: separate into two classes: +/- examples ###
		for skeleton in self.original_skeletons:

			if skeleton.beat == 1 or skeleton.beat == True:
				self.positive_examples.append (skeleton.get_feature_vector())

			else:
				self.negative_examples.append (skeleton.get_feature_vector())

		### Step 2: get clusters for each positive example ###
		km 		= KMeans (init='k-means++', n_clusters=2)
		labels 	= km.fit_predict (self.positive_examples)

		#### Step 3: fill all_examples with appropriate training data ###
		self.all_examples = []
		for index, example in enumerate(self.positive_examples):
			# self.all_examples.append ((example, labels[index]))
			self.all_examples.append ((example, 'pop'))
		for example in self.negative_examples:
			self.all_examples.append ((example, 'not_a_pop'))



	# Function: print_training_data_stats
	# -----------------------------------
	# prints out stats on the training data 
	def print_training_data_stats (self):

		print_message ("Stats on Training Data")
		print "Total Examples: ", len(self.all_examples)
		print "Positive Examples: ", len(self.positive_examples)


	# Function: save_classifier 
	# -------------------------
	# pickles the classifier 
	def save_classifier (self):

		pickle.dump(self.classifier, open(self.classifier_filename, 'w'))

	# Function: open_classifier
	# -------------------------
	# unpickles the classifier 
	def load_classifier (self, filename):

		self.classifier = pickle.load (open(filename, 'r'))


	#####################################################################################
	#####################[ --- Getting Correspondences ---] #############################
	#####################################################################################

	# Function: get_correspondences
	# -----------------------------
	# gets correspondences based on value alone
	def get_correspondences (self):

		print_inner_status ("Get correspondences", "getting the intervals")

		### Step 1: get all of the beat indeces, pop indeces ###
		self.beat_indeces = [i for i in range(len(self.original_skeletons)) if self.original_skeletons[i].beat == 1]

		beat_intervals = []

		### Step 2: get a list of beat intervals ###
		prev_beat = 0
		for i in range (len(self.beat_indeces) - 1):
			cur_beat 	= self.beat_indeces [i]
			next_beat 	= self.beat_indeces [i + 1] 

			beat_interval = Beat_Interval (cur_beat, prev_beat, next_beat)
			beat_intervals.append (beat_interval)

			prev_beat = cur_beat



		### for each beat_interval, iterate through each skeleton and select the top prob ###
		self.correspondences = []
		for beat_interval in beat_intervals:

			best_prob = -1.0
			best_index = -1
			best_class = -1
			for i in range (beat_interval.interval_start, beat_interval.interval_end):
				pop_probability = self.original_skeletons[i].pop_probability
				print i, ": ", pop_probability
				for index, p in enumerate(pop_probability[1:]):
				# for index, p in enumerate (pop_probability[:-1])
					if p > best_prob:
						best_index = i
						best_prob = p
						best_class = index



			self.correspondences.append ((beat_interval.beat_index, best_index))
			print "### best_prob: ", best_prob
			print "### best_index: ", best_index
			print "### best_class: ", best_class



		### Success up to here - correspondences is now filled with (beat, best pop) index pairs ###
		### Now mark beat/pop and write it out
		self.marked_skeletons = self.original_skeletons
		self.pop_indeces = [i[1] for i in self.correspondences]
		for i in range(len(self.marked_skeletons)):
			if i in set(self.pop_indeces):
				self.marked_skeletons[i].pop = 1
			else:
				self.marked_skeletons[i].pop = 0











	#####################################################################################
	#####################[ --- Synchronization ---] #####################################
	#####################################################################################

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
			self.synchronized_skeletons.append (self.marked_skeletons[index])

		### Step 3: Set all beat values to false ###
		for skeleton in self.synchronized_skeletons:
			skeleton.beat = False

		### Step 3: put the beats in where they should be ###
		for i in range (len(self.synchronized_skeletons)):
			if i in set(self.beat_indeces):
				self.synchronized_skeletons[i].beat = True

		return












	#####################################################################################
	#####################[ --- Writing Output ---] ######################################
	#####################################################################################

	# Function: write_pops_marked_jvid
	# --------------------------------
	# writes out self.marked_skeletons to a jvid file. call after marking pops, before synchronizing
	def write_pops_marked_jvid (self):

		for index, skeleton in enumerate (self.marked_skeletons):
			
			original_index = skeleton.original_index

			#--- get filenames ---
			skeleton_filename_new 	= os.path.join (self.jvid_filename_pops_marked, str(index) + '.s')
			color_filename_new 		= os.path.join (self.jvid_filename_pops_marked, str(index) + '.c')
			depth_filename_new 		= os.path.join (self.jvid_filename_pops_marked, str(index) + '.d')			

			color_filename_old 		= os.path.join (self.jvid_filename_raw, str(original_index) + '.c')
			depth_filename_old 		= os.path.join (self.jvid_filename_raw, str(original_index) + '.d')

			#--- write out skeleton ---
			skeleton_file = open (skeleton_filename_new, 'w')
			skeleton_file.write (skeleton.__str__())
			skeleton_file.close ()

			#--- copy over the synced files ---
			# print color_filename_old + " -> " + color_filename_new
			if (os.path.exists (color_filename_new)): 
				os.remove (color_filename_new)
			if (os.path.exists (depth_filename_new)):
				os.remove (depth_filename_new)
			os.symlink (color_filename_old, color_filename_new);
			os.symlink (depth_filename_old, depth_filename_new);


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
			# print color_filename_old + " -> " + color_filename_new
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
	synchronizer.write_pops_marked_jvid ()
	synchronizer.write_synchronized_jvid ()






























