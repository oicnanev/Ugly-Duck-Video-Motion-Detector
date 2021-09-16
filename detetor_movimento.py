"""
@python version:
	Python 3.7.1

@plattform:
	Windows

@summary:
	App designed with the pattern Model-View-Controller (MVC)
	https://pt.wikipedia.org/wiki/MVC

	The goal is to detect motion in a sequence of static images. This is 
	acomplished by comparing two in a row, first resizing them to 500 pixels 
	of width, then greying them, after that, create a new image with the absolut
	difference of between the images. At last, with this new image use a dilated
	binary threshold and find the countours. If the area of any countour is 
	bigger than the threshold chosed in the GUI, there is motion 

	Model is composed by MotionDetector, ReadFoto and SaveFoto Classes
	View is composed by a Graphical User Interface (GUI), GUI class and a 
	commented Command Line Interface (CLI), Console script
	Controller is composed by the Controller class who connects Model and View

@author:
	Venâncio 2000644

@contact:
	venancio.nmm@gnr.pt

@organization:
	SDATO - DP - UAF - GNR

@version:
	1.0.0 (2021-09-03):
	- Creation of the MVC model with classes:
		GUI (view)
		MotionDetector (model)
		ReadFoto (model)
		SaveFoto (model)
		Controller (controller)

@TODO:
	Show the first foto to the user so he can choose an area in witch the app
	finds motion 

@since:
	2021-09-03
"""

from tkinter import HORIZONTAL, BOTTOM, FALSE, W, EW, Tk, Frame, Label, Button,\
	Message, StringVar, IntVar,filedialog, ttk, Scale, VERTICAL

from PIL import ImageTk, Image
import cv2 as cv
import numpy as np

import os
import sys
import imutils
from time import sleep
from datetime import datetime

