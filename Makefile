include ./CommonDefs.mak


# BOOST_LOCATION
# --------------
# location of boost in the filesystem
BOOST_INCLUDE = /Users/jhack/Programming/Boost		

# NiTE_LOCATION/INCLUDE/REDIST
# ----------------------------
# Where NiTE is located on your filesystem
NITE2_LOCATION 	= /Users/jhack/Programming/NI/NiTE
NITE2_INCLUDE	= /Users/jhack/Programming/NI/NiTE/Include
NITE2_REDIST64	= /Users/jhack/Programming/NI/NiTE/Redist


# OPENNI2_INCLUDE and OPENNI2_REDIST
# ----------------------------------
# Locations of Include/Redist directories on your filesystem
OPENNI2_LOCATION 	= /Users/jhack/Programming/NI/OpenNI
OPENNI2_INCLUDE 	= /Users/jhack/Programming/NI/OpenNI/Include
OPENNI2_REDIST 		= /Users/jhack/Programming/NI/OpenNI/Redist

# BIN_DIR
# -------
# Bin directory (output directory)
BIN_DIR = ./Bin


# INC_DIRS: 
# ---------
# list of all additional include directories
INC_DIRS 	+= $(OPENNI2_INCLUDE) 					#OpenNI 
INC_DIRS 	+= $(NITE2_INCLUDE)						#NiTE
INC_DIRS	+= $(BOOST_INCLUDE)						#Boost
INC_DIRS 	+= ../../../External					#OpenGL?
INC_DIRS 	+= ../../../External/GL 				#OpenGL?
# INC_DIRS 	+= /opt/local/include 					#OpenCV
# INC_DIRS 	+= /opt/local/include/opencv 			#OpenCV


# SRC_FILES:
# ----------
# list of all .cpp files to compile into the project
SRC_FILES = 	*.cpp 				#all source files in main directory
SRC_FILES += 	cpp_json/*.cpp 		#all source files in SimpleJson


# LIB_DIRS:
# ---------
# List of additional library directories
LIB_DIRS += /Users/jhack/Programming/NI/OpenNI/Redist/
LIB_DIRS += /Users/jhack/Programming/NI/NiTE/Redist/
LIB_DIRS += /Users/jhack/Programming/NI/NiTE/Bin/
LIB_DIRS += /Users/jhack/Programming/NI/NiTE/Samples/
# LIB_DIRS += /opt/local/lib 								#for OpenCV


# USED_LIBS
# ---------
# list of libraries to link with
CFLAGS += -DMACOS
LDFLAGS += -framework OpenGL -framework GLUT
USED_LIBS += OpenNI2 NiTE2 
#--- for opencv2 ---
# USED_LIBS += opencv_calib3d
# USED_LIBS += opencv_contrib
# USED_LIBS += opencv_core
# USED_LIBS += opencv_features2d
# USED_LIBS += opencv_flann
# USED_LIBS += opencv_gpu
# USED_LIBS += opencv_highgui
# USED_LIBS += opencv_imgproc
# USED_LIBS += opencv_legacy
# USED_LIBS += opencv_ml
# USED_LIBS += opencv_nonfree
# USED_LIBS += opencv_objdetect
# USED_LIBS += opencv_photo
# USED_LIBS += opencv_stitching
# USED_LIBS += opencv_superres
# USED_LIBS += opencv_ts
# USED_LIBS += opencv_video
# USED_LIBS += opencv_videostab


# EXE_NAME:
# ---------
# name of the executable 
EXE_NAME = Autosynch


# CFLAGS:
# -------
# additional flags for the compiler
CFLAGS += -Wall
CFLAGS += -DMACOS

include ./CommonCppMakefile
