#import libraries.
import sqlite3
import os.path
from faker import Faker 
import string 
import random
import datetime


#call faker.
f = Faker()
f.name()


#create a database. 
db_name="Charger_Company.db"
dir='.'
db=os.path.join(dir,db_name)
conn=sqlite3.connect("Charger_Company.db")
c=conn.cursor()


#create table using sqlite3.
#table for Customer.
def Customer():
    with conn:
        c.execute(""" CREATE TABLE IF NOT EXISTS Customer 
        (
            id	TEXT NOT NULL,
	        station_name_code	TEXT NOT NULL,
	        first_name	VARCHAR(20) NOT NULL,
	        last_name	VARCHAR(20) NOT NULL,
            number	TEXT NOT NULL,
	        email	TEXT,
	        time	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
	        date	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
			PRIMARY KEY (id),
	        FOREIGN KEY(station_name_code) REFERENCES Charging_station(name_code)
			ON DELETE SET NULL ON UPDATE CASCADE,
			CONSTRAINT id_c	UNIQUE  (id) ,
			CONSTRAINT number_c	UNIQUE  (number),
			CONSTRAINT email_c	UNIQUE  (email) 
            ) """)


#table for Electric cars.
def El_Car():
     with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS El_Car
        (
	        license_plate	TEXT NOT NULL,
	        id 	TEXT NOT NULL UNIQUE,
	        brand	TEXT NOT NULL,
	        type	TEXT NOT NULL,
	        FOREIGN KEY(id) REFERENCES customer(id)
			ON DELETE SET NULL ON UPDATE CASCADE,
	        PRIMARY KEY(license_plate)
			CONSTRAINT license_plate_E	UNIQUE  (license_plate)
			)""")


#table for Payment.
def Payment():
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS Payment
        (
	        id TEXT NOT NULL,
	        charger_code   TEXT NOT NULL,
	        sale_promo_code	TEXT,
	        method	TEXT NOT NULL,
	        FOREIGN KEY(id) REFERENCES user(id)
			ON DELETE SET NULL ON UPDATE CASCADE,
	        FOREIGN KEY(charger_code) REFERENCES charger(code)
			ON DELETE SET NULL ON UPDATE CASCADE,
	        PRIMARY KEY(id,charger_code )
			CONSTRAINT sale_promo_code_P UNIQUE  (sale_promo_code)
			CONSTRAINT pay_method CHECK (method in ('Cash','Card'))
			 )
            """)


#table for Charging station.
def Charging_station():
    with conn:
         c.execute("""CREATE TABLE IF NOT EXISTS Charging_station
          (
	            name_code	TEXT NOT NULL,
	            pluscode	TEXT NOT NULL,
	            FOREIGN KEY(pluscode) REFERENCES location(pluscode)
				ON DELETE SET NULL ON UPDATE CASCADE,
	            PRIMARY KEY(name_code, pluscode) 
				CONSTRAINT name_code_Cs UNIQUE (name_code)
			
				
				)
            """ ) 


#table for Charger.
def Charger():
    with conn:
        c.execute( """CREATE TABLE IF NOT EXISTS Charger 
        (
	        code	TEXT NOT NULL,
	        type	TEXT NOT NULL,
	        cost	REAL NOT NULL,
	        PRIMARY KEY(code)
			CONSTRAINT code_Ch UNIQUE (code)
			CONSTRAINT Ch_type CHECK (type IN ('Mennekes','CCS')),
			CONSTRAINT Cost_ch CHECK (cost IN	(0.2,0.6))
            )""" )


#table for Books.
def Books():
    with conn:
        c.execute( """ CREATE TABLE IF NOT EXISTS Books(
	                id	TEXT NOT NULL,
	                charger_code	ΤΕΧΤ NOT NULL,
	                book_time	TEXT DEFAULT CURRENT_TIMESTAMP,
	                date	TEXT DEFAULT CURRENT_TIMESTAMP,
	                FOREIGN KEY(id) REFERENCES Customer(id)
					ON DELETE SET NULL ON UPDATE CASCADE,
	                FOREIGN KEY(charger_code) REFERENCES Charger(code)
					ON DELETE SET NULL ON UPDATE CASCADE,
	                PRIMARY KEY(id,charger_code)
                )""")


#table for Location.
def Location():
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS Location
        (   pluscode 	TEXT NOT NULL,
            city	TEXT NOT NULL,
            PRIMARY KEY(pluscode)
			CONSTRAINT pluscode_L UNIQUE  (pluscode)
			)"""
        )


#table for Has.       
def Has():
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS Has (
            station_name_code	TEXT NOT NULL,
            charger_code	TEXT NOT NULL,
            booked	ΤΕΧΤ,
            out_of_order	TEXT,
            PRIMARY KEY(station_name_code,charger_code),
            FOREIGN KEY(station_name_code) REFERENCES Station(name_code)
			ON DELETE SET NULL ON UPDATE CASCADE,
            FOREIGN KEY(charger_code) REFERENCES Charger(code)
			ON DELETE SET NULL ON UPDATE CASCADE,
			CONSTRAINT booked_chk CHECK	(booked IN	('yes','no')),
			CONSTRAINT ofo_chk CHECK (out_of_order IN	('yes','no'))

			)
			""" )

		
