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
										const char *new_read_stage,				//stage we will read from
										const char *new_write_stage):

										filename_manager (selected_file_path) 
{

	/*### Step 1: fill in read/write recording stages ###*/
	print_status ("Initialization", "Setting paramters");
	current_frame_number = 0;
	if 			(strcmp(new_read_stage, "raw") == 0) 		read_recording_stage = RAW;
	else if 	(strcmp(new_read_stage, "marked") == 0) 	read_recording_stage = MARKED;
	else if 	(strcmp(new_read_stage, "synced") == 0)		read_recording_stage = SYNCED;
	else if 	(strcmp(new_read_stage, "xxx") == 0) 		read_recording_stage = -1;
	else 		print_error ("J_StorageDelegate", "Read stage name not recognized");
	if 			(strcmp(new_write_stage, "raw") == 0) 		write_recording_stage = RAW;
	else if 	(strcmp(new_write_stage, "marked") == 0) 	write_recording_stage = MARKED;
	else if 	(strcmp(new_write_stage, "synced") == 0)	write_recording_stage = SYNCED;
	else if 	(strcmp(new_write_stage, "xxx") == 0)		write_recording_stage = -1;
	else 		print_error ("J_StorageDelegate", "Write stage name not recognized");


	/*### Step 2: open the skeleton reading/writing files ###*/
	print_status ("Initialization", "Opening skeleton file(s)");
	if (read_recording_stage != -1) {
		const char *skeleton_infilename 	= filename_manager.get_filename (read_recording_stage, SKEL_FILE);
		cout << "		Skeleton infile: " << skeleton_infilename << endl;
		skel_infile.open(skeleton_infilename);
	}
	if (write_recording_stage != -1) {
		const char *skeleton_outfilename	= filename_manager.get_filename (write_recording_stage, SKEL_FILE);
		cout << "		Skeleton outfile: " << skeleton_outfilename << endl;
		skel_outfile.open (skeleton_outfilename);	
	}

}
J_StorageDelegate::~J_StorageDelegate () {

	/*### Step 1: close all files we were reading from/writing to ###*/
	skel_infile.close ();
	skel_outfile.close ();

}





/*########################################################################################################################*/
/*###############################[--- Writing ---] ###############################################################*/
/*########################################################################################################################*/
/* Function: get_next_(depth|color)_filepath
 * --------------------------------
 * determines where the next (depth|color) file should go and returns a string
 * that is its entire filepath
 */
string J_StorageDelegate::get_next_depth_filepath (int recording_stage) {

	string jvid_directory;
	jvid_directory.assign(filename_manager.get_filename (recording_stage, JVID_FILE));

	stringstream next_filepath;
	next_filepath << jvid_directory << "/" << current_frame_number << ".d";
	return next_filepath.str();
}
string J_StorageDelegate::get_next_color_filepath (int recording_stage) {

	string jvid_directory;
	jvid_directory.assign(filename_manager.get_filename (recording_stage, JVID_FILE));

	stringstream next_filepath;
	next_filepath << jvid_directory << "/" << current_frame_number << ".c";
	return next_filepath.str();
}

/* Function: write_skeleton
 * ------------------------
 * writes the specified J_Skeleton to the .skel outfile.
 */
