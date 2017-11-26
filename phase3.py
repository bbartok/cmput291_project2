from bsddb3 import db
import re

DB_File1 = "re.idx"
database1 = db.DB()
# database1.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
database1.open(DB_File1,None, db.DB_HASH, db.DB_CREATE)
curs1 = database1.cursor()

DB_File2 = "te.idx"
database2 = db.DB()
database2.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
database2.open(DB_File2,None, db.DB_BTREE, db.DB_CREATE)
curs2 = database2.cursor()

DB_File3 = "ye.idx"
database3 = db.DB()
database3.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
database3.open(DB_File3,None, db.DB_BTREE, db.DB_CREATE)
curs3 = database3.cursor()



def main():
	year_str = 'year'
	term_str = 'term'
	phrase_str = 'termPrefix'
	input_str = str('input the input')
	if (year_str in input_str):
		year_val = str(re.findall(r'\d+', year_str)[0])
		if (':' in input_str):
			program3(year_val)
		if ('>' in input_str):
			program6(year_val, 1)
		if ('<' in input_str):
			program6(year_val, 1)

	elif (term_str in input_str):






def program1(): # from term index
	while(True):
		title = 'parallel'
		term_rec = curs2.set(title.encode("utf-8")) # hash needs full key
		if (term_rec == None):
			print("No data Found.")
			break
		printrec(term_rec)
		# In the presence of duplicate key values, term_rec will be set on the first data item for the given key. 
		# journals/acta/Saxena96:<article key="journals/acta/Saxena96"><author>[0]Sanjeev Saxena</author><title>[1]Parallel Integer Sorting and Simulation Amongst CRCW Models.</title><pages>[2]607-619</pages><year>[3]1996</year><journal>Acta Inf.</journal></article>
		dup = curs2.next_dup()
		while(dup != None):
			printrec(dup)
			dup = curs2.next_dup()
		break
			

def printrec(term_rec):
	if(term_rec != None):
		result = curs1.set(term_rec.encode("utf-8"))
		print("List of records: ") # title[0], author[1], journal[2], publisher[3], booktitle[4]
		print("Author: " + str(result[0].decode("utf-8")) + " Title: " + str(result[1].decode("utf-8")) + " Pages: " + str(result[2].decode("utf-8")) + " Year: " + str(result[3].decode("utf-8")) + "Journal name: " + str(result[4].decode("utf-8")))
		# print('(' + str(result[0].decode("utf-8")+ '|' + str(result[1].decode("utf-8") + '|' str(result[2].decode("utf-8")) + str(result[3].decode("utf-8")) + str(result[4].decode("utf-8"))')')
		#iterating through duplicates:
		dup = curs1.next_dup()
		while(dup != None):
			print("Author: " + str(result[0].decode("utf-8")) + " Title: " + str(result[1].decode("utf-8")) + " Pages: " + str(result[2].decode("utf-8")) + " Year: " + str(result[3].decode("utf-8")) + "Journal name: " + str(result[4].decode("utf-8")))
			dup = curs1.next_dup()
		




def program2():
	while(True):
		author = 'a-schindler'
		term_rec = curs2.set(author.encode("utf-8")) # hash needs full key
		if (term_rec == None):
			print("No data Found.")
			break
		#In the presence of duplicate key values, term_rec will be set on the first data item for the given key. 
		printrec(term_rec)
		#In the presence of duplicate key values, term_rec will be set on the first data item for the given key. 
		# journals/acta/Saxena96:<article key="journals/acta/Saxena96"><author>[0]Sanjeev Saxena</author><title>[1]Parallel Integer Sorting and Simulation Amongst CRCW Models.</title><pages>[2]607-619</pages><year>[3]1996</year><journal>Acta Inf.</journal></article>
		dup = curs2.next_dup()
		while(dup != None):
			printrec(dup)
			dup = curs2.next_dup()
		break
		


def program3(year_val):
	while(True):
		year = year_val
		year_rec = curs3.set(year.encode("utf-8")) # hash needs full key
		if (year_rec == None):
			print("No data Found.")
			break
		#In the presence of duplicate key values, year_rec will be set on the first data item for the given key. 
	   
		printrec(year_rec)
		#In the presence of duplicate key values, term_rec will be set on the first data item for the given key. 
		# journals/acta/Saxena96:<article key="journals/acta/Saxena96"><author>[0]Sanjeev Saxena</author><title>[1]Parallel Integer Sorting and Simulation Amongst CRCW Models.</title><pages>[2]607-619</pages><year>[3]1996</year><journal>Acta Inf.</journal></article>
		dup = curs3.next_dup()
		while(dup != None):
			printrec(dup)
			dup = curs3.next_dup()
		break
		


