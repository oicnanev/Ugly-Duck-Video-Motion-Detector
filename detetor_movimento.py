"""
@python version:
    Python 3.7.1

@platform:
    Windows

@summary:
    App designed with the pattern Model-View-Controller (MVC)
    https://pt.wikipedia.org/wiki/MVC

    The goal is to detect motion in a sequence of static images. This is 
    accomplished by comparing two in a row, first resizing them to 500 pixels
    of width, then greying them, after that, create a new image with the absolut
    difference of between the images. At last, with this new image use a dilated
    binary threshold and find the contours. If the area of any contour is
    bigger than the threshold chosen in the GUI, there is motion

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

@since:
    2021-09-03
"""

import os
from time import sleep
from tkinter import BOTTOM, FALSE, W, EW, Tk, Frame, Label, Button, \
    Message, StringVar, IntVar, filedialog, ttk, Scale, VERTICAL

import cv2 as cv
import imutils
from PIL import ImageTk, Image


# GUI (View) ===================================================================
class GUI(object):
    """
    Interface build in Tkinter()
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
        if os.name == 'nt':
            self.master.iconbitmap(icon)  # window icon
            self.master.resizable(width=FALSE, height=FALSE)
            self.master.geometry("430x465")
        self.screen_size = (self.master.winfo_screenwidth(), self.master.winfo_screenheight())

        if os.name == 'nt':
            self.last_dir = "C:/"
        else:
            self.last_dir = os.sep + 'home' + os.sep
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

        # Frame to support buttons, labels and separators --------------
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
            row=1, columnspan=5, sticky=W, padx=5, pady=0)
        self.l6 = Label(
            self.f, text=text, font=font1, bg=bg, fg=bg1).grid(
            row=3, column=3, columnspan=3, sticky=EW, pady=5, padx=5)
        self.l3 = Scale(
            self.f, label='', from_=0, to=100, orient=VERTICAL,
            length=354, variable=self.threshold,
            command=self.__callback_3).grid(row=1, column=5, padx=5, pady=0)

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
        if os.name == 'nt':
            self.s.theme_use('winnative')
        else:
            self.s.theme_use('default')
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

        if not os.listdir(self.input_path):
            msg = 'ERROR: Empty input folder!      Threshold = ' + str(self.threshold.get())

        self.message.set(msg)

    def __callback_2(self):  # "Choose output folder" button handler ---
        """
        None -> None

        Calls the function self.__threat("kmz")
        """
        sleep(1)
        title = 'Select the output folder           Threshold = ' + str(self.threshold.get())
        msg = 'Choose the threshold and click Detect  Threshold = ' + str(self.threshold.get())
        self.output_path = filedialog.askdirectory(title=title, initialdir=self.last_dir)
        if os.listdir(self.output_path):
            msg = 'ERROR: The output folder is not empty!     Threshold = ' + str(self.threshold.get())

        self.message.set(msg)

    def __callback_3(self, value):  # Update Threshold value ---------------
        """
        None -> None

        Updates the threshold value
        """
        msg = str(self.message.get())[:str(self.message.get()).rfind('=')]
        self.message.set(msg + '= ' + str(self.threshold.get()))

    def __callback_4(self):  # "Detect motion" button handler ---------------
        """
        None -> None

        Calls the function self.__detect()
        """
        sleep(1)
        msg = 'Choose the threshold and click Detect  Threshold = ' + str(self.threshold.get())
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
        ctrl = Controller(self.input_path, self.output_path, self.threshold, self.screen_size)
        num_fotos_with_motion_detected = ctrl.check_motion()
        '''
        if num_fotos_with_motion_detected > 0:
            self.message.set(f"Done. {num_fotos_with_motion_detected} fotos with motion detected")
            '''


# CONSOLE (View) ===============================================================
# if __name__ == main():
#   print('Ugly Duck Motion Detector -  versão 1.0.0')
#   print()
#   print('Choose a threshold value, the bigger the value, the lesser will be the motion sensibility.')
#     print('A value between 5 and 20 is recommended')

#     input_folder = []
#     while os.listdir(input_folder) == []:
#       input_folder = input("Write the full path of fotos folder (press 'ENTER' at the end):\n")

#     output_folder = []
#     while os.listdir(output_folder) == []:
#       output_folder = input("Write the full path of an output empty folder (press 'ENTER' at the end):\n")

#     threshold = None
#     while !threshold.isnumeric():
#       threshold = input('Threshold value: ')

#     control = Controller(input_folder, output_folder, int(threshold))
#     num_fotos_with_motion_detected = control.check_motion()

#     print(f'Motion was detected in {num_fotos_with_motion_detected}')
#     exit()


# MotionDetector (Model) =======================================================
# noinspection PyMethodMayBeStatic
class MotionDetector(object):

    # CONSTRUCTOR --------------------------------------------------------------
    def __init__(self, img0, img1, threshold):
        self.img0 = img0
        self.img1 = img1
        self.threshold = threshold

    # PRIVATE METHODS ----------------------------------------------------------
    def __greying(self, img):
        # resize the image, convert it to grayscale
        _img = imutils.resize(img, width=500)
        gray = cv.cvtColor(_img, cv.COLOR_BGR2GRAY)

        return gray

# PUBLIC METHODS -----------------------------------------------------------
    def is_motion_detected(self):
        gray0 = self.__greying(self.img0)
        gray1 = self.__greying(self.img1)

        # compute the absolute difference between two images
        img_delta = cv.absdiff(gray0, gray1)
        thresh = cv.threshold(img_delta, 25, 255, cv.THRESH_BINARY)[1]

        # dilate the threshold image to fill in holes, then find contours
        # on threshold image
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


# Controller (Controller) =======================================================
class Controller(object):

    # CONSTRUCTOR --------------------------------------------------------------
    def __init__(self, input_folder, output_folder, threshold, screen_size):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.threshold = threshold
        self.screen_size = screen_size
        self.resized_img = None
        self.ratio = 1
        self.min_x = None
        self.min_y = None
        self.width = None
        self.height = None

    # PRIVATE METHODS ----------------------------------------------------------
    def __get_input_fotos(self):
        input_imgs = os.listdir(self.input_folder)  # list of str

        if not input_imgs:
            return  # Terminar o Controller e voltar para a GUI ou Console

        return input_imgs

    def __choose_custom_detection_area(self, reference_img):
        self.ratio = self.__image_ratio(reference_img)

        dim = (int(reference_img.shape[1] * self.ratio),
               int(reference_img.shape[0] * self.ratio))

        self.resized_img = cv.resize(reference_img, dim, interpolation=cv.INTER_AREA)

        cv.namedWindow("Detection Area", cv.WINDOW_AUTOSIZE)
        cv.setMouseCallback("Detection Area", self.__draw_rectangle)

        while True:
            cv.imshow("Detection Area", self.resized_img)
            if cv.waitKey(20) & 0xFF == 27:
                break

        cv.waitKey(0)
        cv.destroyAllWindows()

    def __draw_rectangle(self, event, x, y, flags, param):
        point1 = (0, 0)
        if event == cv.EVENT_LBUTTONDOWN:
            point1 = (x, y)
        elif event == cv.EVENT_LBUTTONUP:
            point2 = (x, y)
            self.min_x = min(point1[0], point2[0])
            self.min_y = min(point1[1], point2[1])
            self.width = abs(point1[0] - point2[0])
            self.height = abs(point1[1] - point2[1])
            cv.rectangle(self.resized_img, (point2[0], point2[1]), (point1[0], point1[1]), (0, 255, 0), 2)
            cut_img = self.resized_img[self.min_y:self.min_y + self.height, self.min_x:self.min_x + self.width]
            cv.imshow("Detection Area", cut_img)
            cv.waitKey(0)

    def __image_ratio(self, img):
        x = self.screen_size[0] / 2 / img.shape[1]
        y = self.screen_size[1] / 2 / img.shape[0]

        return min([x, y])

    # PUBLIC METHODS -----------------------------------------------------------
    def check_motion(self):
        input_imgs = self.__get_input_fotos()
        input_imgs.sort()
        self.__choose_custom_detection_area(ReadFoto(
            f'{self.input_folder}{os.sep}{input_imgs[0]}').get_foto())
        cv.waitKey(0)

        min_y = int(self.min_y / self.ratio)
        min_x = int(self.min_x / self.ratio)
        width = int(self.width / self.ratio)
        height = int(self.height / self.ratio)
        num_fotos_with_motion_detected = 0

        for i in range(len(input_imgs) - 1):
            img0 = ReadFoto(f'{self.input_folder}{os.sep}{input_imgs[i]}').get_foto()
            img1 = ReadFoto(f'{self.input_folder}{os.sep}{input_imgs[i + 1]}').get_foto()

            area0 = img0[min_y:min_y + height, min_x:min_x + width]
            area1 = img1[min_y:min_y + height, min_x:min_x + width]

            if MotionDetector(area0, area1, self.threshold).is_motion_detected():
                SaveFoto(f'{self.output_folder}{os.sep}{input_imgs[i + 1]}', img1)
                print(f'{self.output_folder}{os.sep}{input_imgs[i + 1]}')  # DEBUG LINE
                num_fotos_with_motion_detected += 1

        print(f'num fotos detected: {num_fotos_with_motion_detected}')
        return num_fotos_with_motion_detected


# INITIALIZATION ===============================================================
if __name__ == '__main__':
    GUI()