#table for Charging.
def Charging():
    with conn:
        c.execute(""" CREATE TABLE IF NOT EXISTS Charging (
	license_plate	TEXT NOT NULL,
	charger_code	TEXT NOT NULL,
	charging_time	TEXT DEFAULT CURRENT_TIMESTAMP,
	voltage	REAL NOT NULL,
	power	REAL NOT NULL,
	FOREIGN KEY(license_plate) REFERENCES El_Car(license_plate)
	ON DELETE SET NULL ON UPDATE CASCADE,
	FOREIGN KEY(charger_code) REFERENCES Charger(code)
	ON DELETE SET NULL ON UPDATE CASCADE,
	PRIMARY KEY(license_plate,charger_code)
) """)


#fuctions to insert data into tables using sqlite3.
def Insert_Customers(id,station_name_code,first_name,last_name,number,email,Ctime,Cdate):
	with conn:
		c.execute("INSERT OR IGNORE INTO Customer VALUES (?,?,?,?,?,?,?,?)",(id,station_name_code,first_name,last_name,number,email,Ctime,Cdate))

def Insert_El_Car(license_plate,id,brand,type):
	with conn:
		c.execute("INSERT OR IGNORE INTO El_Car VALUES (?,?,?,?)",(license_plate,id,brand,type))

def Insert_Payment(id,charger_code,promo_code, method):
	with conn:
		c.execute("INSERT OR IGNORE INTO Payment VALUES (?,?,?,?)",(id,charger_code, promo_code, method))

def Insert_Charging_station(name_code,pluscode):
	with conn:
		c.execute("INSERT OR IGNORE INTO Charging_station VALUES (?,?)",(name_code, pluscode))

def Insert_Charging(license_plate, charger_code, charging_time, voltage, power):
	with conn:
		c.execute("INSERT OR IGNORE INTO Charging VALUES (?,?,?,?,?)",(license_plate, charger_code, charging_time, voltage, power))

def Insert_Charger(code, charger_type, cost):
	with conn:
		c.execute("INSERT OR IGNORE INTO Charger VALUES (?,?,?)",(code, charger_type, cost))

def Insert_Books(id,charger_code,book_time, date):
	with conn:
		c.execute("INSERT OR IGNORE INTO Books VALUES (?,?,?,?)",(id,charger_code, book_time, date))

def Insert_Location(pluscode, city):
	with conn:
		c.execute("INSERT OR IGNORE INTO Location VALUES (?,?)",(pluscode, city))

def Insert_Has(station_name_code, charger_code, booked, out_of_order):
	with conn:
		c.execute("INSERT OR IGNORE INTO Has VALUES (?,?,?,?)",(station_name_code, charger_code, booked, out_of_order))


#lists we need for the functions.
yes_no = ["yes", "no"] 
Charger_Types= ["Mennekes", "CCS"]
EC_Types = ["HEV","PHEV", "BEV", "FCEV"]
methodofpayment = ["Cash", "Card"]
cities = ["Athens","Thessaloniki", "Patras", "Ioannina", "Pireas", "Larissa", "Heraklion", "Nafplion", "Kalamata", "Volos",  "Komotini","Trikala", "Alexandroupoli"]


#a function that creates random id with 2 letters, a space and 6 numbers.
def create_id(i):
	id=[]
	for j in range(i):
		id_letters =''.join(random.choice(string.ascii_uppercase) for i in range(2))
		id_nums=''.join(random.choice(string.digits) for i in range(6))
		id_creator=(id_letters+" "+id_nums)
		id.append(id_creator)
	return id


#a function that creates random first names.
def create_names(i):
	for j in range(i):
		name_gen=f.first_name()
		return name_gen


#a function that creates random emails depending on the first name.
def create_email(name,i):
	email=[]
	for j in range(i):
		email_gen=name+str(f.random_int(min=0, max=100))+"@"+ f.free_email_domain()
		email.append(email_gen)
	return email


#a function that returns a random choice from a list.
def create_random_choice (lista,i):
	lista2=[]
	for j in range(i):
		lista2.append(random.choice(lista))
	return lista2


#create random license plate codes.
def create_license_plate(users):
	for j in range (users):
		license_plate= f.license_plate()
	return license_plate


#a function that returns a random choice.
def choose_random(funct):
	return	random.choice(funct)


