import mylib as source
db = source.db
login = False
cinema_db = source.cinema_db
source.data()
member = None

def LOGIN(a1, a2):
	global login
	person = db[a1]
	if person:
		if person.password == a2:
			global member
			member = person
			login = True
			print('LOGIN SUCCESSFUL!')
		else:
			print('LOGIN FAILED!')
	else:
		print('LOGIN FAILED!')
	db.i = -1		

def REGISTER(a1, a2):
	global db
	person = source.Person(a1, a2)
	if person not in db:
		db += person
		db[person.name] = person
		db.save()
		print('REGISTERED SUCCESSFULY!')
	else:
		print('Username ('+a1+') already exists!')
	db.i = -1

def DELETE(a1, a2):
	global db
	global login
	person = db[a1]
	if person:
		if person.password == a2:
			db.delete(person)
			login = False
			print('DELETED SUCCESSFULLY!')
		else:
			print('Wrong username or password!')
	else:
		print('Wrong username or password!')
	db.i = -1

def VIEW_CINEMAS():
	global	cinema_db
	for cinema in cinema_db:
		print(cinema)
	cinema_db.i = -1

def VIEW_ALL_MOVIES(a4):
	global cinema_db
	cinema = cinema_db[a4]
	try:
		if cinema == None:
			raise source.CinemaNotFoundException('NO SUCH MOVIE THEATRE!')
		movieNode = cinema.head
		while True:
			print(movieNode.value)
			if movieNode.next != None:
				movieNode = movieNode.next
			else:
				break
		
	except source.CinemaNotFoundException as err:
		print(err)
	finally:
		cinema_db.i = -1


def VIEW_ALL_SANS(a4, a5):
	global cinema_db
	cinema = cinema_db[a4]
	flag = True
	try:
		if cinema == None:
			raise source.CinemaNotFoundException('NO SUCH MOVIE THEATRE!')
		movieNode = cinema.head
		while True and flag:
			if movieNode.value.name == a5:
				print('All Sans for', a4+',',a5+':')
				sans = movieNode.value.head
				while True:
					print(sans.value)
					if sans.next != None:
						sans = sans.next
					else:
						flag = False
						break
			if movieNode.next != None:
				movieNode = movieNode.next
			else:
				raise source.MovieNotFoundException('NO SUCH MOVIE FOUND AT '+a4+'!')
		
	except source.CinemaNotFoundException as err:
		print(err)
	except source.MovieNotFoundException as err:
		print(err)
	finally:
		cinema_db.i = -1

def PURCHASE(a1, a2, a3, a4, a5):
	if login:
		global cinema_db
		cinema = cinema_db[a1]
		flag = True
		try:
			if cinema == None:
				raise source.CinemaNotFoundException('NO SUCH MOVIE THEATRE! ('+a1+')')
			movieNode = cinema.head
			while True and flag:
				if movieNode.value.name == a2:
					sans = movieNode.value.head
					while True and flag:
						if sans.value.name == a3 + a4:
							if int(a5) > sans.value.caps:
								raise source.NotEnoughCapacityException("CAN' T FINISH TRANSACTION! There are only "+str(sans.value.caps)+" tickets for "+ a2+ " at "+a1+" on "+a3+" "+a4)
							sans.value.caps = sans.value.caps - int(a5)
							global member
							member.reservations.append(a1 + ' ' + a2 + ' ' + a3 + ' ' + a4+ ' '+a5)
							print("PURCHASE COMPLETED! "+a5+" tickets for "+a2+" at "+a1+" on "+a3+ " "+a4 )
							flag = False
							cinema_db[a1] = cinema
							cinema_db.save()
							db[member.name] = member
							db.save()
						elif sans.next != None:
							sans = sans.next
						else:
							flag = False
							raise source.SansNotFoundException('SANS NOT FOUND!('+a3+' '+a4+')')
				if movieNode.next != None:
					movieNode = movieNode.next
				else:
					raise source.MovieNotFoundException('MOVIE NOT FOUN! ('+a2+')')
			
		except source.CinemaNotFoundException as err:
			print(err)
		except source.MovieNotFoundException as err:
			print(err)
		except source.SansNotFoundException as err:
			print(err)
		except source.NotEnoughCapacityException as err:
			print(err)
		finally:
			cinema_db.i = -1
	else:
		print('You have not logged in, please login first to purchase tickets!')

def SEE_MY_RES():
	if login:
		global member
		print('RESERVATIONS for user ('+member.name+')')
		a = member.get_reservations()
		if a != []:
			for i in a:
				b = list(map(str, i.strip().split()))
				print(b[4]+' tickets for '+b[1]+' at '+b[0]+' on '+b[2]+' '+b[3])
		else:
			print('You have no reservation yet!')
	else:
		print('You have not logged in, please login to see your reservations!')

while True:
	a = list(map(str, input().strip().split()))
	if a[0] == 'REGISTER':
		REGISTER(a[1], a[2])
	elif a[0] == 'LOGIN':
		LOGIN(a[1], a[2])
	elif a[0] == 'DELETE':
		DELETE(a[1], a[2])
	elif a[0] == 'VIEW':
		if a[1] == 'CINEMAS':
			VIEW_CINEMAS()
		elif a[1] == 'ALL':
			if a[2] == 'MOVIES' and a[3] == 'OF':
				VIEW_ALL_MOVIES(a[4])
			elif a[2] == 'SANS' and a[3] == 'OF':
				VIEW_ALL_SANS(a[4], a[5])
	elif a[0] == 'PURCHASE':
		PURCHASE(a[1], a[2], a[3], a[4], a[5])
	elif a[0] == 'SEE' and a[1] == 'MY' and a[2] == 'RESERVATIONS':
		SEE_MY_RES()
	elif a[0] == 'QUIT':
		db.db.close()
		cinema_db.db.close()
		print('GOODBYE.')
		break
	else:
		print('There is no such command!!')