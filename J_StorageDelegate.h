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
#include "J_Frame.h"
#include "J_FilenameManager.h"

/*--- Constants ---*/
#define MAX_FILENAME_LENGTH 150

#define RECORD_MODE 0
#define MARK_MODE 1
#define OBSERVE_MARKED_MODE 2
#define OBSERVE_SYNCHRONIZED_MODE 3

#define READ 0
#define WRITE 1

/*--- Namespaces ---*/
using namespace std;



class J_StorageDelegate {
private:

	/*--- Filenames ---*/
	J_FilenameManager filename_manager;

	/*--- General ---*/
	int mode;
	int current_read_index;
	int current_write_index;

	/*--- Skel ---*/	
	string in_directory;
	string out_directory;





public:


	/*--- Constructor/Destructor ---*/
	J_StorageDelegate 		();
	J_StorageDelegate 		(const char *selected_file_path, int selected_mode);
	~J_StorageDelegate 		();

	/*--- Misc ---*/
	vector<string> get_next_filepaths (int read_or_write);

	/*--- Writing ---*/
	void write_skeleton 	(J_Skeleton *skeleton, ofstream &outfile);
	void write_frame_ref 	(J_VideoFrameRef *frame_ref, ofstream &outfile);
	void write 				(J_Frame *frame);

	/*--- Reading ---*/
	J_Skeleton *				read_skeleton 	(ifstream &infile);
	J_VideoFrameRef *			read_frame_ref 	(ifstream &infile);
	J_Frame * 					read 			();

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