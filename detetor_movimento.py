# Criar janela com botão para escolher a pasta das fotos, uma pasta de destino das fotos onde foi detetado movimento e a sensibilidade da deteção (View)
from tkinter import HORIZONTAL, BOTTOM, CENTER, FALSE, ALL, E, W, EW, SEPARATOR,\
    Tk, Frame, Label, Button, Message, Menu, Canvas, Toplevel, StringVar, BooleanVar, \
    filedialog, ttk, SUNKEN, TOP, TRUE, BOTH, LEFT, Text, NORMAL, DISABLED

from PIL import ImageTk, Image

import os
import sys
import logging
from time import sleep

class Xls2kml(object):
	"""
	Interface builted in Tkinter()
	"""

	def __init__(self):
		"""
		None -> None

		Builds the Tkinter window and all his elements.
		"""
		# variables ----------------------------------------------------
		self.master = Tk()  # Tk() object
		self.master.title('Ugly Duck Motion Detector - 1.0.0')  # window name
		icons = os.getcwd() + os.sep + "icons" + os.sep  # path to icons
		#foto_folder = os.getcwd() + os.sep + "fotos"  # path to fotos
		icon = icons + "nva2.ico"
		self.master.iconbitmap(icon)  # window icon
		self.master.resizable(width=FALSE, height=FALSE)
		self.master.geometry("548x314")

		self.file_name = ""  # the name of the EXEL file
		self.last_dir = "C:/"
		
		# image to decorate the window
		self.img = ImageTk.PhotoImage(Image.open(icons + "SpecialUnglyDuck.png"))
		
		# to use in frame, message, labels and buttons -----------------
		self.message = StringVar()
		self.message.set("\nSelecciona um ficheiro EXCEL")
		bg = "gray25"
		bg1 = "dark orange"
		fc = "white smoke"
		font = ("Helvetica", "8", "bold")
		font1 = ("Helvetica", "10", "bold")
		text0 = " ----- "
		text1 = " Boris & Vladimir Software "
		text = text0 + text1 + text0

		# Menu ---------------------------------------------------------
		self.menu = Menu(self.master)
		self.master.config(menu=self.menu)
		filemenu = Menu(self.menu)
		self.menu.add_cascade(label="Ficheiro", menu=filemenu)
		filemenu.add_command(label="Sair", command=self.__callback_3)
		filemenu.add_command(label='Pasta Fotos', command=lambda: (self.__open_folder(foto_folder)))

		self.openGE = BooleanVar()
		self.openGE.set(False)
		optionsmenu = Menu(self.menu)
		self.menu.add_cascade(label="Opções", menu=optionsmenu)
		optionsmenu.add_checkbutton(label="Não abrir o Google Earth",
									onvalue=True, offvalue=False, variable=self.openGE)
		docsmenu = Menu(self.menu)
		docs = ["docs\manual.pdf", "docs\icons.pdf", "docs\colors.pdf",
				"docs\GPS.xlsx", "docs\GPS.kmz", "docs\Celulas.xlsx",
				"docs\Celulas.kmz", "docs\Foto.xlsx", "docs\Foto.kmz",
				"docs\Quadrado.xls", "docs\Quadrado.kmz"]
		self.menu.add_cascade(label="Documentação", menu=docsmenu)
		docsmenu.add_command(label="Manual", command=lambda: (self.__open_file(docs[0])))
		docsmenu.add_command(label="Ícones", command=lambda: (self.__open_file(docs[1])))
		docsmenu.add_command(label="Cores", command=lambda: (self.__open_file(docs[2])))

		exemplemenu = Menu(docsmenu)
		docsmenu.add_cascade(label="Exemplos", menu=exemplemenu)

		gpsmenu = Menu(exemplemenu)
		exemplemenu.add_cascade(label="Trajetos", menu=gpsmenu)
		gpsmenu.add_command(label="Excel", command=lambda: (self.__open_file(docs[3])))
		gpsmenu.add_command(label="Google Earth", command=lambda: (self.__open_file(docs[4])))

		cellmenu = Menu(exemplemenu)
		exemplemenu.add_cascade(label="Células Telefónicas", menu=cellmenu)
		cellmenu.add_command(label="Excel", command=lambda: (self.__open_file(docs[5])))
		cellmenu.add_command(label="Google Earth", command=lambda: (self.__open_file(docs[6])))

		fotomenu = Menu(exemplemenu)
		exemplemenu.add_cascade(label="Fotos", menu=fotomenu)
		fotomenu.add_command(label="Excel", command=lambda: (self.__open_file(docs[7])))
		fotomenu.add_command(label="Google Earth", command=lambda: (self.__open_file(docs[8])))

		squaremenu = Menu(exemplemenu)
		exemplemenu.add_cascade(label="Quadrado", menu=squaremenu)
		squaremenu.add_command(label="Excel", command=lambda: (self.__open_file(docs[9])))
		squaremenu.add_command(label="Google Earth", command=lambda: (self.__open_file(docs[10])))

		helpmenu = Menu(self.menu)
		self.menu.add_cascade(label='Ajuda', menu=helpmenu)
		helpmenu.add_command(label="Sobre", command=self.__about)
		helpmenu.add_command(label="Ver erros", command=lambda: (self.__open_file("erros.log")))

		# Frame to suport butons, labels and separators ----------------
		self.f = Frame(self.master, bg=bg)
		self.f.pack_propagate(0)  # don't shrink
		self.f.pack(side=BOTTOM, padx=0, pady=0)

		# Message and Labels -------------------------------------------
		self.l1 = Message(
			self.f, bg=bg1, bd=5, fg=bg, textvariable=self.message,
			font=("Helvetica", "13", "bold italic"), width=500).grid(
			row=0, columnspan=6, sticky=EW, padx=5, pady=5)
