/* ---------------------------------------------- 	*
 *	File: J_StorageDelegate.cpp
 *	-----------------
 *	class that takes care of playing (and labelling)
 *	recordings, both unsynchronized and otherwise
 *
 *	----------------------------------------------	*/
 /*--- Standard ---*/
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#include <map>
#include <vector>
#include <string>
#include <sstream>
#include <unistd.h>

/*--- NiTE ---*/
#include "NiTE.h"

/*--- My Files ---*/
#include "Utilities.h"
#include "J_Skeleton.h"
#include "J_Frame.h"
#include "J_FilenameManager.h" 
#include "J_StorageDelegate.h"

/*--- Namespaces ---*/
using namespace std;


/*########################################################################################################################*/
/*###############################[--- Constructor/Initialization/Destructor ---] #########################################*/
/*########################################################################################################################*/

/* Function: Constructor
 * ---------------------
 * - initializes filename manager appropriately
 * 
 */
J_StorageDelegate::J_StorageDelegate () {}
J_StorageDelegate::J_StorageDelegate (	const char *selected_file_path, 		//filepath to the .sync directory
										int selected_mode):

										filename_manager (selected_file_path) 
{

	print_status ("J_StorageDelegate", "Setting paramters");
	current_read_index = 0;
	current_write_index = 0;

	/*### Step 1: parse the mode ###*/
	print_status ("J_StorageDelegate", "Parsing mode");


	if (selected_mode == RECORD_MODE) {

		in_directory.assign ("");
		out_directory.assign(filename_manager.get_filename(RAW, JVID_FILE));

	}
	else if (selected_mode == OBSERVE_RAW_MODE) {
		in_directory.assign (filename_manager.get_filename 	(RAW, JVID_FILE));
		out_directory.assign(filename_manager.get_filename	(MARKED, JVID_FILE));	
	}
	else if (selected_mode == OBSERVE_MARKED_MODE) {
		in_directory.assign (filename_manager.get_filename 	(MARKED, JVID_FILE));
		out_directory.assign(filename_manager.get_filename	(SYNCED, JVID_FILE));	
	}
	else if (selected_mode == OBSERVE_SYNCHRONIZED_MODE) {
		in_directory.assign (filename_manager.get_filename(SYNCED, JVID_FILE));
		out_directory.assign ("");
	}
	else {
		print_error ("J_StorageDelegate", "could not parse the mode you entered");
		cout << "(mode = " << selected_mode << endl;
	}

	print_status("J_StorageDelegate - in_directory", in_directory.c_str());	
	print_status("J_StorageDelegate - out_directory", out_directory.c_str());		



}
J_StorageDelegate::~J_StorageDelegate () {}





/*########################################################################################################################*/
/*###############################[--- Writing ---] ###############################################################*/
/*########################################################################################################################*/
/* Function: get_next_filepaths
 * --------------------------------
 * returns a vector containing strings in the following order:
 * (skeleton filepath, depth filepath, color filepath)
 * pass in READ or WRITE to get the appropriate filepaths
 */
vector<string> J_StorageDelegate::get_next_filepaths (int read_or_write) {

	stringstream skeleton_filepath;
	stringstream depth_filepath;
	stringstream color_filepath;
	if (read_or_write == READ) {
		skeleton_filepath 	<< in_directory << "/" << current_read_index << ".s";
		depth_filepath 		<< in_directory << "/" << current_read_index << ".d";
		color_filepath 		<< in_directory << "/" << current_read_index << ".c";
	}
	else if (read_or_write == WRITE) {
		skeleton_filepath 	<< out_directory << "/" << current_write_index << ".s";
		depth_filepath 		<< out_directory << "/" << current_write_index << ".d";
		color_filepath 		<< out_directory << "/" << current_write_index << ".c";
	}

	vector<string> next_filepaths;
	next_filepaths.push_back (skeleton_filepath.str());
	next_filepaths.push_back (depth_filepath.str());
	next_filepaths.push_back (color_filepath.str());
	return next_filepaths;
}