# GUI (View) ===================================================================
class GUI(object):
	"""
	Interface builted in Tkinter()
	"""

	# CONSTRUCTOR --------------------------------------------------------------
	def __init__(self):
		"""
		None -> None

		Builds the Tkinter window and all his elements.
		"""
		# variables ---------------------------------------------------
		self.master = Tk()  # Tk() object
		self.master.title('Ugly Duck Motion Detector - 1.0.0')  # window name
		icons = os.getcwd() + os.sep + "icons" + os.sep  # path to icons
		icon = icons + "nva2.ico"
		self.master.iconbitmap(icon)  # window icon
		self.master.resizable(width=FALSE, height=FALSE)
		self.master.geometry("430x465")

		self.last_dir = "C:/"
		self.input_path = ''
		self.output_path = ''
		
		# image to decorate the window
		self.img = ImageTk.PhotoImage(Image.open(icons + "SpecialUglyDuck.png"))
		
		# to use in frame, message, labels and buttons -----------------
		self.message = StringVar()		
		self.threshold = IntVar()
		self.message.set("Select an input folder                    Threshold = " + str(self.threshold.get()))
		bg = "gray25"
		bg1 = "dark orange"
		fc = "white smoke"
		font = ("Helvetica", "8", "bold")
		font1 = ("Helvetica", "10", "bold")
		text = "Vladimir Software"

		# Frame to suport butons, labels and separators ----------------
		self.f = Frame(self.master, bg=bg)
		self.f.pack_propagate(0)  # don't shrink
		self.f.pack(side=BOTTOM, padx=0, pady=0)

		# Message and Labels -------------------------------------------
		self.l1 = Message(
			self.f, bg=bg1, bd=5, fg=bg, textvariable=self.message,
			font=("Helvetica", "13", "bold italic"), width=500).grid(
			row=0, columnspan=6, sticky=EW, padx=5, pady=5)
		self.l2 = Label(
			self.f, image=self.img, fg=bg).grid(
			row=1, columnspan=5, sticky= W, padx=5, pady=0)
		self.l6 = Label(
			self.f, text=text, font=font1, bg=bg, fg=bg1).grid(
			row=3, column=3, columnspan=3, sticky=EW, pady=5, padx=5)
		self.l3 = Scale(self.f, label='', from_=0, to=100, 
			orient=VERTICAL, length=354, variable=self.threshold,
			command=self.__callback_3).grid(
			row=1, column=5, padx=5, pady=0)

		# Buttons ------------------------------------------------------
		self.b0 = Button(
			self.f, text="INPUT...", command=self.__callback, width=10,
			bg="forest green", fg=fc, font=font).grid(row=3, column=0, padx=5, sticky=W)
		self.b1 = Button(
			self.f, text="OUTPUT...", command=self.__callback_2, width=10,
			bg="DodgerBlue3", fg=fc, font=font).grid(row=3, column=1, padx=5, sticky=W)
		self.b3 = Button(
			self.f, text="Detect", command=self.__callback_4, width=10,
			bg="DodgerBlue4", fg=fc, font=font).grid(row=3, column=2, padx=5, sticky=W)

		# Progressbar --------------------------------------------------
		self.s = ttk.Style()
		# themes: winnative, clam, alt, default, classic, vista, xpnative
		self.s.theme_use('winnative')
		self.s.configure("red.Horizontal.TProgressbar", foreground='green', background='forest green')
		self.pb = ttk.Progressbar(self.f, orient='horizontal', mode='determinate',
								  style="red.Horizontal.TProgressbar")
		self.pb.grid(row=2, column=0, columnspan=6, padx=5, pady=5, sticky=EW)

		# Mainloop -----------------------------------------------------
		self.master.mainloop()

	# PRIVATE METHODS ----------------------------------------------------------
	def __callback(self):  # "Choose input folder" button handler ------
		"""
		None -> None

		Opens a new window (filedialog.askdirectory) to choose the folder where
		the input fotos are
		"""
		title = 'Select the input folder'
		msg = 'Select the output folder     Threshold = ' + str(self.threshold.get())
		self.input_path = filedialog.askdirectory(title=title, initialdir=self.last_dir)
		self.last_dir = self.input_path
		
		if os.listdir(self.input_path) == []:
			msg = 'ERROR: Empty input folder!      Threshold = ' + str(self.threshold.get())
		
		self.message.set(msg)

	def __callback_2(self):  # "Choose output folder" button handler ---
		"""
		None -> None

		Calls the function self.__threat("kmz")
		"""
		sleep(1)
		title = 'Select the output folder           Threshold = ' + str(self.threshold.get())
		msg = 'Choose the threshold and clic Detect  Threshold = ' + str(self.threshold.get())
		self.output_path = filedialog.askdirectory(title=title, initialdir=self.last_dir)
		if os.listdir(self.output_path) != []:
			msg = 'ERROR: The output folder is not empty!     Threshold = ' + str(self.threshold.get())
		
		self.message.set(msg)

	def __callback_3(self, threshold=5):  # Update Threshold value -------
		"""
		None -> None

		Updates the threshold value
		"""
		msg = str(self.message.get())[:str(self.message.get()).rfind('=')]
		self.message.set(msg + '= ' + str(self.threshold.get()))

	def __callback_4(self):  # "Detect movment" button handler ---------------
		"""
		None -> None

		Calls the function self.__detect()
		"""
		sleep(1)
		msg = 'Choose the threshold and clic Detect  Threshold = ' + str(self.threshold.get())
		if self.message.get() != msg:
			self.message.set("First choose input and output folders   Threshold = " + str(self.threshold.get()))
		else:
			self.message.set("Processing...                          Threshold = " + str(self.threshold.get()))
			sleep(1)
			self.__detect()



	def __detect(self):
		"""
		None -> None

		Calls the check_motion() method from the Controller() class
		"""
		ctrl = Controller(self.input_path, self.output_path, self.threshold)
		num_fotos_with_motion_detected = ctrl.check_motion()

		if num_fotos_with_motion_detected > 0:
			self.message.set(f"Done. {num_fotos_with_motion_detected} fotos with motion detected")
		


