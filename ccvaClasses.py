import csv
import time

curDT = (str(round(time.time_ns())))

curfile = "./data/datafile"+curDT+".csv"

class CurCSV:
    def __init__(self,file,data=str):
        self.file = file
        self.data = data
        try:
            with open(self.file, 'x') as f:
                pass
            with open(self.file, "a") as CSVfile:
                writer = csv.writer(CSVfile)
                writer.writerow(['Time','Subject','Body','Notes'])
        except:
            pass
    def __str__(self):
        return "File is" + self.file
    def readFile(self):
        print("\nFile Contents:\n-----Start of File-----")
        with open(self.file, "r+") as CSVfile:
            reader = csv.reader(CSVfile)
            for row in reader:
                print(', '.join(row))
        print("-----End of File----\n")
    def printCurFile(self):
        print("File accessed at " + self.file)
        return self.file
    def writeFile(self, time, subj, body, notes):
        global timeStepper
        if self.data == None:
            print("No data provided.")
        elif self.data == str:
            with open(self.file, "a") as CSVfile:
                writer = csv.writer(CSVfile)
                writer.writerow([time,subj,body,notes])