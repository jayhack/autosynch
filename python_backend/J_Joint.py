# ---------------------------------------------------------- #
# Script: J_Joint.py
# ------------------
# Class containing all data relevant to a single joint
#
#
#
#
# ---------------------------------------------------------- #
class J_Joint:

	#--- data ---
	x = None
	y = None
	z = None

	joint_name = None

	# Function: Constructor
	# ---------------------
	# sets all internal properties
	def __init__ (self, x, y, z, joint_name):

		#--- position ---
		self.x = x
		self.y = y
		self.z = z

		#--- joint_name ---
		self.joint_name = joint_name

	# Function: String Representation
	# -------------------------------
	# returns a string representation of this object
	def __str__ (self, ):

		return str(self.joint_name) + ": (" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"


	# Function: json
	# --------------
	# returns a json representation of all joints
	def json (self):
		return (self.joint_name, {'x':self.x, 'y':self.y, 'z':self.z})