# other:pvldb
# the fourth query returns all records that have the term pvldb in other text fields (those fields include journal, book title and publisher).
def program4():
	while(True):
		other = 'o-pvldb'
		term_rec = curs2.set(other.encode("utf-8")) # hash needs full key
		if (term_rec == None):
			print("No data Found.")
			break
		#In the presence of duplicate key values, term_rec will be set on the first data item for the given key. 
	   
		printrec(term_rec)
		#In the presence of duplicate key values, term_rec will be set on the first data item for the given key. 
		# journals/acta/Saxena96:<article key="journals/acta/Saxena96"><author>[0]Sanjeev Saxena</author><title>[1]Parallel Integer Sorting and Simulation Amongst CRCW Models.</title><pages>[2]607-619</pages><year>[3]1996</year><journal>Acta Inf.</journal></article>
		dup = curs2.next_dup()
		while(dup != None):
			printrec(dup)
			dup = curs2.next_dup()
		break
		


def program5():
	title_list = []
	author_list = []
	other_list = []
	# year_list = []
	to_rec_list_temp = []
	to_rec_list = []
	title = 'parallel'
	author = 'a-schindler'
	other = 'o-pvldb'
	# year = '2000'
	
	####
	term_rec1 = curs2.set(title.encode("utf-8"))
	title_list.append(term_rec1)
	dup = curs2.next_dup()
	while(dup != None):
		title_list.append(dup)
		dup = curs2.next_dup()
	####
	term_rec2 = curs2.set(author.encode("utf-8"))
	author_list.append(term_rec2)
	dup = curs2.next_dup()
	while(dup != None):
		author_list.append(dup)
		dup = curs2.next_dup()
	####
	term_rec3 = curs2.set(other.encode("utf-8"))
	other_list.append(term_rec3)
	dup = curs2.next_dup()
	while(dup != None):
		other_list.append(dup)
		dup = curs2.next_dup()
	####
	'''year_rec = curs3.set(year.encode("utf-8"))
							year_list.append(year_rec)
							dup = curs3.next_dup()
							while(dup != None):
								year_list.append(dup)
								dup = curs3.next_dup()'''

	to_rec_list_temp.extend(title_list)
	to_rec_list_temp.extend(author_list)
	to_rec_list_temp.extend(other_list)
	# to_rec_list_temp.extend(year_list)

	for i in to_rec_list_temp:
		if (to_rec_list_temp.count(i) >= 3):
			to_rec_list.append(to_rec_list_temp[i])

	for i in to_rec_list:
		printrec(to_rec_list[i]) # set function of python


def program6(year_val, switch):
	if (switch == 1): # more than
		while(True):
			year = year_val
			year_rec = curs3.set(year.encode("utf-8")) # hash needs full key
			if (year_rec == None):
				year_rec = curs3.set_range(year.encode("utf-8"))
			printrec(year_rec)
			#In the presence of duplicate key values, term_rec will be set on the first data item for the given key. 
			# journals/acta/Saxena96:<article key="journals/acta/Saxena96"><author>[0]Sanjeev Saxena</author><title>[1]Parallel Integer Sorting and Simulation Amongst CRCW Models.</title><pages>[2]607-619</pages><year>[3]1996</year><journal>Acta Inf.</journal></article>
			next = curs3.next()
			while(next != None):
				printrec(next)
				next = curs3.next()
			break
			

	else: # less than
		while(True):
			year = year_val
			year_rec = curs3.set(year.encode("utf-8")) # hash needs full key
			if (year_rec == None):
				year_rec = curs3.set_range(year.encode("utf-8"))
				year_rec = curs3.prev()
			printrec(year_rec)
			#In the presence of duplicate key values, term_rec will be set on the first data item for the given key. 
			# journals/acta/Saxena96:<article key="journals/acta/Saxena96"><author>[0]Sanjeev Saxena</author><title>[1]Parallel Integer Sorting and Simulation Amongst CRCW Models.</title><pages>[2]607-619</pages><year>[3]1996</year><journal>Acta Inf.</journal></article>
			prev = curs3.prev()
			while(prev != None):
				printrec(prev)
				prev = curs3.prev()
			break
			


def program7():
	title_list1 = []
	title_list2 = []
	
	title1 = 'parallel'
	title2 = 'sorting'
	
	####
	term_rec1 = curs2.set(title1.encode("utf-8"))
	title_list1.append(term_rec1)
	dup = curs2.next_dup()
	while(dup != None):
		title_list1.append(dup)
		dup = curs2.next_dup()
	####
	term_rec2 = curs2.set(title2.encode("utf-8"))
	title_list2.append(term_rec2)
	dup = curs2.next_dup()
	while(dup != None):
		title_list2.append(dup)
		dup = curs2.next_dup()

	to_rec_list_temp.extend(title_list1)
	to_rec_list_temp.extend(title_list2)


	for i in to_rec_list_temp:
		if (to_rec_list_temp.count(i) >= 2):
			to_rec_list.append(to_rec_list_temp[i])

	for i in to_rec_list:
		printrec(to_rec_list[i]) # set function of python


