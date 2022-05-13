import pdfkit
import pandas as pd
from datetime import datetime
import csv
import os


###############################################################################################################
###############################################################################################################
###############################################################################################################

X = r"E:\3rd_year\KOLLIA\PROJETS\CV_Project\Attendance_project\Attendance_project"

###############################################################################################################
###############################################################################################################
###############################################################################################################


# create a html file to create pdf file with name is the date and the subject name
def getTodayAttendance():
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

    # convert csv to html
    CSV = pd.read_csv("Attendance.csv")
    CSV.to_html("Attendance.html")

    # convert html to pdf
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfName = f"{subject}__{dayName}_{date}.pdf"
    pdfkit.from_url("Attendance.html", pdfName, configuration=config)

    deleteHTML(X)

###############################################################################################################
###############################################################################################################
###############################################################################################################

# it overwrites the data in the excel file with the two main columns ["Name","Time"]
# briefly: it clears the excel file from all of its data except the two main columns ["Name","Time"] ;)
def clearAttendance():
    try:
        clear = input("Clear Attendance.csv  (y/n?)\n")
        if clear.lower() == "y":
            with open('Attendance.csv', 'w') as f:
                #reader = csv.reader(f)
                #rows = list(reader)[1:]  # no more header row
                # create the csv writer
                writer = csv.writer(f)
                # write a row to the csv file
                writer.writerow(["Name","Time"])
                #print(rows)
        else:
            print("Attendance.csv not cleared.......")
    except:
        print("Attendance.csv not cleared.......")


###############################################################################################################
###############################################################################################################
###############################################################################################################

def deleteHTML(path):
    #try:
    names = os.listdir(path)
    htmls = [n for n in names if n.endswith("html")]
    for h in htmls:
        q = input(f"delete {h}?    (y/n)")
        if q.lower() == 'y':
            os.remove(h)
            print(f"{h} removed.....")
        else:
            return

    #except:
    #    print(f"Please check that your pdf name is different from pdf in the {dest}.")



###############################################################################################################
###############################################################################################################
###############################################################################################################

if __name__ == "__main__":
    getTodayAttendance()

    #clearAttendance()
    #deleteHTML(X)