#a function that randomly chooses if a charger is booked or not and prevents an out of order charger to be booked.
def bkd(outoforder):
	if outoforder =='yes':
		return 'no'
	return random.choice(yes_no)


#a function that returns random specific pluscodes depending on the city.
def plus_codes(city):
	plus_codes=[["XMJH+HM", "XP5Q+52", "XQM5+5P", "XQM9+WC", "2P58+HW", "XPR5+WP", "2P5C+28", "2P2X+F3", "XPMP+27", "XPHF+XQ"], ["JWRR+PV", "JWVQ+66", "JXR2+R5", "JWRQ+XW", "JWRX+3V", "JWQP+PW", "JXQ2+J5"],
				["6PWM+V4", "6PXM+9M", "6PXP+7R", "6PWR+55", "6PWQ+9F"], ["MV83+QF","MV83+MV"], ["WJRX+59", "WMR6+HH"],	["JCWF+XP"], ["84RR+4R", "84QX+3M"], ["HR7G+G6"],
				["24P7+XM","24Q6+9M"],["9X92+4J","9X95+22"],["4CF3+4M"] ,["HQ49+WM"], ["RVXF+33"]]

	if city=="Athens":
		return (random.choice(plus_codes[0]))
	elif city=="Thessaloniki":
		return (random.choice(plus_codes[1]))
	elif city=="Patras":
		return (random.choice(plus_codes[2]))
	elif city=="Ioannina":
		return (random.choice(plus_codes[3]))
	elif city=="Pireas":
		return (random.choice(plus_codes[4]))
	elif city=="Larissa":
		return (random.choice(plus_codes[5]))
	elif city=="Heraklion":
		return (random.choice(plus_codes[6]))
	elif city=="Nafplion":
		return (random.choice(plus_codes[7]))
	elif city=="Kalamata":
		return (random.choice(plus_codes[8]))
	elif city=="Volos":
		return (random.choice(plus_codes[9]))
	elif city=="Komotini":
		return (random.choice(plus_codes[10]))
	elif city=="Trikala":
		return (random.choice(plus_codes[11]))
	elif city=="Alexandroupoli":
		return (random.choice(plus_codes[12]))


#a function that returns random specific station names depending on the city.
def stations_city(city):
	stations=[["Station1", "Station2", "Station3", "Station4", "Station5", "Station6", "Station7", "Station8", "Station9", "Station10"], ["Station11", "Station12", "Station13", "Station14", "Station15", "Station16", "Station17"],
				["Station18", "Station19", "Station20", "Station21", "Station22"], ["Station23","Station24"], ["Station25", "Station26"],	["Station27"], ["Station28", "Station29"], ["Station30"],
				["Station31","Station32"],["Station33","Station34"],["Station35"] ,["Station36"], ["Station37"]]

	if city=="Athens":
		return (random.choice(stations[0]))
	elif city=="Thessaloniki":
		return (random.choice(stations[1]))
	elif city=="Patras":
		return (random.choice(stations[2]))
	elif city=="Ioannina":
		return (random.choice(stations[3]))
	elif city=="Pireas":
		return (random.choice(stations[4]))
	elif city=="Larissa":
		return (random.choice(stations[5]))
	elif city=="Heraklion":
		return (random.choice(stations[6]))
	elif city=="Nafplion":
		return (random.choice(stations[7]))
	elif city=="Kalamata":
		return (random.choice(stations[8]))
	elif city=="Volos":
		return (random.choice(stations[9]))
	elif city=="Komotini":
		return (random.choice(stations[10]))
	elif city=="Trikala":
		return (random.choice(stations[11]))
	elif city=="Alexandroupoli":
		return (random.choice(stations[12]))


#a function that chooses randomly between the two types of chargers.
def Charger_type():
	ctype=["Mennekes", "CCS"]
	return str(random.choice(ctype))


#a function that returns random valid voltage values depending charger type.
def Volts(charger_type):
	AC=["208","240"]
	DC=[]
	create_dc_values=f.random_int(min=200, max=600)
	DC.append(create_dc_values)
	if charger_type=="Mennekes":
		return str(random.choice(AC))
	elif charger_type=="CCS":
		return str(random.choice(DC))


#a function that returns random valid power values depending charger type.
def Power(charger_type):
	AC=[]
	DC=[]
	create_ac_values=f.random_int(min=7, max=19)
	create_dc_values=f.random_int(min=50, max=350)
	DC.append(create_dc_values)
	AC.append(create_ac_values)
	if charger_type=="Mennekes":
		return str(random.choice(AC))
	elif charger_type=="CCS":
		return str(random.choice(DC))


#a function that returns cost values depending charger type.
def charger_cost(charger_type):
	ac_cost=0.20
	dc_cost=0.60
	if charger_type=="Mennekes":
		return ac_cost
	elif charger_type=="CCS":
		return dc_cost