#		self.l2 = Label(
#			self.f, image=self.img, fg=bg).grid(
#			row=1, columnspan=6, padx=5, pady=2)
		self.l6 = Label(
			self.f, text=text, font=font1, bg=bg, fg=bg1).grid(
			row=3, column=3, columnspan=2, sticky=EW, pady=5)

		# Buttons ------------------------------------------------------
		self.b0 = Button(
			self.f, text="Abrir EXCEL...", command=self.__callback, width=10,
			bg="forest green", fg=fc, font=font).grid(row=3, column=0, padx=5, sticky=W)
		self.b1 = Button(
			self.f, text="Gravar KMZ", command=self.__callback_2, width=10,
			bg="DodgerBlue3", fg=fc, font=font).grid(row=3, column=1, padx=5, sticky=W)
		self.b2 = Button(
			self.f, text="Sair", command=self.__callback_3, width=10,
			bg="orange red", fg=fc, font=font).grid(row=3, column=5, sticky=E, padx=5)
		self.b3 = Button(
			self.f, text="Gravar MKD", command=self.__callback_4, width=10,
			bg="DodgerBlue4", fg=fc, font=font).grid(row=3, column=2, padx=5, sticky=W)

		# Progressbar --------------------------------------------------
		self.s = ttk.Style()
		# themes: winnative, clam, alt, default, classic, vista, xpnative
