# Read IP addresses from csv file than PING them one by one.

import os

file = "/Users/scui/Downloads/NOC_mgnt_segment.csv"

with open(file) as file_object:
    file_contents = file_object.readlines()
    file_contents.pop(0)

    for line in file_contents:  # Read each item
        row = line.rstrip().replace('"', '').split(',')
#        address_row = row.split(',')  #Remove quote and newline
        print(row)
 #       addresses.append(address_row)
