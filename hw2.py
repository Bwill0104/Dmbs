# Program written by Bryan Williams and Tony Sanchez


from Database import Database
import sys


sample = Database()
# sample.open("input")

collegeId = [""]
state = [""]
city = [""]
name = [""]

# prints a record using the id
def print_record_id(collegeId, state, city, name):
    print(f"College ID: {collegeId[0]:<10} State: {state[0]:<11} City: {city[0]:<15} Name: {name[0]:<40} ")
    
# prints the record using te record number
def print_record_number(recordNum, collegeId, state, city, name):
    print(f"Record {recordNum}, College ID: {collegeId[0]:<10} State: {state[0]:<11} City: {city[0]:<15} Name: {name[0]:<40} ")
  
# prints a formatted version of a reord; used for printing a report  
def print_report(collegeId, state, city, name):
    print(f"{collegeId[0]:<15} {state[0]:<10}  {city[0]:<19}  {name[0]:<40} ")

# updates a record by id
def update_record(id):
    collegeId = [str(id)]
    recordNum = sample.find(collegeId, state, city, name)[1]
    status = sample.find(collegeId, state, city, name)[0]
    if status:
        print_record_id(collegeId, state, city, name)
    else:
        print("ID ", collegeId[0], " not found")
    
    # allows the user to edit the state, city, or name attribute of a record
    print("\n1)  State")
    print("2)  City")
    print("3)  Name\n")
    change = int(input("Enter Attribute: "))
    
    if change == 1:
        new_state = input("Enter updated State: ")
        status_overwrite = sample.overwriteRecord(recordNum, collegeId[0], new_state, city[0], name[0])
    elif change == 2:
        new_city = input("Enter updated City: ")
        status_overwrite = sample.overwriteRecord(recordNum, collegeId[0], state[0], new_city, name[0])
    elif change == 3:
        new_name = input("Enter updated Name: ")
        status_overwrite = sample.overwriteRecord(recordNum, collegeId[0], state[0], city[0], new_name)
    else:
        sys.exit()

    if status_overwrite:
        status = sample.readRecord(recordNum, collegeId, state, city, name)
        if status:
            print_record_number(recordNum, collegeId, state, city, name)
    else:
        print("Failed to read record number ", recordNum)

# displays a record by the id
def display_record(id) :
    collegeid = [str(id)]
    status = sample.find(collegeid, state, city, name)[0]
    if status is True:
        print_record_id(collegeid, state, city, name)
    else:
        print("ID ", collegeid[0], " not found")
    return id

# prints the first 10 valid records 
def create_report():
    print("\n------------- Printing Report ------------\n")
    print("{:15.15} {:11.11} {:20.20} {:42.42} ".format("College ID", "State", "City", "Name"))
         
    valid = 0
    i = 0
    while valid < 10:
        status = sample.readRecord(i, collegeId, state, city, name)
        if len(state[0]) != 0:
            print_report(collegeId, state, city, name)
            valid += 1
        i += 1
            
# adds a new record in the numerical order of the id
def add_record():
    added_id = [input("Enter College ID: ")]
    added_state = [input("Enter State: ")]
    added_city = [input("Enter City: ")]
    added_name = [input("Enter College Name: ")]
    sample.addRecord(added_id, added_state, added_city, added_name)
    
    print("Successfully added!\n")
  

    
        
 
#____________________________Main Method _____________________________
def main():
    print("Program written by Bryan Williams and Tony Sanchez")

    while True:
        print("\n------------- Menu ------------")
        print("1)  Create new database")
        print("2)  Open database")
        print("3)  Close database")
        print("4)  Display record")
        print("5)  Update record")
        print("6)  Create report")
        print("7)  Add record")
        print("8)  Delete record")
        print("9)  Quit")

        option = int(input("\nEnter Option: "))

        if option == 1:
            #filepath = input("Enter CSV filename: ")
            sample.createDB(input("\nEnter CSV filename: "))
        elif option == 2:
            filepath = input("\nEnter CSV filename: ")
            if sample.openFlag is True or sample.dataFileptr is not None:
                print(f"File {sample.dataFileptr.name} is already open\nPlease close the file (option 3) before opening a new one")
            else:   
                sample.open(filepath)
        elif option == 3:
            sample.close()
        elif option == 4:
            id = int(input("\nEnter College Id: "))
            display_record(id)
        elif option == 5:
            id = int(input("\nEnter College Id: "))
            update_record(id)
        elif option == 6:
            create_report()
        elif option == 7:
            add_record()
        elif option == 8:
            id = int(input("\nEnter College Id: "))
            collegeid = [str(id)]
            sample.delete_record(collegeid, state, city, name)
        elif option == 9:
            sys.exit()
        else:
            sys.exit()

if __name__ == "__main__":
    main()

