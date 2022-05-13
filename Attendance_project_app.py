import cv2
import numpy as np
import face_recognition as fr
from datetime import datetime
import shutil
import os
from csv_to_pdf import getTodayAttendance, clearAttendance
from move_images import moveImages, movePDFs
from fontDistScaling import get_optimal_font_scale, spaceRegion


###############################################################################################################
###############################################################################################################
###############################################################################################################

path = r"faces"
X = r"E:\3rd_year\KOLLIA\PROJETS\cv"

###############################################################################################################
###############################################################################################################
###############################################################################################################



# get img and names of persons
def img_and_name(dir):
    images = []
    classNames = []
    mylist = os.listdir(dir)
    #print("img_names_and_extensions:\n", mylist)
    for cls in mylist:
        img = cv2.imread(os.path.join(dir, cls))
        images.append(img)
        #cv2.imshow("img", img)
        #cv2.waitKey(2)
        classNames.append(os.path.splitext(cls)[0])
    return images, classNames




###############################################################################################################
###############################################################################################################
###############################################################################################################


# Encode images
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList




###############################################################################################################
###############################################################################################################
###############################################################################################################


# check if input image is one from the encoded faces
def isEncoded(name, img, y1,x2,y2,x1):
    try:
        if name == "UNKNOWN":
            choice = input("save image? y/n\n")
            if choice.lower() == 'y':
                imgName = input("Please Enter name of the person:\n")
                img = img[y1-50:y2+100, x1-50:x2+100]
                cv2.imwrite(imgName+'.jpg', img) #os.path.join(path, img)
                #encodeListknown = EncodedInputFace(img, encodeListknown)
            else:
                print("images not saved........\n\n\n")
    except:
        print("images not saved...\n\n\n")


###############################################################################################################
###############################################################################################################
###############################################################################################################

# put the name of the person in the excel file if its img is one of the encoded images
def markAttendance(name):
    file = "Attendance.csv"
    with open(file, "r+") as f:
        myDataList = f.readlines()
        print(myDataList)
        nameList = []

        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList and name != "UNKNOWN":
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')




#markAttendance('Mostafa')
###############################################################################################################
###############################################################################################################
###############################################################################################################



def matching(img):
    # we resized the image to make processing faster
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)   #cv2.resize(src, dsize[, dst[, fx[, fy[, interpolation]]]])
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    facesCurFrame = fr.face_locations(imgS)   # get coordinates of four points (rectangle) that surrounds the face
    encodeCurFrame = fr.face_encodings(imgS, facesCurFrame)  # encode the face from webcam reading

    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = fr.compare_faces(encodeListknown, encodeFace)
        faceDist = fr.face_distance(encodeListknown, encodeFace)   # find the best match (the lower the distance the better the match is)
        print(faceDist)
        #print(matches)
        matchIndex = np.argmin(faceDist)
        print("Smallest Dist: ", faceDist[matchIndex])
        #print(classNames[matchIndex])

        if matches[matchIndex] and faceDist[matchIndex] < 6:
            name = classNames[matchIndex].title()     # upper()
        else:
            name = "UNKNOWN"
        print(name)
        y1,x2,y2,x1 = faceLoc
        isEncoded(name, img, y1,x2,y2,x1)
        #y1,x2,y2,x1 = y1*4, x2*4, y2*4, x1*4
        cv2.rectangle(img, (x1,y1), (x2,y2+35), (0,255,0), 2)
        cv2.rectangle(img, (x1,y2+35), (x2,y2), (0,255,0), cv2.FILLED)
        #scale = map(x1,0,1)
        cv2.putText(img, name, (x1+6,y2+15), cv2.FONT_HERSHEY_COMPLEX, get_optimal_font_scale(name, x2-x1), (255,255,255), 2)
        markAttendance(name)



###############################################################################################################
###############################################################################################################
###############################################################################################################



# https://www.youtube.com/watch?v=oP3MQyO-wwc    Gui code video
# working perfect
if __name__ == "__main__":

    images, classNames = img_and_name(path)
    print(classNames)
    print(len(classNames))


    encodeListknown = findEncodings(images)
    print(len(encodeListknown))
    print("Encoding Complete.")


    cap = cv2.VideoCapture(0)
    while True:
      success, img = cap.read()
      moveImages(X)
      movePDFs(X)
      images, classNames = img_and_name(path)
      spaceRegion()
      if len(images) > len(encodeListknown):
          print("encoding.......")
          encodeListknown = findEncodings(images)
          spaceRegion()
      matching(img)
      cv2.imshow("WebCam", img)
      if cv2.waitKey(1) & 0xFF == ord('q'):
          q = input("QUIT?  (y/n)")
          if q.lower() == 'y':
              spaceRegion()
              getTodayAttendance()
              clearAttendance()
              movePDFs(X)
              break
          else:
              continue



###############################################################################################################
###############################################################################################################
###############################################################################################################
