import os
import shutil


###############################################################################################################
###############################################################################################################
###############################################################################################################


# to move images that I have saved to my data images and put it in the 'faces' directory
# to move pdfs that carries attendance to "AtteendancePDF" directory
def moveImages(path):
    try:
        names = os.listdir(path)
        images = [n for n in names if n.endswith("jpg") or n.endswith("jpeg") or n.endswith("png")]
        dest = os.path.join(path, "faces")
        currentImages = os.listdir(dest)
        #personName = []
        for i in images:
            imgName = i.split('.')
            imgName = imgName[0].lower()+'.jpg'
            #personName.append(imgName[0].lower()+'.jpg')
            #print(personName)

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

def movePDFs(path):
    try:
        names = os.listdir(path)
        pdfs = [n for n in names if n.endswith("pdf")]
        dest = os.path.join(path, "AtteendancePDF")
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




###############################################################################################################
###############################################################################################################
###############################################################################################################




if __name__ == "__main__":
    #path = r"faces"
    X = r"E:\3rd_year\KOLLIA\PROJETS\CV_Project\Attendance_project\Attendance_project"
    #p = r"AtteendancePDF"
    moveImages(X)
    #movePDFs(X)
