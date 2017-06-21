import csv


def get_csv_row(file_name):
	"""
	Takes a csv file path, open it and returns a list of list (rows)
	"""
	csv_rdr = csv.reader(open(file_name,'rb'))
	return [row for row in csv_rdr]

def delete_column(dataset):
	# transpose column in rows
	dataset = zip(*dataset)
	dataset = [row for row in dataset if any(row)]
	return [list(row) for row in zip(*dataset)]

def merge_list(list1, list2):
	id_list1 = [row[0] for row in list1]
	duplicates = []
	for row in list2:
		if row[0] in id_list1:
			duplicates.append(row)
		else:
			list1.append(row)
	return list1, duplicates

def compare_systems(sys1,sys2,id1,id2):
	in_both = []
	only_system2 = []
	only_system1 = []
	system1 = [row[id1] for row in sys1]
	system2 = [row[id2] for row in sys2]
	for symbol in system2:
		if symbol in system1:
			in_both.append(symbol)
		else:
			only_system2.append(symbol)
	for symbol in system1:
		if symbol not in system2:
			only_system1.append(symbol)
	return in_both, only_system1, only_system2

ods_escwa = get_csv_row('data/ods_eescwa_2017_06_19.csv')
ods_ecwa = get_csv_row('data/ods_eecwa_2017_06_19.csv')
undl_ecwa = get_csv_row('data/undl_eecwa_2017_06_19.csv')
undl_escwa = get_csv_row('data/undl_eescwa_2017_06_19.csv')

# Delete empty columns in datasets
undl_escwa = delete_column(undl_escwa[1:])
ods_escwa = delete_column(ods_escwa)
undl_ecwa = delete_column(undl_ecwa[1:])
ods_ecwa = delete_column(ods_ecwa)

ods_escwa = [row[:7] for row in ods_escwa]
ods_ecwa = [row[:7] for row in ods_ecwa]

ods_titles = ['symbol', 'jobar','joben','jobfr','jobru','jobes', 'other']
undl_titles = ['001','191__a', '245','url']

ods, ods_duplicates = merge_list(ods_escwa,ods_ecwa)
undl, undl_duplicates = merge_list(undl_escwa, undl_ecwa)

ods_undl, only_ods, only_undl = compare_systems(ods,undl,0,1)

print "Number of records in ODS: {}".format(len(ods))
print "Number of records in UNDL1: {}".format(len(undl))
print "Number of records in both {}".format(len(ods_unld))
print "Number of records only in ODS {}".format(len(only_ods))
print "Number of records only in UNDL {}".format(len(only_undl))








