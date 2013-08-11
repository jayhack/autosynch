/* ---------------------------------------------- 	*
 *	File: J_VideoFrameRef.cpp
 *	-------------------------
 *	my own implementation of VideoFrameRef that is mutable
 * 	and that I will be able to write 
 *	----------------------------------------------	*/
/*--- Standard ---*/
#include <iostream>
#include <stdlib.h>
#include <stdio.h>

/*--- NiTE ---*/
#include "NiTE.h"

/*--- My Files ---*/
#include "J_VideoFrameRef.h"

/*--- namespaces ---*/
using namespace std;


/*########################################################################################################################*/
/*###############################[--- Construction/Initialization/Destruction ---] #######################################*/
/*########################################################################################################################*/
/* Function: constructor
 * ---------------------
 * given a pointer to an openni::VideoFrameRef, the constructor will 
 * make a deep copy of it and store all information locally.
 */
J_VideoFrameRef::J_VideoFrameRef () {}
J_VideoFrameRef::J_VideoFrameRef (openni::VideoFrameRef *video_frame_ref) {

	/*### Step 1: get parameters ###*/
	video_mode 			= video_frame_ref->getVideoMode ();
	crop_origin_x 		= video_frame_ref->getCropOriginX ();
	crop_origin_y 		= video_frame_ref->getCropOriginY ();
	cropping_enabled	= video_frame_ref->getCroppingEnabled ();
	data_size			= video_frame_ref->getDataSize ();
	frame_index			= video_frame_ref->getFrameIndex ();
	height 				= video_frame_ref->getHeight ();
	width				= video_frame_ref->getWidth ();
	stride_in_bytes		= video_frame_ref->getStrideInBytes ();
	timestamp			= video_frame_ref->getTimestamp ();
	is_valid 			= video_frame_ref->isValid ();

	/*### Step 2: make a deep copy of the data itself ###*/
	data = new char [data_size];
	memcpy (data, video_frame_ref->getData (), data_size);
}
/* Function: destructor
 * --------------------
 * all this has to do is free the memory dedicated to storing the original frame
 */
J_VideoFrameRef::~J_VideoFrameRef () {
	delete data;
}


/*########################################################################################################################*/
/*###############################[--- Getting Parameters/Data ---] #######################################################*/
/*########################################################################################################################*/
int 				J_VideoFrameRef::getCropOriginX () 			{ 	return crop_origin_x; }
int 				J_VideoFrameRef::getCropOriginY () 			{	return crop_origin_y; }
bool 				J_VideoFrameRef::getCroppingEnabled () 		{	return cropping_enabled; }
int 				J_VideoFrameRef::getDataSize () 			{ 	return data_size; }
int 				J_VideoFrameRef::getFrameIndex ()			{ 	return frame_index; }
int 				J_VideoFrameRef::getHeight ()				{ 	return height; }
int 				J_VideoFrameRef::getWidth ()				{ 	return width; }
int 				J_VideoFrameRef::getStrideInBytes ()		{ 	return stride_in_bytes; }
uint64_t 			J_VideoFrameRef::getTimestamp ()			{ 	return timestamp; }
bool 				J_VideoFrameRef::isValid ()					{ 	return is_valid; }
const openni::VideoMode & 	J_VideoFrameRef::getVideoMode ()	{	return video_mode; }


const char * 		J_VideoFrameRef::getData 	()				{ return data; }




