#!/usr/bin/python
# ---------------------------------------------------------- #
# Script: train_classifier.py
# ---------------------------
# trains the 'pop' classifier
#
#
#
#
# ---------------------------------------------------------- #
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


#--- globals ---
correct_order = [0, 1, 2, 4, 6, 3, 5, 7, 8, 9, 10, 11, 13, 12, 14]
important_body_parts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]


# Class: Derivative
# -----------------
# used in classification
class Derivative:
	x = None
	y = None
	z = None

	def __init__ (self, x, y, z):
		self.x = x
		self.y = y
		self.z = z



# Function: get_first_derivatives
# -------------------------------
# given a list of all skeletons, this returns a list of first derivatives
# derivative_length: the number of elements back you go in order to get the deriv
# - NOTE: framerate for this bitch is apparently 30 frames/second
def get_derivatives (entries, derivative_length):

	cur_index = derivative_length
	prev_index = 0
	considering_entries = entries[cur_index:]

	first_derivatives = []

	prev = entries[prev_index]
	for cur in considering_entries:

		derivs = {}
		for i in cur.keys():


			dx_dt = cur[i].x - prev[i].x
			dy_dt = cur[i].y - prev[i].y
			dz_dt = cur[i].z - prev[i].z

			derivs[i] = Derivative (dx_dt, dy_dt, dz_dt)

		prev_index += 1
		prev = entries[prev_index]
		first_derivatives.append (derivs)

	return first_derivatives



# Function: add_skeleton_derivatives 
# ----------------------------------
# given a list of skeletons, this returns a list of skeletons with fd/sd filled
def add_derivatives_to_skeletons (skeletons, fd_interval_1, fd_interval_2, sd_interval_1, sd_interval_2):

	if (fd_interval_1 >= fd_interval_2):
		print_error ("fd_interval_1 is <= fd_interval_2", "make sure that 1 is smaller than 2")
	if (sd_interval_1 >= sd_interval_2):
		print_error ("sd_interval_1 is <= sd_interval_2", "make sure that 1 is smaller than 2")

	### Step 1: get the first and second derivatives ###
	# NOTE: you will want to fuck with this until you seem to be getting it right...
	joints = [s.joints for s in skeletons]
	fd_1_raw 	=	get_derivatives 	(joints, fd_interval_1)
	fd_2_raw	=	get_derivatives 	(joints, fd_interval_2)
	sd_1_raw 	= 	get_derivatives 	(fd_1_raw, sd_interval_1)
	sd_2_raw	= 	get_derivatives 	(sd_1_raw, sd_interval_2)	

	### Step 4: associate them with the original skeletons ###
	considering_skeletons = skeletons[fd_interval_2 + sd_interval_2:]
	fd_1 = fd_1_raw [sd_interval_2:]
	fd_2 = fd_2_raw [sd_interval_2:]
	sd_1 = sd_1_raw
	sd_2 = sd_2_raw
	for i in range(len(considering_skeletons)):
		considering_skeletons[i].fd_1 = fd_1[i]
		considering_skeletons[i].fd_2 = fd_2[i]
		considering_skeletons[i].sd_1 = sd_1[i]
		considering_skeletons[i].sd_2 = sd_2[i]

	return considering_skeletons





# Function: get_training_examples 
# -------------------------------
# given position/all derivatives, this returns a tuple of positive/negative examples.
def get_training_data (skeletons):

	examples = []
	labels = []
	
	for skeleton in skeletons:

		examples.append (skeleton.get_feature_vector ())
		labels.append (skeleton.get_label ())
	return (examples, labels)



# Function: load_classifier
# -------------------------
# loads the classifier from a pickled file
def load_classifier (filename):
	
	return pickle.load (open(filename, 'rb'))


# Function: save_classifier
# -------------------------
# save the classifier to a pickled file
def save_classifier (classifier, filename):

	return pickle.dump (classifier, open(filename, 'wb'))


# Function: evaluate_classifier
# -----------------------------
# evaluates the classifier...
def evaluate_classifier (classifier, X, Y):

	hits = 0
	misses = 0

	total_prob_true = 0.0
	total_prob_false = 0.0
	num_true = 0
	num_false = 0

	for i in range (len(X)):

		example = X[i]
		true_label = Y[i]

		prediction = classifier.predict (example)


		prediction_prob = classifier.predict_proba (example)
		p_of_pop = prediction_prob[0][1]


		if prediction == true_label:
			hits += 1
		else:
			misses += 1

		# print "true_label | prediction: ", true_label, " | ", prediction


		prediction_prob = classifier.predict_proba (example)
		print "true_label | prediction: ", true_label, " | ", prediction_prob, " | ", prediction

	print "--- RESULTS ---"
	print 'hits: ', hits
	print 'misses: ', misses
	print 'accuracy: ', float(hits)/float(hits+misses)




if __name__ == "__main__":

	### Step 1: manage args ###
	if len(sys.argv) < 3:
		print_error ("Not enough args", "Usage: ./train_classifier.py [infile] [classifier_name] [(load|save|test)]")
	infile_name 	= sys.argv[1]
	classifier_name	= sys.argv[2]
	if 'load' in sys.argv:
		load = True
	else:
		load = False
	if 'save' in sys.argv:
		save = True
	else:
		save = False
	if 'test' in sys.argv:
		test = True
	else:
		test = False


	### Step 2: read in the skeleton timeseries and add derivatives to them ###
	skeletons = read_in_skeletons (infile_name)
	fd_interval_1 = 5
	fd_interval_2 = 10
	sd_interval_1 = 5
	sd_interval_2 = 10
	skeletons = add_derivatives_to_skeletons (skeletons, fd_interval_1, fd_interval_2, sd_interval_1, sd_interval_2)


	### Step 3: put it into training data form ###
	(X, Y) = get_training_data (skeletons)

	### Step 4: get it in training data form ###
	all_data = zip(X, Y)
	print "Number of examples: ", len(all_data)
	random.shuffle (all_data);
	training = all_data[:-1]
	# testing = all_data[6000:]
	#--- training ---
	X_train = [t[0] for t in training]
	Y_train = [t[1] for t in training]
	#--- testing ---
	# X_test = [t[0] for t in testing]
	# Y_test = [t[1] for t in testing]



	#--- get the classifier ---
	classifier = None
	if load:
		print "---> Status: loading classifier"
		classifier = load_classifier (classifier_name)
	else:
		print "---> Status: training classifier"
		classifier = LogisticRegression().fit(X_train, Y_train)


	#--- saving data ----
	if save:
		print "---> Status: pickling classifier"
		save_classifier (classifier, classifier_name)

	# #--- testing ---
	if test:
		print "---> Status: evaluating"
		evaluate_classifier (classifier, X_test, Y_test)









