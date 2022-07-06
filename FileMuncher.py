"""
FileMuncher.py

File reader class with a bit of flexibility for transforming csv datasets to prep them for visualization.
Not intended to make analysis, just to manipulate csv files into more manageable files

Process goes as follows
1. setFile(): Takes file name and checks it for validity/existence
2. setOptions(): Opens the file and reads the header. Allows user to choose which columns they want and then rename them to look better if necessary
3. readFile(): Uses the options chosen to pull required data from the file
4. exportFile(data): Converts the chosen data to csv and saves
"""


from fileinput import filename
import copy, csv


class FileMuncher:

    def __init__(self):
        self.fileName = ""
        self.fileHeaders = []
        self.colIndexesToUse = []

    #Kicks off the whole thang
    def startMunching(self):
        self.setFile()
    
    #Takes file name and checks it for validity/existence
    def setFile(self):
        #Ask user for file name, check csv
        self.fileName = input("Enter the name of a csv file you've added to the data/ directory: ")

        fileValid = False

        while not fileValid: 
            #Default filename for testing
            if self.fileName == "":
                self.fileName = "Abandoned_And_Vacant_Housing.csv"
            #Check for file extension
            elif self.fileName[-4:] != ".csv":
                self.fileName = input("Filename is not a .csv. Enter a csv file: ")
            #Check if file exists in correct directory
            elif not self.checkFile():
                self.fileName = input("No such file exists. Check file location is in data/ directory and enter file name again: ")
            else:
                fileValid = True

        print("File found, opening...")
        self.setOptions()
    #END setFile()


    #Check for file existence
    def checkFile(self):
        try:
            open("data/" + self.fileName, "r")
        except:
            return False
        else:
            return True
    #END checkfile()


    #Opens the file and reads the header. Allows user to choose which columns they want and then rename them to look better if necessary
    def setOptions(self):
        #Open the file at fileName
        try:
            f = open("data/" + self.fileName, "r", encoding='utf-8-sig')
        except:
            print("Unexpected error, ending program...")
            exit()

        #Grab just the header
        header = f.readline()
        f.close()
        headers = header.split(",")

        #Output headers in prettified format
        print("\nThe dataset headers are as follows: ")
        count = 1
        for item in headers:
            #Don't print the | if it's the last guy
            if not headers.index(item) == (len(headers) - 1):
                print("(" + str(count) + ")" + item + "  |  ", end="")
                count += 1
            else:
                print("(" + str(count) + ")" + item)

        #Ask user if they'd like to set options for the headers
        userResponse = ""
        while userResponse != "y" and userResponse != "n":
            userResponse = input("Would you like to adjust the dataset headers? y/n: ")

        if userResponse == "y":
            #TODO: Add validation to this section
            
            #Get column numbers the user wants to use
            colNums = input("Type the column numbers (separated by single spaces) for the headers you would like to use: ")
            colNums = colNums.split()
            #Transform into indexes
            colIndexes = []
            for num in colNums:
                colIndexes.append(int(num)-1)
            
            print("You've elected to use headers ", end="")
            for i in colIndexes:
                print(headers[i] + "  |  ", end="")

            #Ask user if they'd like to rename any headers
            userResponse = ""
            while userResponse != "y" and userResponse != "n":
                userResponse = input("\nWould you like to rename the dataset headers you've chosen? y/n: ")

            #TODO Allow user to rename column headers
            if userResponse == "y":
                print("You can't do that yet.")

        else:
            colIndexes = []
            for i in range(0,len(headers)):
                colIndexes.append(i)

        
        #Make a copy of column index list and save as attribute
        self.colIndexesToUse = copy.deepcopy(colIndexes)

        #Continue program
        self.readFile()
    #END setOptions()


    #Uses the options chosen to pull required data from the file
    def readFile(self):
        #Open the file at fileName
        try:
            f = open("data/" + self.fileName, "r", encoding='utf-8-sig')
        except:
            print("Unexpected error, ending program...")
            exit()

        #Go through file line by line and extract the items at self.colIndexesToUse
        extractedData = []
        for line in f:
            #Split data into list of numbers
            line = line.split(",")
            #New list for storing the data needed from this line
            extractedLine = []
            for index in self.colIndexesToUse:
                extractedLine.append(line[index])
            extractedData.append(extractedLine)

        #print(extractedData)
        self.exportFile(extractedData)
    #END readFile()

    #Converts the chosen data to csv and saves
    def exportFile(self, data):
        exportSuccessful = False

        while not exportSuccessful:
            newFileName = input("Choose a file name for the new file: ")
            
            try:
                with open("data/" + newFileName + ".csv", "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerows(data)
            except:
                print("An error occurred")
            else:
                print("Successfully exported file as 'data/" + newFileName + ".csv'")
                exportSuccessful = True
    #END exportFile()






