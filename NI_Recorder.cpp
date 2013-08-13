/* ---------------------------------------------- 	*
 *	File: NI_Recorder.h
 *	-------------------
 *	Class to take care of all recording of skeleton
 * 	and device streams
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
#include "NI_Recorder.h"

/*--- Namespaces ---*/
using namespace std;

/*--- Initialize Static Elements ---*/
NI_Recorder* NI_Recorder::self = NULL;



/*########################################################################################################################*/
/*###############################[--- Constructor/Initialization/Destructor ---] #########################################*/
/*########################################################################################################################*/
/* Function: Constructor
 * ---------------------
 * initializes all forms of recording, though does not start writing to output
 */
NI_Recorder::NI_Recorder (const char* file_path, int argc, char** argv) {
	self = this;

	/*### Step 1: initialize the APIs ###*/
	print_status ("Initialization (Recorder)", "Initializing APIs");
	initialize_APIs (argc, argv);

	/*### Step 2: initialize opengl ###*/
	print_status ("Initialization (Recorder)", "Initializing OpenGL");
	InitOpenGL (argc, argv);

	/*### Step 2: initialize the device/user tracker ###*/
	print_status ("Initialization (Recorder)", "Creating Device Delegate");
	device_delegate = new J_DeviceDelegate ();

	/*### Step 3: initialize the storage delegate ###*/
	print_status ("Initialization (Recorder)", "Creating Storage Delegate");
	storage_delegate = new J_StorageDelegate (file_path, MARKED, RAW);

	/*### Step 3: initialize recording to false ###*/
	stop_recording ();
}

/* Function: Destructor
 * --------------------
 * stops recording and closes all files
 */
NI_Recorder::~NI_Recorder () {
		
	/*### Step 1: free all memory allocatd for the device delegate ###*/
	print_status ("Finalization (Recorder)", "Deleting device delegate");
	delete device_delegate;

	/*### Step 2: free all memory allocatd for the device delegate ###*/
	print_status ("Finalization (Recorder)", "Deleting storage delegate");
	delete storage_delegate;

}




/*########################################################################################################################*/
/*###############################[--- OpenGL Initialization ---]##########################################################*/
/*########################################################################################################################*/
/* Function: InitOpenGLHooks
 * -------------------------
 * sets up OpenGL hooks 
 */
void NI_Recorder::InitOpenGLHooks () {
	glutKeyboardFunc 	(glut_keyboard);
	glutDisplayFunc		(glut_display);
	glutIdleFunc		(glut_idle);
}

/* Function: InitOpenGL 
 * --------------------
 * initializes OpenGL
 */
openni::Status NI_Recorder::InitOpenGL (int argc, char **argv) {

	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH);
	glutInitWindowSize(GL_WIN_SIZE_X, GL_WIN_SIZE_Y);
	glutCreateWindow ("Display");
	
	/*--- uncomment for full screen ---*/
	// 	glutFullScreen();

	glutSetCursor(GLUT_CURSOR_NONE);
	InitOpenGLHooks();
	glDisable(GL_DEPTH_TEST);
	glEnable(GL_TEXTURE_2D);
	glEnableClientState(GL_VERTEX_ARRAY);
	glDisableClientState(GL_COLOR_ARRAY);

	return openni::STATUS_OK;
}


// ########################################################################################################################
// /*#####################[--- OPENGL INTERFACE FUNCTIONS ---]###############################################################*/
// /*########################################################################################################################*/
// /* Functions: glut(Idle|Display|Keyboard)
//  * --------------------------------------
//  * these functions serve as the interface to OpenGL;
//  * they are static (?)
//  */
void NI_Recorder::glut_idle() {
	
	glutPostRedisplay();
}
void NI_Recorder::glut_display() {

	NI_Recorder::self->display();
}
void NI_Recorder::glut_keyboard(unsigned char key, int x, int y) {
	
	NI_Recorder::self->onkey(key, x, y);
}



/*########################################################################################################################*/
/*###############################[--- Recording Manipulation ---] ########################################################*/
/*########################################################################################################################*/
/* Function: is_recording
 * ----------------------
 * returns wether we are recording or not
 */
bool NI_Recorder::isRecording () {
	return is_recording;
}

/* Function: (start|stop)_recording
 * -------------------------
 * starts/stops the recording
 */
void NI_Recorder::start_recording () {
	is_recording = true;
}
void NI_Recorder::stop_recording () {
	is_recording = false;
}






/*########################################################################################################################*/
/*###############################[--- OpenGL Interface ---] ##############################################################*/
/*########################################################################################################################*/
/* Function: onkey
 * ---------------
 * callback function for handling keyboard events.
 * here, it mainly controls wether recording is active or not, 
 * also quitting the application.
 */
void NI_Recorder::onkey (unsigned char key, int x, int y) {
	
	switch (key)
	{
		/*### ESC: exits application ###*/
		case 27:	
			// Finalize();
			exit (1);

		/*### B: start recording ###*/
		case 'r':
			print_status ("Main operation", "Started recording");
			start_recording ();
			break;	

		/*### P: stop recording ###*/
		case 's':
			print_status ("Main operation", "Stopped recording");
			stop_recording ();
			break;
	}
}

void NI_Recorder::display () {

	/*### Step 1: get the next J_Frame ###*/
	// print_status ("Display", "Getting frame");
	J_Frame *frame = device_delegate->readFrame ();

	/*### Step 2: draw it to the screen ###*/
	// print_status ("Display", "Drawing frame");
	drawer.draw_frame (frame);

	/*### Step 3: record it ###*/
	if (isRecording ()) {
		storage_delegate->write (frame);
	} 	 

	/*### Step 3: free all memory dedicated to the frame ###*/
	delete frame;
}

/* Function: Run
 * -------------
 * engages in the main loop, does not return.
 */
openni::Status NI_Recorder::Run() {	
	glutMainLoop();
	return openni::STATUS_OK;
}













