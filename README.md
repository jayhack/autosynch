--- To Compile: ---
$ make

--- To run: ---
cd into ./Bin from home directory
make sure that the environmental variable $DYLD_LIBRARY_PATH is set to your ./Bin directory:
export DYLD_LIBRARY_PATH=/path/to/bin/
(or wherever your .dylib files are for OPENNI and NiTE2)

then do ./x64-.../executable (play|record) filpath



#####[ --- FILE FORMAT --- ]#####
- all information for a single recording (pre-sync, etc) is contained in a directory with a '.sync' suffix in the Recordings directory.
- Subdirectories:
	- Raw: contains raw recordings (skeleton.skel, color_depth.oni)
	- Marked: contains a marked version:
		- Raw/skeleton.skel --> Marked/skeleton.skel
	- Synced: contains a synchronized versions:
		 - Raw/skeleton.skel --> Synced/skeleton.skel 
		 - Raw/video.oni --> Synced/skeleton.skel




#####[ --- .S file format --- ]#####
timestamp
exists
beat
pop
joint 0 x, y, z, x_abs, y_abs, z_abs
...
joint 14 x, ...