void J_StorageDelegate::write_skeleton (J_Skeleton * skeleton) {

	/*### Step 1: Skeleton id ###*/
	skel_outfile << "##### " << current_frame_number << " #####" << endl;

	/*### Step 2: if no skeleton exists, then get out of there ###*/
	if (skeleton == NULL) {
		skel_outfile << "----- exists: 0 -----" << endl << endl;
		return;
	}
	else {
		skel_outfile << "----- exists: 1 -----" << endl;

		/*### Step 2: joints ###*/
		for (int i=0;i<JSKEL_NUM_OF_JOINTS;i++) {
		
			J_Joint *current_joint = skeleton->getJoint ((nite::JointType) i);

			nite::Point3f position = current_joint->getPosition ();
			nite::Point3f position_absolute = current_joint->getPositionAbsolute ();

			skel_outfile << i << ": (" << position.x << ", " << position.y << ", " << position.z << ") | ";
			skel_outfile << 		"( " << position_absolute.x << ", " << position_absolute.y << ", " << position_absolute.z << ")" << endl;

		}

		bool beat = skeleton->getBeat ();
		bool pop = skeleton->getPop ();

		/*### Step 3: beat ###*/
		if (beat) 	skel_outfile << "----- beat: 1 -----" << endl;
		else 		skel_outfile << "----- beat: 0 -----" << endl;

		/*### Step 4: pop ###*/
		if (pop) 	skel_outfile << "----- pop: 1 -----" << endl;
		else 		skel_outfile << "----- pop: 0 -----" << endl;

		/*### Step 5: trailing newline ###*/
		skel_outfile << endl;
	}
}


/* Function: write_frame
 * ------------------------------
 * writes all data that is proprietary of all J_VideoFrameRefs to the specified
 * outfile
 */
