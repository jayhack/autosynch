/* ---------------------------------------------- 	*
 *	File: J_StorageDelegate.h
 *	-------------------------
 *	class that takes care of all interactions with storage,
 * 	including reading from files and writing to them
 *
 *	----------------------------------------------	*/
#ifndef _NI_PLAYER_H_
#define _NI_PLAYER_H_

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
#include "VideoFrameRef_Wrapper.h"
#include "J_Frame.h"
#include "J_FilenameManager.h"

/*--- Constants ---*/
#define MAX_FILENAME_LENGTH 150

/*--- Namespaces ---*/
using namespace std;



class J_StorageDelegate {
private:

	/*--- Filenames ---*/
	J_FilenameManager filename_manager;

	/*--- General ---*/
	int current_frame_number;
	int write_recording_stage;		//the recording stage we are writing to
	int read_recording_stage;		//the recording stage we are reading from


	/*--- Skel ---*/	
	ifstream skel_infile;	
	ofstream skel_outfile;

	/*--- Jvid ---*/
	ifstream jvid_infile;			
	ofstream jvid_outfile;			






public:


	/*--- Constructor/Destructor ---*/
	J_StorageDelegate 		();
	J_StorageDelegate 		(const char *selected_file_path, int new_read_recording_stage=RAW, int new_write_recording_stage=MARKED);

	/*--- Misc ---*/
	string get_next_jvid_filepath (int recording_stage);

	/*--- Writing ---*/
	void write_frame (J_Frame *frame);

	/*--- Reading ---*/
	void read_frame (J_Frame *frame);

	/*--- Controls ---*/
	void start_recording ();
	void stop_recording ();
	bool is_recording ();

	/*--- Record ---*/
	void record_jvid_frame (openni::VideoFrameRef *frame);
	void record_skeleton (J_Skeleton *skeleton);
	void record_both (openni::VideoFrameRef *frame, J_Skeleton *skeleton);



};



#endif //_NI_RECORD_H_