/* Function: write_skeleton
 * ------------------------
 * writes the skeleton in a compressed format
 * basically just a matrix
 */
void J_StorageDelegate::write_skeleton (J_Skeleton *skeleton, ofstream &outfile) {

	/*--- skeleton index ---*/
	outfile << current_write_index << endl;

	/*--- skeleton existence ---*/
	if (skeleton == NULL) {
		outfile << "0" << endl;
		return;
	}
	else outfile << "1" << endl;

	/*--- beat ---*/
	if (skeleton->getBeat ()) 	outfile << "1" << endl;
	else 						outfile << "0" << endl;

	/*--- pop ---*/
	if (skeleton->getPop ()) 	outfile << "1" << endl;
	else 						outfile << "0" << endl;

	/*--- joints ---*/
	for (int i=0;i<JSKEL_NUM_OF_JOINTS;i++) {

		J_Joint *current_joint = skeleton->getJoint ((nite::JointType) i);
		nite::Point3f position = current_joint->getPosition ();
		nite::Point3f position_absolute = current_joint->getPositionAbsolute ();

		outfile << position.x << ", " << position.y << ", " << position.z << ", " << position_absolute.x << ", " << position_absolute.y << ", " << position_absolute.z << endl;
	}
}

/* Function: write_frame_ref
 * ------------------------------
 * writes all data contained in the frame_ref to the specified outfile
 */
void J_StorageDelegate::write_frame_ref (J_VideoFrameRef *frame_ref, ofstream &outfile) {
	
	/*### Step 1: write parameters ###*/
	outfile << "resolution_x: "		<< frame_ref->getResolutionX () << endl;
	outfile << "resolution_y: " 	<< frame_ref->getResolutionY () << endl;
	outfile << "crop_origin_x: " 	<< frame_ref->getCropOriginX () << endl;
	outfile << "crop_origin_y: " 	<< frame_ref->getCropOriginY () << endl;
	outfile << "data_size: " 		<< frame_ref->getDataSize () << endl;
	outfile << "frame_index: " 		<< frame_ref->getFrameIndex () << endl;
	outfile << "height: " 			<< frame_ref->getHeight () << endl;
	outfile << "width: " 			<< frame_ref->getWidth () << endl;
	outfile << "stride_in_bytes: " 	<< frame_ref->getStrideInBytes () << endl;
	outfile << "timestamp: " 		<< frame_ref->getTimestamp () << endl;
	outfile << "is_valid: " 		<< frame_ref->isValid () << endl;

	/*### Step 4: write the data ###*/
	outfile << "---------- DATA ----------" << endl;
	outfile.write(frame_ref->getData(), frame_ref->getDataSize());

	return;
}

/* Function: write_frame_ref
 * -------------------------
 * writes the specified J_VideoFrameRef to the .jvid file
 */
void J_StorageDelegate::write (J_Frame *frame) {

	/*### Step 1: sanitize the frame ###*/
	if (!frame->isValid ()) print_error ("J_StorateDelegate::write_frame error", "you passed in an invalid J_Frame");
	J_Skeleton 			*skeleton 		= frame->get_skeleton ();
	J_VideoFrameRef 	*depth_frame 	= frame->get_depth_frame ();
	J_VideoFrameRef 	*color_frame 	= frame->get_color_frame ();


	/*### Step 2: open the outfiles ###*/
	vector<string> filepaths = get_next_filepaths (WRITE);
	string skeleton_filepath = filepaths.at(0);
	string depth_filepath = filepaths.at(1);
	string color_filepath = filepaths.at(2);

	ofstream skeleton_outfile;
	ofstream depth_outfile;
	ofstream color_outfile;

	skeleton_outfile.open (skeleton_filepath.c_str());
	depth_outfile.open (depth_filepath.c_str());
	color_outfile.open (color_filepath.c_str());

	// cout << "		### Skeleton outfile: " << skeleton_filepath.c_str() << endl;
	// cout << "		### Depth outfile: " << depth_filepath.c_str () << endl;
	// cout << "		### Color outfile: " << color_filepath.c_str () << endl;

	/*### Step 3: write the contents to each of them ###*/
	write_skeleton 	(skeleton, skeleton_outfile);
	write_frame_ref (depth_frame, depth_outfile);
	write_frame_ref (color_frame, color_outfile);


	/*### Step 4: cleanup ###*/
	skeleton_outfile.close ();
	depth_outfile.close ();
	color_outfile.close ();

	current_write_index++;

	return;
}