#		self.s.theme_use('winnative')
		self.s.configure("red.Horizontal.TProgressbar", foreground='green', background='forest green')
		self.pb = ttk.Progressbar(self.f, orient='horizontal', mode='determinate',
								  style="red.Horizontal.TProgressbar")
		self.pb.grid(row=2, column=0, columnspan=6, padx=5, pady=5, sticky=EW)

		# Mainloop -----------------------------------------------------
		self.master.mainloop()

	def __callback(self):  # "Abrir EXEL..." button handler ------------
		"""
		None -> None

		Opens a new window (filedialog.askopenfilename) to choose the
		EXCEL file that is necessary to make the KMZ file.
		"""
		title = 'Selecciona um ficheiro Excel'
		msg = 'Ficheiro EXCEL carregado em memória\nTransforma-o em KMZ/MKD'
		self.file_name = filedialog.askopenfilename(title=title, initialdir=self.last_dir)
		self.last_dir = self.file_name[:self.file_name.rfind('/')]

		if self.file_name[self.file_name.rfind('.') + 1:] != 'xls' and \
				self.file_name[self.file_name.rfind('.') + 1:] != 'xlsx':
			msg = self.file_name + ' não é um ficheiro Excel válido!'
		self.message.set(msg)

	def __callback_2(self):  # "Gravar KMZ" button handler ---------------
		"""
		None -> None

		Calls the function self.__threat("kmz")
		"""
		sleep(1)
		msg = 'Ficheiro EXCEL carregado em memória\nTransforma-o em KMZ/MKD'
		if self.message.get() != msg:
			self.message.set("\nEscolhe um ficheiro Excel primeiro")
		else:
			self.message.set("\nA processar...")
			self.master.update_idletasks()
			sleep(1)
			self.__threads("kmz")

	def __callback_3(self):  # "Sair" button handler ---------------------
		"""
		None -> None

		Kills the window
		"""
		self.master.destroy()

	def __callback_4(self):  # "Gravar MKD" button handler ---------------
		"""
		None -> None

		Calls the function self.__threads("mkd")
		"""
		sleep(1)
		msg = 'Ficheiro EXCEL carregado em memória\nTransforma-o em KMZ/MKD'
		if self.message.get() != msg:
			self.message.set("\nEscolhe um ficheiro Excel primeiro")
		else:
			self.message.set("\nA processar...")
			self.master.update_idletasks()
			sleep(1)
			self.__threads("mkd")

	def __threads(self, mkd_or_kmz):
		"""
		str -> MyTread() objects

		mkd_or_kmz - a string to choose between kmz or mdk

		Creates two threads to run at the same time the functions:
		self.__create_kmz() or self.__crerate_mkd()
		self.__progressbar()
		"""
		if mkd_or_kmz == "mkd":
			funcs = [self.__create_mkd, self.__progressbar]
		else:
			funcs = [self.__create_kmz, self.__progressbar]
		threads = []
		nthreads = list(range(len(funcs)))

		for i in nthreads:
			t = MyThread(funcs[i], (), funcs[i].__name__)
			threads.append(t)

		for i in nthreads:
			threads[i].start()

	def __create_mkd(self):
		"""
		None -> None

		Calls the excel_to_mkd() attribute from the MotherControl() class
		"""
		mkd = MotherControl(
			self.file_name, self.original_working_dir).excel_to_mkd()
		if type(mkd) == str:
			self.message.set(mkd)
			self.pb.stop()
			self.master.update_idletasks()
		else:
			sleep(2)
			self.pb.stop()
			self.master.update_idletasks()
		self.message.set("\nMKD gravado com sucesso.")
		sleep(2)
		self.master.update_idletasks()

	def __create_kmz(self):
		"""
		None -> None

		Calls the excel_to_kml() atribute from MotherControl() class
		And when it returns, calls self.__open_Google_Earth()
		"""
		kmz = MotherControl(
			self.file_name, self.original_working_dir).excel_to_kml()
		if type(kmz) == str:
			self.message.set(kmz)
			self.pb.stop()
			self.master.update_idletasks()
		else:
			sleep(2)
			self.pb.stop()
			self.master.update_idletasks()
			self.__open_Google_Earth()

	def __open_Google_Earth(self):
		"""
		None -> None

		Opens the made KMZ file in Google Earth
		"""
		sleep(1)
		self.master.update_idletasks()
		msg = "KMZ gravado com sucesso.\nA abrir o Google Earth..."
		if not self.openGE.get():
			self.message.set(msg)
		else:
			self.message.set("\nKMZ gravado com sucesso.\n")
		sleep(2)
		self.master.update_idletasks()
		path = self.file_name[:self.file_name.rindex('/')]
		path_1 = self.file_name[self.file_name.rindex('/') +
								1:self.file_name.rfind('.')]
		kmzs = [x for x in os.listdir(path) if x[-4:] == '.kmz' and x[:-12] == path_1]
		kmzs.sort()
		try:
			if not self.openGE.get():
				os.startfile(path + os.sep + kmzs[-1])
				sleep(2)
			self.message.set("\nSelecciona um ficheiro EXCEL")
		except:
			msg = "Instale o Google Earth\nhttp://www.google.com/earth/"
			self.message.set(msg)
			self.master.update_idletasks()

	def __progressbar(self, ratio=0):
		"""
		None -> None

		Starts the progressbar in the window
		"""
		self.pb.start(50)

	def __about(self):
		"""
		None -> None

		Associated with the Help Menu.
		Creates a new window with the "About" information
		"""
		appversion = "2.0.4"
		appname = "EXCEL to KML Transformer"
		copyright = 14 * ' ' + '(c) 2013' + 12 * ' ' + \
					'SDATO - DP - UAF - GNR\n' + 34 * ' ' + "No Rights Reserved"
		licence = 18 * ' ' + 'http://opensource.org/licenses/GPL-3.0\n'
		contactname = "Nuno Venâncio"
		contactphone = "(00351) 969 564 906"
		contactemail = "venancio.gnr@gmail.com"

		message = "Version: " + appversion + 5 * "\n"
		message0 = "Copyleft: " + copyright + "\n" + "Licença: " + licence
		message1 = contactname + '\n' + contactphone + '\n' + contactemail

		icons = os.getcwd() + os.sep + "icons" + os.sep  # path to icons
		icon = icons + "compass.ico"

		tl = Toplevel(self.master)
		tl.configure(borderwidth=5)
		tl.title("Sobre...")
		tl.iconbitmap(icon)
		tl.resizable(width=FALSE, height=FALSE)
		f1 = Frame(tl, borderwidth=2, relief=SUNKEN, bg="gray25")
		f1.pack(side=TOP, expand=TRUE, fill=BOTH)

		l0 = Label(f1, text=appname, fg="white", bg="gray25", font=('courier', 16, 'bold'))
		l0.grid(row=0, column=0, sticky=W, padx=10, pady=5)
		l1 = Label(f1, text=message, justify=CENTER, fg="white", bg="gray25")
		l1.grid(row=2, column=0, sticky=E, columnspan=3, padx=10, pady=0)
		l2 = Label(f1, text=message0, justify=LEFT, fg="white", bg="gray25")
		l2.grid(row=6, column=0, columnspan=2, sticky=W, padx=10, pady=0)
		l3 = Label(f1, text=message1, justify=CENTER, fg="white", bg="gray25")
		l3.grid(row=7, column=0, columnspan=2, padx=10, pady=0)

		button = Button(tl, text="Ok", command=tl.destroy, width=10)
		button.pack(pady=5)

	def __open_file(self, doc):
		try:
			os.startfile(doc)
		except:
			pass

	def __open_folder(self, folder):
		os.system('start explorer "' + folder + '"')


