import os
import cv2
import csv
import shutil
import pdfkit
import numpy as np
import pandas as pd
from tkinter import *
import face_recognition as fr
from datetime import datetime
from PIL import ImageTk, Image
from fontDistScaling import get_optimal_font_scale, spaceRegion



###############################################################################################################
###############################################################################################################
###############################################################################################################

BG_GRAY = "#ABB2B9"
FONT = "Helvetica 13 bold"
FONT_BOLD = "Helvetica 10 bold"
###############################################################################################################
icoImg ='face recognition.ico'
faces = r"faces"
X = r"E:\3rd_year\KOLLIA\PROJETS\cv"

###############################################################################################################
###############################################################################################################
###############################################################################################################



class Attendance:
    def __init__(self, app_path=X, faces=faces):
        self.app_path = app_path
        self.faces = faces
        self.win = Tk()
        self._setup_main_window()
        self.videoStream()



    # get img and names of persons
    def img_and_name(self):
        images = []
        classNames = []
        mylist = os.listdir(self.faces)
        #print("img_names_and_extensions:\n", mylist)
        for cls in mylist:
            img = cv2.imread(os.path.join(self.faces, cls))
            images.append(img)
            #cv2.imshow("img", img)
            #cv2.waitKey(2)
            classNames.append(os.path.splitext(cls)[0])
        self.images = images
        self.classNames = classNames
        return self.images, self.classNames



    #images, classNames = img_and_name(path)


###############################################################################################################
###############################################################################################################
###############################################################################################################


    # Encode images
    def findEncodings(self):
        encodeList = []
        for img in self.images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = fr.face_encodings(img)[0]
            encodeList.append(encode)

        self.encodeList = encodeList
        return self.encodeList




    #encodeListknown = findEncodings(images)



###############################################################################################################
###############################################################################################################
###############################################################################################################

    def training(self):
        self.images, self.classNames = self.img_and_name()
        self.showText("Name of People in DB:\n")
        for cls in self.classNames:
            self.showText(cls+'\n')
        self.showText(f"Num of Faces: {len(self.classNames)}\n")

        self.showText("encoding faces.....\n")
        self.encodeList = self.findEncodings()
        self.showText(f"Num of Encoded Faces: {len(self.encodeList)} \n")
        self.showText("Encoding Complete.")
        self.showText("\nYOU MUST TRAIN AFTER ADDING ANY NEW PERSON....\n")
        return self.classNames, self.encodeList


###############################################################################################################
###############################################################################################################
###############################################################################################################

# check if input image is one from the encoded faces
    def isEncoded(self):
        try:
            if self.name not in self.classNames and self.name == "UNKNOWN":
                choice = input("save image? y/n\n")
                if choice.lower() == 'y':
                    imgName = input("Please Enter name of the person:\n")
                    img = self.frameCopy[self.y1-50:self.y2+100, self.x1-50:self.x2+100]
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    cv2.imwrite(imgName+'.jpg',  img) #os.path.join(path, img)
                    #encodeListknown = EncodedInputFace(img, encodeListknown)
                else:
                    self.showText("\nimages not saved........\n")
            else:
                self.showText("\nalready encoded.....\n")
        except:
            self.showText("\nopen webcam...\n")


###############################################################################################################
###############################################################################################################
###############################################################################################################

# put the name of the person in the excel file if its img is one of the encoded images
    def markAttendance(self):
        file = "Attendance.csv"
        with open(file, "r+") as f:
            myDataList = f.readlines()
            self.showText(f"current attendance: {myDataList}\n\n")
            nameList = []

            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])

            if self.name not in nameList and self.name != "UNKNOWN":
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{self.name},{dtString}')




