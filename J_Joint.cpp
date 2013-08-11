/* ---------------------------------------------- 	*
 *	File: J_Joint.cpp
 *	--------------------
 *	My personal implementation of nite::SkeletonJoint
 *
 *
 *	----------------------------------------------	*/
#include <iostream>
#include <stdio.h>
#include <stdlib.h>

/*--- NiTE ---*/
#include "NiTE.h"

/*--- OpenCV ---*/


/*--- My Files ---*/
#include "J_Joint.h"



/*########################################################################################################################*/
/*###############################[--- Constructor/Destructors ---]########################################################*/
/*########################################################################################################################*/

/* Constructor: J_Joint (copy constructor) or nite::Point3f/float[3]/nite::Quaternion
 * -----------------------------------------------------------------------------------------
 * creates/initializes a J_Joint from an nite::SkeletonJoint
 * or, one or both of the position and orientation
 */
J_Joint::J_Joint () {
	setPosition 		(nite::Point3f(0, 0, 0));
	setPositionAbsolute (nite::Point3f(0, 0, 0));
	setOrientation 		(nite::Quaternion (0, 0, 0, 0));
}
J_Joint::J_Joint (J_Joint *joint) {
	set(joint);
}
J_Joint::J_Joint (nite::Point3f new_position, nite::Point3f new_position_absolute, nite::Quaternion new_orientation) {
	set(new_position, new_position_absolute, new_orientation);
}



/*########################################################################################################################*/
/*###############################[--- Setters/Getters ---]################################################################*/
/*########################################################################################################################*/
/* Getter: getPositionConfidence
 * -----------------------------
 * not really implemented yet, just returns 1
 */
int J_Joint::getPositionConfidence () {

	return 1;
}


/* Position/Orientation getters
 * ---------------------------
 * gets/sets a particular joint's properties given either a nite::SkeletonJoint
 * or nite::Point3f and/or nite::Quaternion for position/orientation, respectively
 */
nite::Point3f J_Joint::getPosition () {
	return position;
}
nite::Point3f J_Joint::getPositionAbsolute () {
	return position_absolute;
}
nite::Quaternion J_Joint::getOrientation () {
	return orientation;
}


/* Setters
 * -------
 * takes in either a J_Joint, nite::Joint or nite::Point3f new_position and 
 * nite::Quaternion new_orientation
 */
void J_Joint::set (J_Joint *joint) {
	setPosition 		(joint->getPosition ());
	setPositionAbsolute (joint->getPositionAbsolute());
	setOrientation 		(joint->getOrientation());
}
void J_Joint::set (nite::Point3f new_position, nite::Point3f new_position_absolute, nite::Quaternion new_orientation) {
	setPosition 			(new_position);
	setPositionAbsolute		(new_position_absolute);
	setOrientation 			(new_orientation);
}
void J_Joint::setPosition (nite::Point3f new_position) {
	position = new_position;
}
void J_Joint::setPositionAbsolute (nite::Point3f new_position_absolute) {
	position_absolute = new_position_absolute;		
}
void J_Joint::setOrientation (nite::Quaternion new_orientation) {
	orientation = new_orientation;
}


