/*########################################################################################################################*/
/*###############################[--- Reading ---] #######################################################################*/
/*########################################################################################################################*/
/* Function: read_skeleton 
 * -----------------------
 * reads in the next skeleton from skeleton_infile;
 * NOTE: the user is responsible for freeing the returned skeleton
 */
J_Skeleton * J_StorageDelegate::read_skeleton (ifstream &infile) {

	J_Skeleton *skeleton = new J_Skeleton ();

	string line;
	int beat_val, pop_val;

	/*--- timestamp ---*/
	int timestamp;
	getline (infile, line);
	sscanf (line.c_str(), "%d", &timestamp);
	skeleton->setTimestamp (timestamp);


	/*--- existence ---*/
	int skeleton_exists;
	getline (infile, line);
	sscanf(line.c_str(), "%d", &skeleton_exists);
	if (skeleton_exists == 1) {
		skeleton->setValid (true);


		/*--- beat ---*/
		int beat;
		getline (infile, line);
		sscanf(line.c_str(), "%d", &beat);
		skeleton->setBeat (beat);

		/*--- pop ---*/
		int pop;
		getline (infile, line);
		sscanf(line.c_str (), "%d", &pop);
		skeleton->setPop (pop);

		/*--- joints ---*/
		for (int i=0;i<JSKEL_NUM_OF_JOINTS;i++) {

			/*--- we will fill these with joint information... ---*/
			nite::Point3f position;
			nite::Point3f position_absolute;
			nite::Quaternion orientation = nite::Quaternion(0, 0, 0, 0);

			getline (infile, line);
			sscanf (	line.c_str(), "%f, %f, %f, %f, %f, %f", 
						&position.x, &position.y, &position.z, 
						&position_absolute.x, &position_absolute.y, &position_absolute.z);

			skeleton->setJoint ((nite::JointType) i, position, position_absolute, orientation);
		}
	}

	return skeleton;
}


/* Function: read_frame
 * --------------------
 * given an infile, this function will read in and return a J_VideoFrameRef.
 * Note: user is responsible for freeing the J_VideoFrameRef!
 */