#markAttendance('Mostafa')
###############################################################################################################
###############################################################################################################
###############################################################################################################


    def matching(self):
        #try:
        #while(self.cap.isOpened()):
        _, self.frame = self.cap.read()
        # Get the latest frame and convert into Image
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.frameCopy = self.frame.copy()
        imgS = cv2.resize(self.frame, (0,0), None, 0.25, 0.25)


        facesCurFrame = fr.face_locations(imgS)   # get coordinates of four points (rectangle) that surrounds the face
        encodeCurFrame = fr.face_encodings(imgS, facesCurFrame)  # encode the face from webcam reading

        for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
            matches = fr.compare_faces(self.encodeList, encodeFace)
            faceDist = fr.face_distance(self.encodeList, encodeFace)   # find the best match (the lower the distance the better the match is)
            print(faceDist)
            #print(matches)
            matchIndex = np.argmin(faceDist)
            print("Smallest Dist: ", faceDist[matchIndex])
            #print(classNames[matchIndex])

            if matches[matchIndex] and faceDist[matchIndex] < 6:
                self.name = self.classNames[matchIndex].title()     # upper()
            else:
                self.name = "UNKNOWN"
            print(self.name)
            y1, x2, y2, x1 = faceLoc
            #isEncoded(name, frame, y1,x2,y2,x1)
            self.y1, self.x2, self.y2, self.x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(self.frame, (self.x1, self.y1), (self.x2, self.y2+35), (0,255,0), 2)
            cv2.rectangle(self.frame, (self.x1, self.y2+35), (self.x2, self.y2), (0,255,0), cv2.FILLED)
            #scale = map(x1,0,1)
            cv2.putText(self.frame, self.name, (self.x1+6, self.y2+15), cv2.FONT_HERSHEY_COMPLEX, get_optimal_font_scale(self.name, self.x2-self.x1), (255,255,255), 2)
            self.markAttendance()

            img = Image.fromarray(self.frame)
            # Convert image to PhotoImage
            imgtk = ImageTk.PhotoImage(img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
            # Repeat after an interval to capture continiously
            self.label.after(20, self.matching)
        #except:
        #    self.showText("Train first....\n")
            #self.cap.release()
        #    cv2.destroyAllWindows()



###############################################################################################################
###############################################################################################################
###############################################################################################################

#    def closeCamera(self):
#        if self.cap.isOpened():
#            self.showText("camera closed....\n")
#            self.cap.release()
#            cv2.destroyAllWindows()
#        else:
#            self.showText("camera not opened....\n")


###############################################################################################################
###############################################################################################################
###############################################################################################################



    def videoStream(self):
        self.cap = cv2.VideoCapture(0)
        cap_w, cap_h = 640, 480
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_h)



###############################################################################################################
###############################################################################################################
###############################################################################################################


    def _setup_main_window(self):
        # Create an instance of TKinter Window or frame
        self.win.title("Attendance")
        self.win.bind('<Escape>', lambda e: win.quit())
        self.lmain = Label(self.win)

        # Set the size of the window
        w, h = 800, 600
        self.win.geometry(f"{w}x{h}")
        self.win.resizable(width = False, height = False)

        # Create a Label to capture the Video frames
        self.label = Label(self.win)
        self.label.grid(row=0, column=0)


    ###############################################################################################################

        # LABELS
        self.right_label = Label(self.win, bg="gray")
        self.right_label.place(relwidth=0.2, relheight=0.8, relx=0.8, rely=0)

        self.right_black_separator = Label(self.win, bg="black")
        self.right_black_separator.place(relheight=0.8, relx=0.8, rely=0)

        self.bottom_label = Label(self.win, bg="gray")
        self.bottom_label.place(relwidth=1, relheight=0.2, relx=0, rely=0.8)

        self.bottom_black_separator = Label(self.win, bg="black")
        self.bottom_black_separator.place(relwidth=0.8069, relheight=0.015, relx=0, rely=0.80)

        self.left_black_separator = Label(self.win, bg="black")
        self.left_black_separator.place(relheight=0.8, relx=0, rely=0)

        self.upper_black_separator = Label(self.win, bg="black")
        self.upper_black_separator.place(relwidth=0.8069, relheight=0.015, relx=0, rely=0)


    ###############################################################################################################

        #Text widget
        # Create text widget and specify size.
        self.text = Text(self.bottom_label, height = 20, width = 10, bg="cyan", fg="red", font=FONT)
        self.text.place(relwidth=0.6, relheight=0.5, relx=0.1, rely=0.3)
        #text.configure(cursor="arrow", state=DISABLED)

        # Create label
        self.l = Label(self.bottom_label, text = "Input/Output window:", fg="white", bg="black")
        self.l.place(relwidth=0.6, relheight=0.2, relx=0.1, rely=0.1)
        self.l.configure(font =("Courier", 14))

        # scroll bar
        self.scrollbar = Scrollbar(self.text)
        self.scrollbar.place(relheight=1, relx=0.974)
        self.scrollbar.configure(command=self.text.yview)


    ###############################################################################################################

        # Entry box
        self.msg_entry = Entry(self.bottom_label, fg="black", bg="white", font=FONT_BOLD)
        self.msg_entry.place(relwidth=0.57, relheight=0.15, rely=0.8, relx=0.1)
        #self.msg_entry.focus()
        self.msg_entry.focus_set()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)


        # send button
        send_button = Button(self.bottom_label, text=">", font=FONT, width=10, height=7, fg="white", bg="black",
                            command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.67, rely=0.8, relheight=0.15, relwidth=0.03)


