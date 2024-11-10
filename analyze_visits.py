import csv

with open("ms_data.csv", mode="r") as file:
    msdata = csv.reader(file)
    
    header = next(msdata)
    print("Header:", header)
    
