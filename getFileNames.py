import os

class getFileNames():
    def operate_csvs(self, mode):
        csvfiles = []
        allfiles = os.listdir()
        for file in allfiles:
            if(file.endswith(".csv")):
                if(mode==1):
                    csvfiles.append(file)
                if(mode==2):
                    os.remove(file)
        return csvfiles