##############################################################################################################################

        # BUTTONS
        # start webcam
        self.cam_start = Button(self.right_label, text="Start Webcam", font=FONT, width=20, height=7, fg="white", bg="black",
                            command=lambda:self.matching())
        self.cam_start.place(relwidth=0.8, relheight=0.12, relx=0.1, rely=0.05)

##############################################################################################################################

        # Train: read faces and encode them
        self.train = Button(self.right_label, text="Train", font=FONT, width=20, height=7, fg="white", bg="black",
                            command=lambda:self.training())
        self.train.place(relwidth=0.8, relheight=0.12, relx=0.1, rely=0.18)

##############################################################################################################################

        # matching
        self.is_encoded = Button(self.right_label, text="Encode Image", font=FONT, width=20, height=7, fg="white", bg="black",
                            command=lambda:self.isEncoded())
        self.is_encoded.place(relwidth=0.8, relheight=0.12, relx=0.1, rely=0.31)

##############################################################################################################################

        # create attendance pdf
        self.pdf = Button(self.right_label, text="pdf", font=FONT_BOLD, width=20, height=7, fg="white", bg="black",
                            command=lambda:self.movePDFs())
        self.pdf.place(relwidth=0.29, relheight=0.12, relx=0.05, rely=0.44)

##############################################################################################################################

        self.moveImg = Button(self.right_label, text="move\n img", font=FONT_BOLD, width=20, height=7, fg="white", bg="black",
                            command=lambda:self.moveImages())
        self.moveImg.place(relwidth=0.29, relheight=0.12, relx=0.37, rely=0.44)

##############################################################################################################################

        self.delHTML = Button(self.right_label, text="del\nHTML", font=FONT_BOLD, width=20, height=7, fg="white", bg="black",
                            command=lambda:self.deleteHTML())
        self.delHTML.place(relwidth=0.29, relheight=0.12, relx=0.69, rely=0.44)

##############################################################################################################################

        self.clear_attendance = Button(self.right_label, text="clear\nattend.", font=FONT_BOLD, width=20, height=7, fg="white", bg="black",
                            command=lambda:self.clearAttendance())
        self.clear_attendance.place(relwidth=0.29, relheight=0.12, relx=0.05, rely=0.57)

##############################################################################################################################

        self.take_attendance = Button(self.right_label, text="take\nattend.", font=FONT_BOLD, width=20, height=7, fg="white", bg="black",
                            command=lambda:self.getTodayAttendance())
        self.take_attendance.place(relwidth=0.29, relheight=0.12, relx=0.37, rely=0.57)

##############################################################################################################################

        self.yes = Button(self.right_label, text="YES", font=FONT_BOLD, width=20, height=7, bg="green", fg="white",
                            command=lambda:self.YES())
        self.yes.place(relwidth=0.29, relheight=0.05, relx=0.69, rely=0.57)

##############################################################################################################################

        self.no = Button(self.right_label, text="NO", font=FONT_BOLD, width=20, height=7, bg="red", fg="white",
                            command=lambda:self.NO())
        self.no.place(relwidth=0.29, relheight=0.05, relx=0.69, rely=0.64)

##############################################################################################################################

        self.close_camera = Button(self.right_label, text="Close Webcam", font=FONT, width=20, height=7, fg="white", bg="black",
                            command=lambda:self.closeCamera())
        self.close_camera.place(relwidth=0.8, relheight=0.12, relx=0.1, rely=0.72)

##############################################################################################################################

        # quit
        self.quit = Button(self.right_label, text="Quit", font=FONT, width=20, height=7, fg="white", bg="black",
                            command=lambda:self.win.quit())
        self.quit.place(relwidth=0.8, relheight=0.12, relx=0.1, rely=0.88)


##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg)


    def _insert_message(self, msg):
        if not msg:
            return
        self.msg_entry.delete(0, END)    # to delete the entered message from the enterring tap
        self.text.configure(state=NORMAL)
        #self.text_widget.configure(state=DISABLED)
        msg = f"{msg}\n"
        self.text.insert(END, msg)
        self.text.see(END)     # to make program scroll down automatically for the last message



    def showText(self, anyThing):
        self.text.insert(END, anyThing)
        self.text.see(END)     # to make program scroll down automatically for the last message


    #def takeInput(self):
    #    anyInput = self.msg_entry.get()



    def YES(self):
        accept = self.msg_entry.get()
        accept = 'y'
        return self.showText(accept)


    def NO(self):
        refuse = self.msg_entry.get()
        refuse = 'n'
        return self.showText(refuse)


