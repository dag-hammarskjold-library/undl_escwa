
# Library to read and write csv files
import csv
from csv import writer


def get_csv_row(file_name):
	"""
	Takes a csv file path, open it and returns a list of lists where nested lists correspond to csv rows
	"""
	csv_rdr = csv.reader(open(file_name,'rb'))
	return [row for row in csv_rdr]

def delete_column(dataset):
	"""
	Takes a list of lists (rows), and delete columns if there is no value for all rows.
	"""
	# transpose columns in rows
	dataset = zip(*dataset)
	# delete empty rows if any
	dataset = [row for row in dataset if any(row)]
	# transpose rows in columns to return a list of lists.
	return [list(row) for row in zip(*dataset)]

def merge_list(list1, list2, id_index=0):
	"""
	Takes two similar lists of lists, remove the duplicates and merge the two lists. return the merged lists and the list of duplicates.
	"""
	id_list1 = [row[id_index] for row in list1]
	duplicates = []
	for row in list2:
		if row[id_index] in id_list1:
			duplicates.append(row)
		else:
			list1.append(row)
	return list1, duplicates

def compare_systems(sys1,sys2,id_index1,id_index2):
	"""
	Takes data stored in  2 systems, and the index where the common identifier
	is. Compare the identifiers, and return of list of identifier for the
	data that are in both system, only in system 1 or only in system2.
	"""
	in_both = []
	only_system2 = []
	only_system1 = []
	system1 = [row[id_index1] for row in sys1]
	system2 = [row[id_index2] for row in sys2]
	for identifier in system2:
		if identifier in system1:
			in_both.append(identifier)
		else:
			only_system2.append(identifier)
	for identifier in system1:
		if identifier not in system2:
			only_system1.append(identifier)
	return in_both, only_system1, only_system2

def write_sheet(book, sheet_name, data):
	book = book.add_sheet(sheet_name)
	rowx = 0
	colx = 0
	for row in data:
	    for colx, value in enumerate(row):
	        sheet.write(rowx, colx, value)
	        rowx += 1
	return book

def clean(row):
    """
    This function  takes a line and remove bad caracters
    """
    for v in row:
    	v = v.replace("\xef\xbb\xbf","")
    return row

def write_file(data,file_name):
	"""
	This assigns to the variable new_csv_file a newly opened file(file_name)
	opened in 'wb mode' ( = write in binary mode).
	"""
	with open(file_name,'wb') as new_csv_file:
		wrtr = writer(new_csv_file)
		for row in data:
			wrtr.writerow(row)

# Create a list of each csv files.
ods_escwa = get_csv_row('data/ods_eescwa_2017_06_19.csv')
ods_ecwa = get_csv_row('data/ods_eecwa_2017_06_19.csv')
undl_ecwa = get_csv_row('data/undl_eecwa_2017_06_19.csv')
undl_escwa = get_csv_row('data/undl_eescwa_2017_06_19.csv')

# Delete empty columns in datasets, and header rows if any
undl_escwa = delete_column(undl_escwa[1:])
ods_escwa = delete_column(ods_escwa)
undl_ecwa = delete_column(undl_ecwa[1:])
ods_ecwa = delete_column(ods_ecwa)

# clean:
undl_ecwa = [clean(row) for row in undl_ecwa]
undl_escwa = [clean(row) for row in undl_escwa]
ods_ecwa = [clean(row) for row in ods_ecwa]
ods_escwa = [clean(row) for row in ods_escwa]

# merge data comming from the same system.
ods, ods_duplicates = merge_list(ods_escwa,ods_ecwa)
undl, undl_duplicates = merge_list(undl_escwa, undl_ecwa)


# compare the systems to get list of symbol that are in both system, only in
# ods or only in undl
ods_undl, only_ods, only_undl = compare_systems(ods,undl,0,1)

# print some usefull numbers
print "Number of records in ODS: {}".format(len(ods))
print "Number of records in UNDL1: {}".format(len(undl))
print "Number of records in both {}".format(len(ods_undl))
print "Number of records only in ODS: {}".format(len(only_ods))
print "Number of records only in UNDL: {}".format(len(only_undl))

# Write results in distinct csv

write_file(only_ods,'export/ods_only.csv')
write_file(only_undl,'export/undl_only.csv')
write_file(ods_undl,'export/ods_undl.csv')

