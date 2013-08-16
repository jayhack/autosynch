# ---------------------------------------------------------- #
# Script: J_Skeleton.py
# ---------------------
# Class containing all data relevant to a single skeleton 
#
#
#
#
# ---------------------------------------------------------- #
from J_Joint import J_Joint

class J_Skeleton:

	#--- properties ---
	read_index = -1
	original_index = -1
	exists = False
	beat = 0
	pop = 0
	pop_probability = 0.0

	#--- joints positions ---
	joints = None		#dict mapping joint_name to J_Joint objects

	#--- first derivatives of joint position ---
	fd_1 = None			# first derivatives of joint motion (over a smaller interval)
	fd_2 = None			# first derivatives of joint motion (over a larger interval)

	#--- second derivatives of joint position ---
	sd_1 = None			#second derivatives of joint motion (over a smaller interval)
	sd_2 = None			#second derivatives of joint motion (over a larger interval)



	# Function: Constructor
	# ---------------------
	# initializes with timestamp and joints
	def __init__ (self, read_index, original_index, exists, beat, pop, joints):

		#--- index ---
		self.read_index = read_index
		self.original_index = original_index
		self.exists = exists
		self.beat = beat
		self.pop = pop
		self.joints = joints


	# Function: setters/getters
	# -------------------------
	# setters/getters for beat/pop
	def setBeat (self, value):
		self.beat = value
	def setPop (self, value):
		self.pop = value
	def getBeat (self):
		return self.beat
	def getPop (self):
		return self.pop



	# Function: String Representation
	# -------------------------------
	# returns a string representation of this object
	def __str__ (self):
		all_strings = []

		#--- timestamp ---
		all_strings.append(str(self.original_index))
		if self.exists == 0:
			all_strings.append (str(0))
		else:
			all_strings.append (str(1))

			if self.beat == True or self.beat == 1:
				all_strings.append ('1')
			else:
				all_strings.append ('0')

			if self.pop == True or self.pop == 1:
				all_strings.append ('1')
			else:
				all_strings.append ('0')


			for i in range(15):
				current_joint = self.joints[i]
				joint_list = [current_joint.x, current_joint.y, current_joint.z, current_joint.x_abs, current_joint.y_abs, current_joint.z_abs]
				joint_list = [str(l) for l in joint_list]
				joint_string = ", ".join(joint_list)

				all_strings.append (joint_string)

		return '\n'.join(all_strings)


	# Function: get_feature_vector
	# ------------------------
	# returns a feature vector representation of this skeleton
	# Note: call this only after setting fd and sd
	def get_feature_vector (self):
		
		features = []

		for joint in self.joints.values ():
			features.append (joint.x)
			features.append (joint.y)
			features.append (joint.z)

		for deriv in self.fd_1.values ():
			features.append (deriv.x)
			features.append (deriv.y)
			features.append (deriv.z)

		for deriv in self.fd_2.values ():
			features.append (deriv.x)
			features.append (deriv.y)
			features.append (deriv.z)	
	
		for deriv in self.sd_1.values ():
			features.append (deriv.x)
			features.append (deriv.y)
			features.append (deriv.z)

		for deriv in self.sd_1.values ():
			features.append (deriv.x)
			features.append (deriv.y)
			features.append (deriv.z)

		return features





