J_VideoFrameRef * J_StorageDelegate::read_frame_ref (ifstream &infile) {

 	/*--- data to write to ---*/
 	string line;
 	J_VideoFrameRef *frame_ref = new J_VideoFrameRef ();

 	/*--- resolution x/y ---*/
	int resolution_x, resolution_y;
	getline (infile, line);
	sscanf (line.c_str(), "resolution_x: %d", &resolution_x);
	getline (infile, line);	
	sscanf (line.c_str(), "resolution_y: %d", &resolution_y);
	frame_ref->setResolutionX (resolution_x);
	frame_ref->setResolutionY (resolution_y);

	/*--- crop origin x/y ---*/
	int crop_origin_x, crop_origin_y;
	getline (infile, line);
	sscanf (line.c_str(), "crop_origin_x: %d", &crop_origin_x);
	getline (infile, line);	
	sscanf (line.c_str(), "crop_origin_y: %d", &crop_origin_y);
	frame_ref->setCropOriginX (crop_origin_x);
	frame_ref->setCropOriginY (crop_origin_y);

	/*--- data size/frame index ---*/
	int data_size, frame_index;
	getline (infile, line);
	sscanf (line.c_str(), "data_size: %d", &data_size);
	getline (infile, line);	
	sscanf (line.c_str(), "frame_index: %d", &frame_index);
	frame_ref->setDataSize (data_size);
	frame_ref->setFrameIndex (frame_index);

	/*--- width/height ---*/
	int height, width;
	getline (infile, line);
	sscanf (line.c_str(), "height: %d", &height);
	getline (infile, line);	
	sscanf (line.c_str(), "width: %d", &width);
	frame_ref->setHeight (height);
	frame_ref->setWidth (width);

	/*--- stride_in_bytes/timestamp/is_valid---*/
	/*### NOTE: fix this so that you are correctly setting the validity ###*/
	int stride_in_bytes;
	int timestamp;
	char is_valid[80];
	getline (infile, line);
	sscanf (line.c_str(), "stride_in_bytes: %d", &stride_in_bytes);
	getline (infile, line);	
	sscanf (line.c_str(), "timestamp: %d", &timestamp);
	getline (infile, line);	
	sscanf (line.c_str(), "is_valid: %s", is_valid);	

	frame_ref->setStrideInBytes (stride_in_bytes);
	frame_ref->setTimestamp (timestamp);
	frame_ref->setValid (true);

	getline (infile, line);

	/*### Step 3: allocate and write the data ###*/
	frame_ref->allocate_for_data ();
	const char * data = frame_ref->getData ();
	infile.read ((char *) frame_ref->getData (), frame_ref->getDataSize());

	return frame_ref;
 }

/* Function: read
 * --------------
 * returns the next J_Frame, NULL if one doesn't exist
 * Note: user is responsible for freeing the J_Frame at the end of their usage.
 */
J_Frame * J_StorageDelegate::read() {

	/*### Step 1: open the infiles ###*/
	vector<string> filepaths = get_next_filepaths (READ);
	string skeleton_filepath = filepaths.at(0);
	string depth_filepath = filepaths.at(1);
	string color_filepath = filepaths.at(2);

	ifstream skeleton_infile;
	ifstream depth_infile;
	ifstream color_infile;

	skeleton_infile.open (skeleton_filepath.c_str());
	depth_infile.open (depth_filepath.c_str());
	color_infile.open (color_filepath.c_str());


	/*### DEBUG: make sure it is reading in the right files ###*/
	// cout << "		-------------------------------" << endl;
	// cout << "		# Skeleton infile: " << skeleton_filepath.c_str () << endl;
	// cout << "		# depth infile: " << depth_filepath.c_str () << endl;
	// cout << "		# color infile: " << color_filepath.c_str () << endl;
	// if (!skeleton_infile.is_open()) cout << "		(skeleton infile isn't opening)" << endl;
	// if (!color_infile.is_open()) cout << "		(color infile isn't opening)" << endl;
	// if (!depth_infile.is_open()) cout << "		(depthx infile isn't opening)" << endl;	


	/*### Step 2: check if they are open ###*/
	if (!skeleton_infile.is_open () || !depth_infile.is_open () || !color_infile.is_open ()) {
		return NULL;
	}


	/*### Step 3: write the contents to each of them ###*/
	J_Skeleton * 		skeleton 	= read_skeleton 	(skeleton_infile);
	J_VideoFrameRef * 	depth_frame = read_frame_ref 	(depth_infile);
	J_VideoFrameRef * 	color_frame = read_frame_ref 	(color_infile);	


	/*### Step 4: close infiles ###*/
	skeleton_infile.close ();
	depth_infile.close ();
	color_infile.close ();

	/*### Step 4: Construct and return a J_Frame ###*/
	J_Frame * frame = new J_Frame (skeleton, depth_frame, color_frame);
	current_read_index++;
	return frame;
}













