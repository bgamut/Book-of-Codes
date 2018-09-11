import PyPDF2
import sys
import time
from sentiment import relativepath
import os


def read(file_name):
    newfile=relativepath(file_name)
    file = open(newfile,'rb')
    fileReader=PyPDF2.PdfFileReader(file)
    for i in range(fileReader.numPages):
        pageObj = fileReader.getPage(i)
        stringraw=pageObj.extractText()
        sometype=stringraw.split()
        for j in range(len(sometype)):
            print(sometype[j])
            #yield(sometype[j])
            time.sleep(0.125)
            os.system('cls')

if __name__ == "__main__":
    read(sys.argv[1])
