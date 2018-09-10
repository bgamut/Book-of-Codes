import PyPDF2
import sys
from sentiment import relativepath
import time
def read(file_name):
    newfile=relativepath(file_name)
    file = open(newfile,'rb')
    fileReader=PyPDF2.PdfFileReader(file)
    for i in range(fileReader.numPages):
        pageObj = fileReader.getPage(i)
        stringraw=pageObj.extractText()
        sometype=stringraw.split()
        for j in range(len(sometype)):
            yield(sometype[j])
            time.sleep(0.125)
if __name__ == "__main__":
	if sys.argv[1]:
		read(sys.argv[1])