##############################################################################################################################
##############################################################################################################################
##############################################################################################################################


    def run(self):
        self.win.iconbitmap(icoImg)
        self.win.mainloop()


##############################################################################################################################
##############################################################################################################################
##############################################################################################################################


    # to move images that I have saved to my data images and put it in the 'faces' directory
    # to move pdfs that carries attendance to "AtteendancePDF" directory
    def moveImages(self):
        try:
            names = os.listdir(self.app_path)
            images = [n for n in names if n.endswith("jpg") or n.endswith("jpeg") or n.endswith("png")]
            dest = os.path.join(self.app_path, "faces")
            currentImages = os.listdir(dest)
            for i in images:
                imgName = i.split('.')
                imgName = imgName[0].lower()+'.jpg'
                self.showText(f"\n{imgName}\n")

                if imgName in currentImages:
                    #print(True)
                    removeImage = os.path.join(dest, imgName)     # +'jpg'
                    os.remove(removeImage)
                    shutil.move(i, dest)
                else:
                    self.showText(i)
                    shutil.move(i, dest)

        except:
            self.showText("ERROR: moveImages")


    #moveImages(X, os.path.join(X, path))




    ###############################################################################################################
    ###############################################################################################################
    ###############################################################################################################

    def movePDFs(self):
        try:
            names = os.listdir(self.app_path)
            pdfs = [n for n in names if n.endswith("pdf")]
            dest = os.path.join(self.app_path, "AtteendancePDF")
            currentPDFs = os.listdir(dest)
            for p in pdfs:
                if p.lower() in currentPDFs:
                    removePDF = os.path.join(dest, p)
                    os.remove(removePDF)
                    shutil.move(p, dest)
                else:
                    shutil.move(p, dest)

        except:
            self.showText(f"Please check that your pdf name is different from pdf in the {dest}.")



##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################


    # create a html file to create pdf file with name is the date and the subject name
    def getTodayAttendance(self):
        try:
            subject = input("Please write subject name:\n")
        except:
            subject = ""

        dt = datetime.today()

        year =  dt.year
        month = dt.month
        day = dt.day
        date = f"{day}-{month}-{year}"
        #print(date)

        now = datetime.now()
        dayName = now.strftime("%A")
        #print(now.strftime("%A"))

        # convert csv to html
        CSV = pd.read_csv("Attendance.csv")
        CSV.to_html("Attendance.html")

        # convert html to pdf
        path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        pdfName = f"{subject}__{dayName}_{date}.pdf"
        pdfkit.from_url("Attendance.html", pdfName, configuration=config)


    ###############################################################################################################
    ###############################################################################################################
    ###############################################################################################################

    # it overwrites the data in the excel file with the two main columns ["Name","Time"]
    # briefly: it clears the excel file from all of its data except the two main columns ["Name","Time"] ;)
    def clearAttendance(self):
        #try:
        self.showText("\nClear Attendance.csv  (y/n?)\n")
        clear = self.msg_entry.get()
        if clear == "y":
            with open('Attendance.csv', 'w') as f:
                #reader = csv.reader(f)
                #rows = list(reader)[1:]  # no more header row
                # create the csv writer
                writer = csv.writer(f)
                # write a row to the csv file
                writer.writerow(["Name","Time"])
                self.showText("\nAttendance.csv cleared......\n")
        #else:
        #    self.showText("Attendance.csv not cleared.......\n")
        #except:
        #    self.showText("Error: clearAttendance\n")


    ###############################################################################################################
    ###############################################################################################################
    ###############################################################################################################

    def deleteHTML(self):
        try:
            names = os.listdir(self.app_path)
            htmls = [n for n in names if n.endswith("html")]
            for h in htmls:
                q = input(f"delete {h}?    (y/n)")
                if q.lower() == 'y':
                    os.remove(h)
                    self.showText(f"{h} removed.....")
                else:
                    return

        except:
            self.showText("\nError: deleteHTML.\n")




##############################################################################################################################
##############################################################################################################################
##############################################################################################################################


if __name__ == "__main__":
    obj = Attendance()
    obj.run()
