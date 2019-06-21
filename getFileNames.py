import os

class getFileNames():
    def get_csvs(self):
        csvfiles = []
        allfiles = os.listdir()
        for file in allfiles:
            if(file.endswith(".csv")):
                csvfiles.append(file)
        return csvfiles




