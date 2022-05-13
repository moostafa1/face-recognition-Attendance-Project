import os
import cv2
import csv
import shutil
import pdfkit
import numpy as np
import pandas as pd
import face_recognition as fr
from datetime import datetime
from fontDistScaling import get_optimal_font_scale, spaceRegion



###############################################################################################################
###############################################################################################################
###############################################################################################################


faces = r"faces"
X = r"E:\3rd_year\KOLLIA\PROJETS\cv"

###############################################################################################################
###############################################################################################################
###############################################################################################################



class Attendance:
    def __init__(self, app_path=X, faces=faces):
        self.app_path = app_path
        self.faces = faces
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
        print("Name of People in DB:\n")
        for cls in self.classNames:
            print(cls+'\n')
        print(f"Num of Faces: {len(self.classNames)}\n")

        print("encoding faces.....\n")
        self.encodeList = self.findEncodings()
        print(f"Num of Encoded Faces: {len(self.encodeList)} \n")
        print("Encoding Complete.")
        print("\nYOU MUST TRAIN AFTER ADDING ANY NEW PERSON....\n")
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
                    print("\nimages not saved........\n")
            else:
                print("\nalready encoded.....\n")
        except:
            print("\nopen webcam...\n")


###############################################################################################################
###############################################################################################################
###############################################################################################################

# put the name of the person in the excel file if its img is one of the encoded images
    def markAttendance(self):
        file = "Attendance.csv"
        with open(file, "r+") as f:
            myDataList = f.readlines()
            print(f"current attendance: {myDataList}\n\n")
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
        while(self.cap.isOpened()):
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

            cv2.imshow("WebCam", self.frame)
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
                print(f"\n{imgName}\n")

                if imgName in currentImages:
                    #print(True)
                    removeImage = os.path.join(dest, imgName)     # +'jpg'
                    os.remove(removeImage)
                    shutil.move(i, dest)
                else:
                    print(i)
                    shutil.move(i, dest)

        except:
            print("ERROR: moveImages")


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
            print(f"Please check that your pdf name is different from pdf in the {dest}.")



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
        print("\nClear Attendance.csv  (y/n?)\n")
        clear = self.msg_entry.get()
        if clear == "y":
            with open('Attendance.csv', 'w') as f:
                #reader = csv.reader(f)
                #rows = list(reader)[1:]  # no more header row
                # create the csv writer
                writer = csv.writer(f)
                # write a row to the csv file
                writer.writerow(["Name","Time"])
                print("\nAttendance.csv cleared......\n")
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
                    print(f"{h} removed.....")
                else:
                    return

        except:
            print("\nError: deleteHTML.\n")




##############################################################################################################################
##############################################################################################################################
##############################################################################################################################


if __name__ == "__main__":
    obj = Attendance()
    obj.training()
    obj.matching()