void J_StorageDelegate::write_frame (J_VideoFrameRef *frame_ref, ofstream &outfile) {
	
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
void J_StorageDelegate::write_frames (J_VideoFrameRef *depth_frame, J_VideoFrameRef *color_frame) {

	/*### Step 1: open the outfiles ###*/
	/*### NOTE: change this from just 'RAW' later on ###*/
	string depth_filename = get_next_depth_filepath (write_recording_stage); 
	string color_filename = get_next_color_filepath (write_recording_stage);
	ofstream depth_outfile;
	ofstream color_outfile;
	depth_outfile.open (depth_filename.c_str());
	color_outfile.open (color_filename.c_str());

	cout << "		### Depth frame outfile: " << depth_filename.c_str () << endl;
	cout << "		### Color frame outfile: " << color_filename.c_str () << endl;

	/*### Step 2: write the contents to each of them ###*/
	write_frame (depth_frame, depth_outfile);
	write_frame (color_frame, color_outfile);


	/*### Step 3: cleanup ###*/
	depth_outfile.close ();
	color_outfile.close ();

	return;
}




/* Function: write_frame 
 * ---------------------
 * given a pointer to a J_Frame object, this function will write it
 * to a file
 */
void J_StorageDelegate::write (J_Frame *frame) {

	/*### Step 0: assert that the frame is in fact valid ###*/
	if (!frame->isValid ()) {
		print_error ("J_StorateDelegate::write_frame error", "you passed in an invalid J_Frame");
	}

 	/*### Step 1: write the skeleton ###*/
 	// print_status ("Storage", "Writing J_Skeleton");
 	write_skeleton (frame->get_skeleton());

 	/*### Step 2: write the frame_ref ###*/
 	// print_status ("Storage", "Writing J_VideoFrameRef");
 	write_frames (frame->get_depth_frame(), frame->get_color_frame());

 	/*### Step 3: increment the frame number that we are currently on ###*/
 	current_frame_number++;
 }






/*########################################################################################################################*/
/*###############################[--- Reading ---] #######################################################################*/
/*########################################################################################################################*/
/* Function: read_skeleton 
 * -----------------------
 * reads in the next skeleton from skel_infile;
 * NOTE: the user is responsible for freeing the returned skeleton
 */
J_Skeleton * J_StorageDelegate::read_skeleton () {

	J_Skeleton *skeleton = new J_Skeleton ();

	string line;
	int beat_val, pop_val;

	/*### Step 1: timestamp ###*/
	int timestamp;
	getline (skel_infile, line);
	sscanf (line.c_str(), "##### %d #####", &timestamp);
	skeleton->setTimestamp (timestamp);
	// cout << "	- timestamp " << timestamp << endl;


	/*### Step 2: see if it exists or not ###*/
	int skeleton_exists;
	getline (skel_infile, line);
	sscanf(line.c_str(), "----- exists: %d -----", &skeleton_exists);
	// cout << "	- exists " << skeleton_exists << endl;


	/*### Step 3: in case it does, fill in all the other information ###*/
	if (skeleton_exists == 1) {

		skeleton->setValid (true);

		/*### Step 2: joints ###*/
		for (int i=0;i<JSKEL_NUM_OF_JOINTS;i++) {

			/*--- we will fill these with joint information... ---*/
			nite::Point3f position;
			nite::Point3f position_absolute;
			nite::Quaternion orientation = nite::Quaternion(0, 0, 0, 0);

			getline (skel_infile, line);

			int joint_name;

			sscanf (	line.c_str(), "%d: (%f, %f, %f) | (%f, %f, %f)", 
						&joint_name, 
						&position.x, &position.y, &position.z, 
						&position_absolute.x, &position_absolute.y, &position_absolute.z);

			skeleton->setJoint ((nite::JointType) joint_name, position, position_absolute, orientation);
		}

		/*### Step 3: beat existence ###*/
		getline(skel_infile, line);
		sscanf(line.c_str(), "----- beat: %d -----", &beat_val);
		skeleton->setBeat ((beat_val == 1));
		// cout << "	- beat " << beat_val << endl;

		/*### Step 4: pop existence ###*/
		getline (skel_infile, line);
		sscanf (line.c_str(), "----- pop: %d -----", &pop_val);
		skeleton->setPop ((pop_val == 1));
		// cout << "	- pop " << pop_val << endl;

	}

	/*### Step 5: get final line ###*/
	getline(skel_infile, line);

	return skeleton;
}


/* Function: read_frame
 * --------------------
 * given an infile, this function will read in and return a J_VideoFrameRef.
 * Note: user is responsible for freeing the J_VideoFrameRef!
 */
J_VideoFrameRef * J_StorageDelegate::read_frame (ifstream &infile) {

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

/* Function: read_frames
 * -------------------------
 * reads in the next depth/color frames and returns pointers to them in an array.
 * NOTE: the user is responsible for freeing all memory created by
 * calling this function (namely the J_VideoFrameRef returned)
 */
vector <J_VideoFrameRef*> J_StorageDelegate::read_frames() {

	/*### Step 1: open the infiles ###*/
	string depth_filename = get_next_depth_filepath (read_recording_stage); 
	string color_filename = get_next_color_filepath (read_recording_stage);
	ifstream depth_infile;
	ifstream color_infile;
	depth_infile.open (depth_filename.c_str());
	color_infile.open (color_filename.c_str());

	/*### Step 2: read into each of the frames ###*/
	J_VideoFrameRef * depth_frame;
	J_VideoFrameRef * color_frame;
	depth_frame = read_frame (depth_infile);
	color_frame = read_frame (color_infile);

	/*### Step 3: close the infiles ###*/
	depth_infile.close ();
	color_infile.close ();

	/*### Step 4: return the array of J_VideoFrameRefs ###*/
	std::vector <J_VideoFrameRef*> frame_refs;
	frame_refs.push_back (depth_frame);
	frame_refs.push_back (color_frame);
	return frame_refs;
}



/* Function: read_frame 
 * ---------------------
 * given a pointer to a J_Frame object, this function will write it
 * to a file
 */
J_Frame * J_StorageDelegate::read () {

	/*### Step 1: read in the skeleton ###*/
	J_Skeleton *skeleton = read_skeleton ();

	/*### Step 2: get the frame_refs ###*/
	vector <J_VideoFrameRef*> frame_refs = read_frames ();
	J_VideoFrameRef* depth_frame = frame_refs.at (0);
	J_VideoFrameRef* color_frame = frame_refs.at (1);	


	/*### Step 3: make the frame and return it ###*/
	J_Frame * frame = new J_Frame (skeleton, depth_frame, color_frame);

	/*### Step 4: update the current frame number ###*/
	current_frame_number++;

	return frame;
 }