if __name__ == '__main__':
	Xls2kml()








# Console (View)
# if __name__ == main():
# 	print('Ugly Duck Motion Detector -  versão 1.0.0')
# 	print()
# 	print('Choose a threshold value, the biger the value, the lesser will be the motion sensibility.')
#     print('A value between 5 and 20 is recommended')

#     input_folder = []
#     while os.listdir(input_folder) == []:
#     	input_folder = input("Write the full path of foto's folder (press 'ENTER' at the end):\n")

#     output_folder = ['some shit', 'another shit']
#     while os.listdir(output_folder) != []:
#     	output_folder = input("Write the full path of an output empty folder (press 'ENTER' at the end):\n")
	
#     threshold = None
#     while !threshold.isnumeric():
#     	threshold = input('Threshold value: ')

#     control = Controller(input_folder, output_folder, int(threshold))
#     num_fotos_with_motion_detected = control.check_motion()

#     print(f'Motion was detected in {num_fotos_with_motion_detected}')
#     exit()


# MotionDetector (Model) =======================================================
import cv2 as cv


class MotionDetector(object):

	# CONSTRUCTOR --------------------------------------------------------------
	def __init__(self, img0, img1, threshold):
		self.img0 = img0
		self.img1 = img1
		self.threshold = threshold

	# PRIVATE METHODS ----------------------------------------------------------
	def __get_binarazed_bgr(self, img):
		imgB = cv.split(img[0])
		imgG = cv.split(img[1])
		imgR = cv.split(img[2])

		(T, imgBinB) = cv2.threshold(imgB, 125, 255, cv2.THRESH_BINARY)
		(T, imgBinG) = cv2.threshold(imgG, 125, 255, cv2.THRESH_BINARY)
		(T, imgBinR) = cv2.threshold(imgR, 125, 255, cv2.THRESH_BINARY)

		imgBinBG = cv.add(imgBinB, imgBinG)
		imgBinBGR = cv.add(imgBinBG, imgBinR)

		return imgBinBGR

	# PUBLIC METHODS -----------------------------------------------------------
	def is_motion_detected(self):
		bin_img0 = __get_binarazed_bgr(self.img0)
		bin_img1 = __get_binarazed_bgr(self.img1)

		variation = bin_img1 - bin_img1

		return variation.sum() > self.threshold



# Read (Model) =================================================================
import cv2 as cv


class ReadFoto(object):

	# CONSTRUCTOR --------------------------------------------------------------
	def __init__(self, log, path):
		self.img = cv2.imread(path)
		log.write('info', f'Getting foto {path}')

	# PUBLIC METHODS -----------------------------------------------------------
	def get_foto(self):
		return self.img



