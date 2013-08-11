#!/usr/bin/python
import os
import sys

if __name__ == "__main__":

	entire_file = open("unlabelled.txt", "r").read()
	sections = entire_file.split('\n\n')

	outfile = open("outfile.txt", "w")
	
	for i in range(len(sections)):

		current_section = sections[i]
		all_lines = [l for l in current_section.split('\n') if len(l) > 5]

        #--- write the top line ----
		outfile.write ("##### " + str(i) + " #####\n")


		#--- get joint locations ---
		joint_lines = [l for l in all_lines if l[0].isdigit()]
		for line in joint_lines:

			splits = line.split (":")
			
			joint_name = int(splits[0])
			rest = splits[1]

			splits = rest.split(',')
			x = float (splits[0])
			y = float (splits[1])
			z = float (splits[2])

			outfile.write(str(joint_name) + ": (" + str(x) + ", " + str(y) + ", " + str(z) + ")\n")


		#--- get beat ---
		print all_lines
		beat_line = [l for l in all_lines if 'b' in set(l)][0]
		if '1' in set(beat_line): 
			beat = 1
		else:
			beat = 0
		outfile.write ("----- beat: " + str(beat) + " -----\n")
		outfile.write ("----- pop: 0 -----\n\n")

	outfile.close ()
