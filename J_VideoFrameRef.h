/* ---------------------------------------------- 	*
 *	File: J_VideoFrameRef.h
 *	-------------------------
 *	my own implementation of VideoFrameRef that is mutable
 * 	and that I will be able to write 
 *	----------------------------------------------	*/
#ifndef _J_VID_REF_H_
#define _J_VID_REF_H_

/*--- Standard ---*/
#include <stdlib.h>
#include <stdio.h>

/*--- NiTE ---*/
#include "NiTE.h"


class J_VideoFrameRef {
private:

	/*--- parameters ---*/
	openni::VideoMode video_mode;
	int crop_origin_x;
	int crop_origin_y;
	bool cropping_enabled;
	int data_size;
	int frame_index;
	int height, width;
	int stride_in_bytes;
	uint64_t timestamp;
	bool is_valid;


	/*--- data ---*/
	char *data;


public:

	/*--- Constructors ---*/
	J_VideoFrameRef ();
	J_VideoFrameRef (openni::VideoFrameRef *video_frame_ref);
	~J_VideoFrameRef ();

	/*--- Getting Data ---*/
	const char *		getData ();

	/*--- Getting Paramters ---*/
	const openni::VideoMode & 	getVideoMode ();
	int 						getCropOriginX ();
	int 						getCropOriginY ();
	bool 						getCroppingEnabled ();
	int 						getDataSize (); 
	int 						getFrameIndex ();
	int 						getHeight ();
	int 						getWidth ();
	int 						getStrideInBytes ();
	uint64_t 					getTimestamp ();
	bool 						isValid ();


};

#endif