# Save (Model) =================================================================
import cv2 as cv
import os


class SaveFoto(object):

	# CONSTRUCTOR --------------------------------------------------------------
	def __init__(self, log, path, img):
		cv2.imwrite(path, img)
		log.write('info', f'Foto saved: {path[path.rfind(os.sep):]}')



# Log (Model) ==================================================================
import logging
import os
from datetime import datetime


class Logger(object):
	# CONSTRUCTOR --------------------------------------------------------------
	def __init__(self, name, level, path, num_days_to_keep_logs):
		self.name = name
		self.level = level
		self.path = path
		self.num_days_to_keep_logs = num_days_to_keep_logs
		self.logger = self.__init_logger()
		self.write('info', '-' * 27 + ' PROGRAM STARTED ' + '-' * 27)
		self.write('info', f'Logger.__init__\t\t\t\tLogs path = {self.path}')

	# PRIVATE METHODS ----------------------------------------------------------
	def __init_logger(self):
		# create logger and set logging level
		logger = logging.getLogger(self.name)
		logger.setLevel(self.level)

		# create file handler and set level
		filename = f'{self.path}{self.name}-{datetime.now().date()}.log'
		handler = logging.FileHandler(filename)
		handler.setLevel(self.level)

		# create formatter and add it to handler
		log_format = '%(asctime)s\t\t%(levelname)s\t\t%(message)s'
		log_formatter = logging.Formatter(log_format)
		handler.setFormatter(log_formatter)

		# add file handler to logger
		logger.addHandler(handler)

		return logger
	
	# PUBLIC METHODS -----------------------------------------------------------
	def write(self, level, message):
		if level == 'critical':
			self.logger.critical(message)
		elif level == 'error':
			self.logger.error(message)
		elif level == 'warning':
			self.logger.warning(message)
		elif level == 'info':
			self.logger.info(message)
		else:
			self.logger.debug(message)

	def del_old(self):
		date_today = datetime.now().date()
		have_deleted_logs = False
		for log in os.listdir(self.path):
			log_date = datetime.fromisoformat(log[-14:-4]).date()
			diff = date_today - log_date
			if diff.days > self.num_days_to_keep_logs:
				try:
					os.remove(f'{self.path}{os.sep}{log}')
					have_deleted_logs = True
					message = 'Logger.del_old\t\t\t\ttDeleted old logs'
					self.write('info', message)
				except Exception as e:
					message = 'Logger.del_old\t\t\t\tFailed to delete old logs\t' + str(e)
					self.write('warning', message)
		if not have_deleted_logs:
			message = 'Logger.del_old\t\t\t\tNo old logs to delete'
			self.write('info', message)




# Controller (Controler) =======================================================
import sys
import os
import Logger


class Controller(object):

	# CONSTRUCTOR --------------------------------------------------------------
	def __init__(self, input_folder, output_folder, threshold):
		self.input_folder = input_folder
		self.output_folder = output_folder
		self.threshold = threshold

		if sys.path[0] == '':
			log_path = f'{sys.path[1]}{os.sep}logs{os.sep}'
		else:
			log_path = f'{sys.path[0]}{os.sep}logs{os.sep}'

		self.log = Logger('MotionDetector', logging.DEBUG, log_path, 30)
		self.log.del_old()

	# PRIVATE METHODS ----------------------------------------------------------
	def __get_input_fotos(self):
		input_imgs = os.listdir(self.input_folder)  # list of strs

		if input_imgs == []:
			self.log.write('error', 'The input folder is empty')
			return  # Terminar o Controller e voltar para a GUI ou Console
		else:
			self.log.write('info', 'Start reading input fotos')
			return input_imgs

	# PUBLIC METHODS -----------------------------------------------------------
	def check_motion(self):
		img0 = None
		img1 = None
		input_imgs = self.__get_input_fotos()
		num_fotos_with_motion_detected = 0
		
		for i in range(len(input_imgs) - 1):
			img0 = ReadFoto(self.log, f'{input_folder}{os.sep}{input_imgs[i]}').get_foto()
			img1 = ReadFoto(self.log, f'{input_folder}{os.sep}{input_imgs[i + 1]}').get_foto()

			if MotionDetector(img0, img1, self.threshold).is_motion_detected():
				SaveFoto(self.log, f'{self.output_folder}{os.sep}{input_imgs[i + 1]}', img1)
				num_fotos_with_motion_detected += 1

		return num_fotos_with_motion_detected

