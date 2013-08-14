/* ---------------------------------------------- 	*
 *	File: NI_Recorder.h
 *	-------------------
 *	Class to take care of all recording of skeleton
 * 	and device streams
 *
 *	----------------------------------------------	*/
#ifndef _NI_RECORD_H_
#define _NI_RECORD_H_

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
#include "NI_App.h"
#include "J_DeviceDelegate.h"

/*--- Constants ---*/
#define MAX_FILENAME_LENGTH 150


/*--- Namespaces ---*/
using namespace std;


class NI_Recorder: public NI_App {
private:

	/*--- Self ---*/
	static NI_Recorder *self;

	/*--- Device --*/
	J_DeviceDelegate *device_delegate;

	/*--- Recording Stats ---*/
	bool is_recording;	
	bool isRecording ();
	void start_recording ();
	void stop_recording ();

	/*--- OpenGL Static Functions ---*/
	static void glut_keyboard 		(unsigned char key, int x, int y);
	static void glut_display 		();
	static void glut_idle 			();

	/*--- OpenGL Inialization ---*/
	void 			InitOpenGLHooks	();	
	openni::Status 	InitOpenGL 		(int argc, char **argv);


	/*--- Keyboard/Display for OpenGL ---*/
	void onkey 		(unsigned char key, int x, int y);
	void display 	();

public:


	/*--- Constructor/Destructor ---*/
	NI_Recorder 	(const char* file_path, const char* read_dir, const char* write_dir, int argc, char** argv);
	~NI_Recorder 	();


	/*--- Getting user state, etc ---*/
	void 			updateUserState	(const nite::UserData& user, uint64_t ts);
	openni::Status	Run				();

	/*--- Record ---*/
	void record_jvid_frame (openni::VideoFrameRef *frame);
	void record_skeleton (J_Skeleton *skeleton);
	void record_both (openni::VideoFrameRef *frame, J_Skeleton *skeleton);



};



#endif //_NI_RECORD_H_