#a function that returns car brands depending their electric car type.
def brands_from_type(Car_type):
	EC_Brands = ["Audi e-tron GT", "Audi e-tron", "Mercendes-Benz EQS", "TESLA Model  S", "TESLA Model X", "TESLA Model 3", "PORCHE Taycan", "LUCID Air Pure", "JAGUAR I-Pace*",
	 	  "Polestar Polestar 2", "Ford Mustang March-E-RWD", "HYUNDAI Ioniq 5","HYUNDAI Kona Electric", "Volkswagen ID.4*", "KN Niro EV", "NISSAN Leaf" ]
	if Car_type=="BEV":
		return(random.choice(EC_Brands))
	elif Car_type=="PHEV":
		return "VOLVO C40 Recharge"
	elif Car_type=="HEV":
		return "CHEVROLET Bolt EUV"
	elif Car_type=="FCEV":
		return "GMC Hammer EV Pickup"


#a function that returns the charge time depending the charger type.
def charge_time(charger_type):
	if charger_type=="Mennekes":
		H=f.time("%H")
		M=f.time("%M")
		S=f.time("%S")
		return(H +":" +  M + ":" + S)

	elif charger_type=="CCS":
		H="00"
		M=f.time("%M")
		S=f.time("%S")
		
		return(H +":" +  M + ":" + S)


#a function that returns a random promo code or null.
def promo_code():
	promo=[]
	promo_code =  "".join(random.choice(string.digits) for i in range(5))
	Null=("null")
	promo.append(Null)
	promo.append(promo_code)
	return str(random.choice(promo))


#a function that returns random charger codes.
def chargers(i):
	r=(i/10)
	for i in range(1,int(r)):
		charger_code='C'+str(random.randint(1,100))
		return charger_code

#a function that makes a list, append charger codes from the previous function and then returns them.
def charge_car(ch,i):
	chargs=[]
	for j in range(i):
		chargs.append(ch)
	return chargs


#function that deletes all tables
def delete():
	with conn:
		c.execute("DELETE  FROM Customer ")
		c.execute("DELETE  FROM El_Car ")
		c.execute("DELETE  FROM Payment ")
		c.execute("DELETE  FROM Location ")
		c.execute("DELETE  FROM Books ")
		c.execute("DELETE  FROM Has ")
		c.execute("DELETE  FROM Charging_station ")
		c.execute("DELETE  FROM Charger ")
		c.execute("DELETE  FROM Charging ")


#calling the functions that create the tables.
Customer()
El_Car()
Payment()
Charging_station()
Charging()
Charger()
Location()
Books()
Has()


#create random dates between 2022, 1, 1 - 2022, 12, 31 .
f.date_between(datetime.date(2022, 1, 1),datetime.date(2022, 12, 31))


#users in the database,must be 20 or more users to start generating data.
users=20

for i in range(users): 

#variables. 
	id = create_id(users)

	date=f.date_between(datetime.date(2022, 1, 1),datetime.date(2022, 12, 31))
    
	names = create_names(users)
	
	license_plate = create_license_plate(users)

	tel_number=f.unique.random_int(min=6911111111, max=6999999999)

	email = create_email(names,users)

	types = create_random_choice (EC_Types,users)

	brands = brands_from_type(types[i])

	method = create_random_choice (methodofpayment,users)

	station_name_code='station'+str(f.random_int(min=1, max=37))

	promocode = promo_code() 

	city = choose_random(cities)

	pluscodes=plus_codes(city)

	out_of_order=choose_random(yes_no)

	booked=bkd(out_of_order)

	charger_code=chargers(users)

	charging_code=charge_car(chargers(users),users)

	visit_time=f.time()

	c_type=Charger_type()

	power=Power(c_type)	

	cost=charger_cost(c_type)

	volts=Volts(c_type)

	time_g=charge_time(c_type)
	

#calling the function that insert data into tables.

	Insert_Customers(id[i],station_name_code,names,f.last_name(),tel_number,email[i],visit_time,date)

	Insert_El_Car(license_plate,id[i],brands,types[i])

	Insert_Payment(id[i],charger_code, promocode, method[i])

	Insert_Charging_station(station_name_code, pluscodes)
	
	Insert_Location(pluscodes, city)

	Insert_Has(station_name_code, charger_code, booked, out_of_order)

	Insert_Charger(charger_code, c_type,cost)

	Insert_Charging(license_plate, charging_code[i], time_g, volts, power)

#creating users who have booked a charger.
for i in range(int(users-(users//2.5))):
	book_time=f.time()
	date=f.date_between(datetime.date(2022, 1, 1),datetime.date(2022, 12, 31))
	charger_code=charge_car(chargers(users),users-int(users//2.5))
	Insert_Books(id[i],charger_code[i], book_time, date)








