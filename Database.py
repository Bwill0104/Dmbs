import csv
import os.path
from pathlib import Path


class Database:
    def __init__(self):
        self.numRecords = 0
        self.recordSize = 0
        self.dataFileptr = None
        self.openFlag = False
        self.deleted = []
        
    # creates a database
    def createDB(self, filename):
        csvFile = filename + ".csv"
        cfgFile = filename + ".config"
        dataFile = filename + ".data" 
        
        if not os.path.isfile(dataFile):
            print(str(dataFile)+" not found")
            return
        
        self.__readCsv(csvFile, dataFile)
        with open(cfgFile, "w") as cfg_file:
            cfg_file.write(f"Number of records: {self.numRecords}\n" )
            cfg_file.write(f"Record Size: {self.recordSize}" )

    # read and parse csv file 
    def __readCsv(self, csvFile, dataFile):
        with open(csvFile, "r") as csv_file, open(dataFile, "w") as outfile:
            for line in csv_file:
                csv_reader = csv.reader([line])
                row = next(csv_reader)                
                self.numRecords += 1
                self.__writeRecord(outfile,row[0],row[1],row[2],row[3])
        # print(os.path.getsize(dataFile))
        self.recordSize = int(os.path.getsize(dataFile) / self.numRecords)
           
    # opens the inputted file and creates the config file for it 
    def open(self, filename) -> bool :
        datafile = filename + ".data"
        cfgFile = filename + ".config"
        
        try:
            if not os.path.isfile(cfgFile):
                print(str(cfgFile)+" not found")
                return False
            if not os.path.isfile(datafile):
                print(str(datafile)+" not found")
                return False
            if self.openFlag is True or self.dataFileptr is not None:
                return False
            
            # sets the data file pointer to the opened data file
            self.dataFileptr = open(datafile, "r+")
            with open(cfgFile, "r") as cfg_file:
                # reads the number of records from the config file
                lines = cfg_file.readlines()
                first_line = lines[0].strip()
                self.numRecords = int(first_line[19:])
                
                # reads the record size from the config file
                second_line = lines[1].strip()
                self.recordSize = int(second_line[13:])
                
            self.openFlag = True
            return True
        
        except Exception as e:
            print(f"There was an error opening {filename}: {e}")
            
    # closes the database
    def close(self):
        self.numRecords = 0
        self.recordSize = 0
        self.dataFileptr.close()
        self.dataFileptr = None
        self.openFlag = False
        
        print("Successfully Close!")
        
    # writes each of the records formatted in the opened data file
    def __writeRecord(self, filestream, collegeID, state, city, name) -> bool:
        try:
            filestream.write("{:10.10}".format(collegeID))
            filestream.write("{:15.15}".format(state))
            filestream.write("{:15.15}".format(city))
            filestream.write("{:40.40}".format(name))
            filestream.write("\n")
            return True
        
        except IOError:
            return False
    
    # reads the record base on the record number    
    def readRecord(self, recordNum, collegeID, state, city, name) -> int:
        if self.openFlag is False:
            return -1
        
        if 0 <= recordNum < self.numRecords:
            self.dataFileptr.seek(recordNum * self.recordSize)
            return self.__getRecord(collegeID, state, city, name)
        else:
            return -1
     
    # gets the currently read reocrd  
    def __getRecord(self, collegeID, state, city, name) -> int:
            if self.openFlag is False:
                return -1
            line = self.dataFileptr.readline().rstrip('\n')
            
            collegeID[0] = line[:10].strip()
            state[0] = line[10:25].strip() 
            city[0] = line[25:40].strip()
            name[0] = line[40:80].strip()
            # if len(line[10:25].strip()) != 0:
                
            # else: return 0
    
            return 1
        
    # adds a record in order by id    
    def addRecord(self,collegeID, state, city, name):
        cfgFile = self.dataFileptr.name.split('.', 1)[0] + ".config"
        insert_text ="{:10}{:15}{:15}{:40}".format(collegeID[0], state[0], city[0], name[0])
        recordnum = self.__binarySearch(collegeID, state, city, name)[1]
        
        with open(self.dataFileptr.name, 'r') as outfile, open(cfgFile, "w") as cfg_file:
            content = outfile.readlines()
            self.numRecords += 1
            cfg_file.write(f"Number of records: {self.numRecords}\n" )
            cfg_file.write(f"Record Size: {self.recordSize}" )
        content.insert(recordnum + 1, insert_text + "\n")
        
        with open(self.dataFileptr.name, 'w') as outfile:
            outfile.writelines(content)
        
    # checks to see if there is a record matching the college id 
    def find(self, collegeID, state, city, name) -> bool:
        if self.openFlag is False:
            return False
        
        return self.__binarySearch(collegeID, state, city, name)
    
    # deletes a record by id number 
    def delete_record(self,collegeID, state, city, name):
        cfgFile = self.dataFileptr.name.split('.', 1)[0] + ".config"
        status,recordNum = self.__binarySearch(collegeID, state, city, name)
        
        if status is True:
            self.overwriteRecord(recordNum, collegeID[0],"", "", "")
        else:
            print("Record not found")
         
        if status is True:
            print("Successfully deleted!\n")
        
        
   
    # uses binary search method to find a certain id
    def __binarySearch(self, collegeID, state, city, name) :
        low = 0
        high = self.numRecords - 1
        self.found = False
        
        targetID = collegeID[0]
        
        while not self.found and high >= low:
            middle = (low + high) // 2
            try:
                tempID = [None]
                self.readRecord(middle, tempID, state, city, name)
                if tempID[0] is None:
                    self.readRecord(middle + 1, tempID, state, city, name)
               
            except Exception as e:
                break
            middleID = tempID[0]
            if middleID == targetID:
                self.found = True
            elif middleID < targetID:
                low = middle + 1
            else:
                high = middle - 1
            
        return self.found, middle
    
    # updates/changes a record
    def overwriteRecord(self, record_num, collegeID, state, city, name):
        try:
            # Calculate the byte offset of the record
            offset = record_num * self.recordSize 

            # Move to the beginning of the specified record
            self.dataFileptr.seek(offset)

            # Call writeRecord to output the passed-in parameters
            self.__writeRecord(self.dataFileptr, collegeID, state, city, name)
            return True
        
        except IOError:
            return False
        
    
        
        
        