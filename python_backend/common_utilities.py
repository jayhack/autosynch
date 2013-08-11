# ---------------------------------------------------------- #
# Script: common_utilities.py
# ---------------------------
# random functions that are common utilities
#
#
#
#
# ---------------------------------------------------------- #

# Function: print_error
# ---------------------
# prints an error and exits 
def print_error (top_string, bottom_string):
	print "Error: " + top_string
	print "---------------------"
	print bottom_string
	exit ()



# Function: print_status
# ----------------------
# prints out a status message 
def print_status (stage, status):
	print "-----> " + stage + ": " + status
