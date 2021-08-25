import shelve
class CinemaNotFoundException(Exception):
	def __init__(self, value):
		self.value = value

class MovieNotFoundException(Exception):
	def __init__(self, value):
		self.value = value

class SansNotFoundException(Exception):
	def __init__(self, value):
		self.value = value

class NotEnoughCapacityException(Exception):
	def __init__(self, value):
		self.value = value

# when you are handling query "PURCHASE cinema_name movie_name date sans count" 
# you should use above exceptions instead of doing a lot of if-else statements
# or any other query that these kind of exceptions may occur

class MyDatabase:
	def __init__(self, dbname):
		self.dbname = dbname
		self.db = shelve.open(dbname)
		self.i = -1

	def __iadd__(self, other):
		flag = False
		for obj in list(self.db.keys()):
			if obj == other.name:
				print('Exist!')
				flag = True
				break
		if not flag:
			self.db[other.name] = other
		return self

	def save(self):
		self.db.close()
		self.db = shelve.open(self.dbname)

	def __str__(self):
		a = []
		for obj in list(self.db.keys()):
			a.append('(name='+self.db[obj].name+', '+'password='+self.db[obj].password+')')
		return str(a)

	def __iter__(self):
		return self

	def __next__(self):
		a = list(self.db.keys())
		if self.i >= len(a) - 1:
			raise StopIteration
		self.i += 1
		return self.db[a[self.i]]

	def __getitem__(self, key):
		for obj in list(self.db.keys()):
			if obj == key:
				return self.db[obj]

	def __delitem__(self, obj):
		del self.db[obj.name]
	def delete(self, obj):
		del self.db[obj.name]

class Person:
	def __init__(self, name, password):
		self.name = name
		self.password = password
		self.reservations = []

	def __str__(self):
		return 'name=' + self.name + ', ' + 'password=' + self.password

	def get_name(self):
		return self.name

	def get_password(self):
		return self.password

	def __eq__(self, obj):
		if self.name == obj.name and self.password == obj.password:
			return True
		return False

	def get_reservations(self):
		return self.reservations

class Cinema:
	def __init__(self, name):
		self.name = name
		self.head = None

	def __iadd__(self, movie):
		a = Node(movie)
		a.next = self.head
		self.head = a
		return self

	def __str__(self):
		return self.name

	def get_name(self):
		return self.name

class Movie:
	def __init__(self, name):
		self.name = name
		self.head = None

	def __iadd__(self, sans):
		a = Node(sans)
		a.next = self.head
		self.head = a
		return self

	def __str__(self):
		return self.name

class Sans:
	def __init__(self, date, hour):
		self.date = date
		self.hour = hour


db = MyDatabase(dbname="persons") # should open shelve with this filename
person = Person(name="nima", password="vahdat")
print(person) # -> "name=username1, password=password1"
db += person # should add this person to database
             # should prevent from adding the same person twice (repetitive usernames not allowed)
db.save() # should save current state of this (persons) database using shelve

# MyDatabase can be used for any object that has get_name() method
# for simplicity we use "name" instead of username for class Person
# to be able to use it in MyDatabase
# later in this file you will see that Cinema has get_name() as well

db += person
db += person
print('here1')
print(db) 
p2 = Person(name="u2", password="p2")
print('here2')
db += p2

print(db)
if person in db:
	print("{} exists in db".format(person))
db.i = -1
if person not in db: 
	print("{} does not exist in db".format(person))
db.i = -1
for person in db: 
	print(person)
db.i = -1
print(person.get_name())
print(person.get_password())

if db[person.get_name()] == person: 
	pass                              

if person == db[person.get_name()]: 
	pass

class Node:
	def __init__(self, _value):
		self.value = _value
		self.next = None

head = Node(1)
head.next = Node(2)
head.next.next = Node(3)
head.next.next.next = Node(5)

it = head
while it != None:
	print(it.value)
	it = it.next

# prints 1 2 3 5

cinema = Cinema(name="Azadi")
movie = Movie(name="God_Father")
sans = Sans(date="Saturday 15-11-2019", hour="15-17")
movie += sans
cinema += movie

cinema_db = MyDatabase(dbname="cinemas")
cinema_db += cinema
cinema_db.save()
print(person.get_reservations()) 


print(cinema_db['Azadi'].head.value)#___________Here