# CONSOLE (View) ===============================================================
# if __name__ == main():
# 	print('Ugly Duck Motion Detector -  versão 1.0.0')
# 	print()
# 	print('Choose a threshold value, the biger the value, the lesser will be the motion sensibility.')
#     print('A value between 5 and 20 is recommended')

#     input_folder = []
#     while os.listdir(input_folder) == []:
#     	input_folder = input("Write the full path of foto's folder (press 'ENTER' at the end):\n")

#     output_folder = []
#     while os.listdir(output_folder) == []:
#     	output_folder = input("Write the full path of an output empty folder (press 'ENTER' at the end):\n")
	
#     threshold = None
#     while !threshold.isnumeric():
#     	threshold = input('Threshold value: ')

#     control = Controller(input_folder, output_folder, int(threshold))
#     num_fotos_with_motion_detected = control.check_motion()

#     print(f'Motion was detected in {num_fotos_with_motion_detected}')
#     exit()


# MotionDetector (Model) =======================================================
class MotionDetector(object):

	# CONSTRUCTOR --------------------------------------------------------------
	def __init__(self, img0, img1, threshold):
		self.img0 = img0
		self.img1 = img1
		self.threshold = threshold

	# PRIVATE METHODS ----------------------------------------------------------
	def __greying(self, img):
		# recize the image, convert it to grayscale
		img = imutils.resize(img, width=500)
		gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

		return gray


	# PUBLIC METHODS -----------------------------------------------------------
	def is_motion_detected(self):
		gray0 = self.__greying(self.img0)
		gray1 = self.__greying(self.img1)

		# compute the absolute difference between two images
		img_delta = cv.absdiff(gray0, gray1)
		thresh = cv.threshold(img_delta, 25, 255, cv.THRESH_BINARY)[1]
		
		# dilate the thresholded image to fill in holes, then find contours
		# on thresholded image
		thresh = cv.dilate(thresh, None, iterations=2)
		cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,
			cv.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		

		# loop over the contours
		for c in cnts:
			# if the contour is too small, ignore it
			if cv.contourArea(c) < (self.threshold.get() * 100):
				continue
			else:
				return True

		
		return False



# Read (Model) =================================================================
class ReadFoto(object):

	# CONSTRUCTOR --------------------------------------------------------------
	def __init__(self, path):
		self.img = cv.imread(path)

	# PUBLIC METHODS -----------------------------------------------------------
	def get_foto(self):
		return self.img



# Save (Model) =================================================================
class SaveFoto(object):

	# CONSTRUCTOR --------------------------------------------------------------
	def __init__(self, path, img):
		cv.imwrite(path, img)


# Controller (Controler) =======================================================
class Controller(object):

	# CONSTRUCTOR --------------------------------------------------------------
	def __init__(self, input_folder, output_folder, threshold):
		self.input_folder = input_folder
		self.output_folder = output_folder
		self.threshold = threshold

	# PRIVATE METHODS ----------------------------------------------------------
	def __get_input_fotos(self):
		input_imgs = os.listdir(self.input_folder)  # list of strs

		if input_imgs == []:
			return  # Terminar o Controller e voltar para a GUI ou Console

		return input_imgs

	# PUBLIC METHODS -----------------------------------------------------------
	def check_motion(self):
		img0 = None
		img1 = None
		input_imgs = self.__get_input_fotos()
		num_fotos_with_motion_detected = 0
		
		for i in range(len(input_imgs) - 1):
			img0 = ReadFoto(f'{self.input_folder}{os.sep}{input_imgs[i]}').get_foto()
			img1 = ReadFoto(f'{self.input_folder}{os.sep}{input_imgs[i + 1]}').get_foto()

			if MotionDetector(img0, img1, self.threshold).is_motion_detected():
				SaveFoto(f'{self.output_folder}{os.sep}{input_imgs[i + 1]}', img1)
				print(f'{self.output_folder}{os.sep}{input_imgs[i + 1]}')
				num_fotos_with_motion_detected += 1

		print(f'num fotos detected: {num_fotos_with_motion_detected}')
		return num_fotos_with_motion_detected



# INITIALIZATION ===============================================================
if __name__ == '__main__':	
	GUI()