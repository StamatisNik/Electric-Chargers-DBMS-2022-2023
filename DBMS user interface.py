#import necessary libraries.
import	PySimpleGUI	as	sg
import	sqlite3
import os
#connect with our database.
conn=sqlite3.connect("Charger_Company.db")
c=conn.cursor()
dir='.'
ic=os.path.join(dir,'lightning.ico')

# a function that inserts data into the table charging station.
def insert_data_Charging_station(name_code,pluscode):
    with conn:
        try:
            conn.execute("INSERT INTO Charging_station VALUES (?,?)",(name_code, pluscode))
        except sqlite3.Error as er: 
            sg.popup_error("Error", er,icon=ic)


# a function that inserts data into the table Location .
def insert_data_Location(pluscode,city):
    with conn:
        try:
            conn.execute("INSERT INTO Location VALUES (?,?)",(pluscode, city))
        
        except sqlite3.Error as er: 
            sg.popup_error("Error", er,icon=ic)


# a function that inserts data into the table Charger.
def insert_data_Charger(code,charger_type, cost):
    with conn:
        try:
            conn.execute("INSERT INTO Charger VALUES (?,?,?)",(code,charger_type,cost))
        except sqlite3.Error as er: 
            sg.popup_error("Error", er,icon=ic)

#queries 
#a query that answers which chargers are out of order.
def broken_chargers_query ():
    with conn:
            c.execute("CREATE INDEX IF NOT EXISTS  Has_Index ON Has(charger_code)")
            c.execute(" SELECT DISTINCT charger_code FROM Has  WHERE out_of_order = 'yes'  ORDER BY charger_code ")
            return c.fetchall() 

#a query that answers which chargers are not  out of order and not booked.
def available_chargers_query():
    with conn:
        c.execute("CREATE INDEX IF NOT EXISTS  Station_Index ON Charging_station(name_code)")
        c.execute( "SELECT station_name_code as Station, COUNT (charger_code) as howmany FROM Has  WHERE out_of_order = 'no' AND booked = 'no' GROUP BY Station ")
        return c.fetchall()


#a query that answers how many cars were charged.
def charge_count_query ():
    with conn:
        c.execute("CREATE  INDEX IF NOT EXISTS  El_Car_Index ON El_Car(license_plate)")
        c.execute("SELECT DISTINCT COUNT(license_plate) as posoi_fortisan FROM Charging ")
        return c.fetchall()


#a query that answers how much energy was consumed in a station.
def power_per_station_query():
    with conn:
        c.execute("CREATE INDEX IF NOT EXISTS  Station_Index ON Charging_station(name_code)")
        c.execute( """SELECT DISTINCT station_name_code as Station,sum(power) as Power 
        FROM (Charging JOIN Charger ON Charging.charger_code=Charger.code )JOIN Has ON Charger.code=Has.charger_code GROUP BY station_name_code """)
        return c.fetchall()


#a query that answers which car type was the most popular.
def most_popular_cartype_query ():
    with conn:
        c.execute("CREATE INDEX IF NOT EXISTS  El_Car_Index ON El_Car(type)")
        c.execute( " SELECT type FROM El_Car GROUP BY type ORDER BY count(type) DESC limit 1 ")
        return c.fetchall()


#a query that answers which city was the most popular.
def popular_locations_query():
    with conn:
        c.execute("CREATE  INDEX IF NOT EXISTS  Customer_Index ON Customer(station_name_code)")
        c.execute( """SELECT  city FROM (Customer JOIN Charging_station on Customer.station_name_code=Charging_station.name_code) as Stations, Location 
                        WHERE  Stations.pluscode=Location.pluscode GROUP BY city ORDER BY count(Location.pluscode) DESC limit 5 """)
        return c.fetchall()


#a query that answers which hours were rush hours.
def rush_hour_query():
    with conn:
        c.execute("CREATE INDEX IF NOT EXISTS  Customer_Index ON Customer(time)")
        c.execute("""SELECT strftime('%H',time) AS Hours FROM Customer GROUP BY strftime('%H',time) ORDER BY count(strftime('%H',time)) DESC LIMIT 3 """)
        return c.fetchall()

#a query that finds a pluscode depending on the city.
def find_pluscodes_query():
    with conn:
        loq2 = [[sg.Text('???????? ????????: ',size=(10,1),font=("Calibri light",17)), sg.InputText(font=("Calibri light",15)), [sg.VPush()]],
            [sg.Submit(key="-SUBMIT-",font=("Calibri",16))],[sg.VPush()] ]
        wq2 = sg.Window("find_pluscodes_query", loq2, size=(250,100))	
        eq2, values = wq2.read()

        if eq2 == sg.WIN_CLOSED :
            wq2.close()

        elif eq2 ==	"-SUBMIT-" :
            c.execute("CREATE INDEX IF NOT EXISTS  Location_Index ON Location(pluscode)")
            c.execute("SELECT pluscode FROM Location WHERE city= ?",(values[0],))
            wq2.close()
            return c.fetchall()

#a query that finds city and  pluscode depending on the station.
def whereisthestation_query():
    with conn:
        loq1 = [[sg.Text('???????? ????????????:',size=(11,1),font=("Calibri light",17)), sg.InputText(font=("Calibri light",16)), [sg.VPush()]],
            [sg.Submit(key="-SUBMIT-",font=("Calibri",16))],[sg.VPush()] ]
        wq1 = sg.Window("whereisthestation_query", loq1, size=(270,100))	
        eq1, values = wq1.read()
    
        if eq1 == sg.WIN_CLOSED :
            wq1.close()

        elif eq1 ==	"-SUBMIT-" :
            c.execute("CREATE INDEX IF NOT EXISTS  Location_Index ON Location(city)")
            c.execute( "SELECT Location.city, Charging_station.pluscode FROM Charging_station JOIN Location ON Charging_station.pluscode = Location.pluscode WHERE Charging_station.name_code = ? ",(str(values[0]),) )
            wq1.close()
            return c.fetchall()

#a function that the user can make a custom query.
def custom_query():
    with conn:
        while True:
            sg.theme("Green")
            layout2=[[sg.Text("??????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15),size=(300,300))],
                    [sg.Submit(key="-SUMBIT-",font=("Calibri",	15))]]
            window2	= sg.Window("??????????????????",icon=ic,size=(800,100)).Layout(layout2)
            event2,value2=window2.read()
            if event2=="-SUMBIT-":
                try:
                    c.execute(str(value2[0]))
                    items=c.fetchall()
                    window2.close()
                    for item in items:
                        sg.Print(item,size=(120,30))
                    window2.close()
                        
                except sqlite3.Error as er:
                    sg.popup_error("Error",er,icon=ic)
                    window2.close()
            elif event2==sg.WIN_CLOSED:
                window2.close()
                break

# a function that deletes data from tables.
def delete_data():
    with conn:
        while True:
            sg.theme("Green")
            layout1	=[[sg.Text('?????????????? ????????????:',font=("Calibri", 15))],	
                [sg.Button("??????????????",size=(13,1),font=("Calibri", 18)) , sg.Button("????.????????????????????",size=(13,1),font=("Calibri", 18)),sg.Button("??????????????",size=(14,1),font=("Calibri", 18))],
                [sg.Button("??????????????",size=(13,1),font=("Calibri", 18)),sg.Button("????????????????",size=(13,1),font=("Calibri", 18)),sg.Button("??????????????????",size=(14,1),font=("Calibri", 18))],
                [sg.Button("??????????????",size=(13,1),font=("Calibri", 18)),sg.Button("??????????????????",size=(13,1),font=("Calibri", 18)),sg.Button("????????????????",size=(14,1),font=("Calibri", 18))]
                ,[sg.Submit(button_text="Apply",button_color="Black",key="Confirm",size=(100,1),font=("Calibri",15)),]]
            window1	= sg.Window("???????????????? ??????????????????",icon=ic,size=(500,270)).Layout(layout1)
            event,value = window1.read()

            if event == "??????????????":
                layout2=[
                [sg.Text("???????? id ????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri",	15))]]
                window2	= sg.Window("???????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout2) 
                event2,value2=window2.read()
                
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Customer_Index ON Customer(id)")
                        c.execute('DELETE  FROM Customer WHERE id=?',(str(value2[0]),))
                        window2.close()
                        window1.close()
                    
                    except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window2.close()
                            window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()

            elif event == "????.????????????????????":
                layout2=[
                [sg.Text("???????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri",15))]]
                window2	= sg.Window("Delete Data",icon=ic, size=(500,100)).Layout(layout2) 
                event2,value2=window2.read()

                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  El_Car_Index ON El_Car(license_plate)")
                        c.execute("DELETE  FROM El_Car WHERE license_plate=?",(str(value2[0]),))
                        window2.close()
                        window1.close()
                        
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()
            
            elif event == "??????????????":
                layout2=[
                [sg.Text("???????? id ????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri ",15))]]
                window2	= sg.Window("???????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout2) 
                event2,value2=window2.read()
                
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Payment_Index ON Payment(id)")
                        c.execute('DELETE  FROM Payment WHERE id=?',(str(value2[0]),))
                        window2.close()
                        window1.close()
            
                                                
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()
                
                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()

            elif event == "??????????????":
                layout2=[
                [sg.Text("???????? ?????????? ??????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri ",	15))]]
                window2	= sg.Window("???????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout2)  
                event2,value2=window2.read()
                
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Station_Index ON Charging_station(name_code)")
                        c.execute("DELETE  FROM Charging_station WHERE name_code=?",(str(value2[0]),))
                        window2.close()
                        window1.close()
            
                                                
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()

            elif event == "????????????????":
                layout2=[
                [sg.Text("???????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri",15))]]
                window2	= sg.Window("???????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout2)  
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Charging_Index ON El_Car(license_plate)")
                        c.execute("DELETE  FROM Charging WHERE license_plate=?",(str(value2[0]),))
                        window2.close()
                        window1.close()

                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()								

            elif event == "??????????????????":
                layout2=[
                [sg.Text("???????? ???????????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri",15))]]
                window2	= sg.Window("???????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout2)  
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Charger_Index ON Charger(code)")
                        c.execute("DELETE  FROM Charger WHERE code=?",(str(value2[0]),))
                        window2.close()
                        window1.close()
                            
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()		

            elif event == "??????????????":
                layout2=[
                [sg.Text("???????? id ????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri",15))]]
                window2	= sg.Window("???????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout2)  
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Books_Index ON Customer(id)")
                        c.execute("DELETE  FROM Books WHERE id=?",(value2[0],))
                        window2.close()
                        window1.close()
                
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()		

            elif event == "??????????????????":
                layout2=[
                [sg.Text("???????? pluscode:",font=("Calibri",15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri",15))]]
                window2	= sg.Window("???????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout2)   
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Location_Index ON Location(pluscode)")
                        c.execute("DELETE  FROM Location WHERE pluscode=?",(str(value2[0]),))
                        window2.close()
                        window1.close()
                                
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()		

            elif event == "????????????????":
                layout2=[
                [sg.Text("???????? ???????????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri",15))]]
                window2	= sg.Window("???????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout2)   
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS Has_Index ON Has(charger_code)")
                        c.execute("DELETE  FROM Has WHERE charger_code=?",(str(value2[0]),))			
                        window2.close()
                        window1.close()
                                                
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()
                        

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()									
                    
            elif event in (sg.WIN_CLOSED, "Confirm"):
                window1.close()
                break

#a function that searches data from tables.
def search_data():
    with conn:
        while True:
            sg.theme("Green")
            layout1	=[[sg.Text('?????? ???????????? ???? ??????????????????????;',font=("Calibri", 15))],	
               [sg.Button("??????????????",size=(13,1),font=("Calibri", 18)) , sg.Button("????.????????????????????",size=(13,1),font=("Calibri", 18)),sg.Button("??????????????",size=(14,1),font=("Calibri", 18))],
                [sg.Button("??????????????",size=(13,1),font=("Calibri", 18)),sg.Button("????????????????",size=(13,1),font=("Calibri", 18)),sg.Button("??????????????????",size=(14,1),font=("Calibri", 18))],
                [sg.Button("??????????????",size=(13,1),font=("Calibri", 18)),sg.Button("??????????????????",size=(13,1),font=("Calibri", 18)),sg.Button("????????????????",size=(14,1),font=("Calibri", 18))]
                ,[sg.Submit(button_text="Back",button_color="Black",key="Confirm",size=(5,1))]]
            window1	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,260)).Layout(layout1) 
            event,value = window1.read()

            if event == "??????????????":
                layout2=[[sg.Text("???????? ????:",font=("Calibri", 15))],
                [sg.Button("Id",size=(13,1),font=("Calibri", 18)),sg.Button("??????????????",size=(13,1),font=("Calibri", 18))]]
                window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(370,100)).Layout(layout2)  
                event2,value2=window2.read()
                if event2=="Id":
                    layout3=[[sg.Text("???????? id:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                    [sg.Submit(key="-SUMBIT-",font=("Calibri",	18))]]
                    window3	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout3)  
                    event3,value3=window3.read()
                    if event3=="-SUMBIT-":
                        try:
                            
                
                            c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Customer_Index ON Customer(id)")
                            c.execute("SElECT * FROM Customer WHERE id =?",(str(value3[0]),))
                            sg.Print(c.fetchall())
                            window3.close()
                            window2.close()
                            window1.close()
                                
                        except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window2.close()
                            window1.close()

                    elif event3 == sg.WIN_CLOSED:
                            window3.close()
                            window2.close()
                            window1.close()
                        

                elif event2=="??????????????":
                    layout3=[[sg.Text("???????? ??????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                    [sg.Submit(key="-SUMBIT-",font=("Calibri",15))]]
                    window3	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout3)  
                    event3,value3=window3.read()
                    if event3=="-SUMBIT-":
                        try:
                            
                
                            c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Customer_Index ON Customer(last_name)")
                            c.execute("SElECT * FROM Customer WHERE last_name =?",(str(value3[0]),))
                            sg.Print(c.fetchall())
                            window3.close()
                            window2.close()
                            window1.close()
                                
                        except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window3.close()
                            window2.close()
                            window1.close()

                    elif event3==sg.WIN_CLOSED:
                            window3.close()
                            window2.close()
                            window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()


            elif event == "????.????????????????????":
                layout2=[[sg.Text("???????? ????:",font=("Calibri", 15))],
                [sg.Button("Id",size=(13,1),font=("Calibri", 18)),sg.Button("????????????????",size=(13,1),font=("Calibri", 18))]]
                window2	= sg.Window("Search Data",icon=ic,size=(370,100)).Layout(layout2)   
                event2,value2=window2.read()
                if event2=="Id":
                    layout3=[[sg.Text("Give id:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                    [sg.Submit(key="-SUMBIT-",font=("Calibri",	15))]]
                    window3	= sg.Window("Search Data",icon=ic,size=(400,100)).Layout(layout3)   
                    event3,value3=window3.read()
                    if event3=="-SUMBIT-":
                        try:
                            
                
                            c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Customer_Index ON Customer(id)")
                            c.execute("SElECT * FROM Customer WHERE id =?",(str(value3[0]),))
                            sg.Print(c.fetchall())
                            window3.close()
                            window2.close()
                            window1.close()
                        except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window3.close()
                            window2.close()
                            window1.close()
                            
                    elif event3==sg.WIN_CLOSED:
                            window3.close()
                            window2.close()
                            window1.close()
                

                elif event2=="????????????????":
                    layout3=[[sg.Text("????????????????:",font=("Calibri",15)),sg.InputText(font=("Calibri light",15))],
                    [sg.Submit(key="-SUMBIT-",font=("Calibri",15))]]
                    window3	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout3)   
                    event3,value3=window3.read()
                    if event3=="-SUMBIT-":
                            
                        try:
                            c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  El_Car_Index ON El_Car(id)")
                            c.execute("SElECT * FROM El_Car WHERE id =?",(str(value3[0]),))
                            sg.Print(print(c.fetchall()))
                            window3.close()
                            window2.close()
                            window1.close()
                                
                        except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window2.close()
                            window1.close()

                    elif event3==sg.WIN_CLOSED:
                            window3.close()
                            window2.close()
                            window1.close()

                if event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()

            elif event == "??????????????":
                layout2=[
                [sg.Text("???????? id ????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri light",15))]]
                window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout2) 
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE   UNIQUE INDEX IF NOT EXISTS  Payment_Index ON Payment(id)")
                        c.execute("SElECT * FROM Payment WHERE id =?",(str(value2[0]),))
                        sg.Print(c.fetchall())
                        window2.close()
                        window1.close()
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()
                                            
                                                

            elif event == "??????????????":
                layout2=[
                [sg.Text("???????? ?????????? ??????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri",	15))]]
                window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout2) 
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Station_Index ON Charging_station(name_code)")
                        c.execute("SElECT * FROM Charging_station WHERE name_code =?",(str(value2[0]),))
                        sg.Print(c.fetchall())
                        window2.close()
                        window1.close()

                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()
                                            

            elif event == "????????????????":
                layout2=[
                [sg.Text("???????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri",	18))]]
                window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout2) 
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Charging_Index ON Charging(license_plate)")
                        c.execute("SElECT *  FROM Charging WHERE license_plate=?",(str(value2[0]),))
                        sg.Print(c.fetchall())	
                        window2.close()
                        window1.close()

                                                
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()
                
                
                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()

            elif event == "??????????????????":
                layout2=[
                [sg.Text("???????? ???????????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri",	18))]]
                window2	= sg.Window("?????????????????? ??????????????????",layout2,size=(500,100)) 
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS Charger_Index ON Charger(code)")
                        c.execute("SElECT * FROM Charger WHERE code=?",(str(value2[0]),))
                        sg.Print(c.fetchall())
                        window2.close()
                        window1.close()
                    
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()


                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()

                
            elif event == "??????????????":
                layout2=[
                [sg.Text("???????? id ????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri",	18))]]
                window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout2) 
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Books_Index ON Books(id)")
                        c.execute("SELECT * FROM Books WHERE id=?",(str(value2[0]),))
                        sg.Print(c.fetchall())	
                        window2.close()
                        window1.close()
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()


                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()
                                                
                
            elif event == "??????????????????":
                layout2=[
                [sg.Text("???????? pluscode:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri",	15))]]
                window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout2) 
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Location_Index ON Location(pluscode)")
                        c.execute("SELECT city FROM Location WHERE pluscode=?",(str(value2[0]),))
                        sg.Print(c.fetchall())	
                        window2.close()
                        window1.close()
                        
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()

            
                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()
                                                
                
            elif event == "????????????????":
                layout2=[
                [sg.Text("???????? ???????????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calbri",	18))]]
                window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,100)).Layout(layout2)  
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Has_Index ON Has(charger_code)")
                        c.execute("SELECT * FROM Has WHERE charger_code =?",(str(value2[0]),))
                        sg.Print(c.fetchall())	
                        window2.close()
                        window1.close()

                    except sqlite3.Error as er:
                        print("Error",er,icon=ic)	

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()
                                                                        
                    
            elif event in (sg.WIN_CLOSED, "Confirm"):
                window1.close()
                break

#a function that gives us every table.
def tables():
    with conn:
        while True:
            sg.theme("Green")
            layout1	=[[sg.Text('???????????????? ????????????:',font=("Calibri", 15))],	
               [sg.Button("??????????????",size=(13,1),font=("Calibri", 18)) , sg.Button("????.????????????????????",size=(13,1),font=("Calibri", 18)),sg.Button("??????????????",size=(14,1),font=("Calibri", 18))],
                [sg.Button("??????????????",size=(13,1),font=("Calibri", 18)),sg.Button("????????????????",size=(13,1),font=("Calibri", 18)),sg.Button("??????????????????",size=(14,1),font=("Calibri", 18))],
                [sg.Button("??????????????",size=(13,1),font=("Calibri", 18)),sg.Button("??????????????????",size=(13,1),font=("Calibri", 18)),sg.Button("????????????????",size=(14,1),font=("Calibri", 18))]
                ,[sg.Submit(button_text="Back",button_color="black",key="Confirm",size=(5,1))]]
            window1	= sg.Window("?????????????? ??????????????",icon=ic,size=(500,250)).Layout(layout1) 
            event,value = window1.read()

            if event =="??????????????":
                    try:
                        c.execute("SELECT * FROM Customer")
                        items=c.fetchall()
                        for item in items:
                            sg.Print(item,size=(120,30))
                            window1.close()
                        
                            

                    except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window1.close()

            elif event == "????.????????????????????":
                    try:
                        c.execute("SELECT * FROM El_Car")
                        items=c.fetchall()
                        for item in items:
                            sg.Print(item,size=(120,30))
                            window1.close()
                        
                    
                    except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window1.close()
                
            elif event == "??????????????":
                    try:
                        c.execute("SELECT * FROM Payment")
                        items=c.fetchall()
                        for item in items:
                            sg.Print(item,size=(120,30))
                            window1.close()
                        
                    
                    except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window1.close()

            elif event == "??????????????":
                    try:
                        c.execute("SELECT * FROM Charging_station")
                        items=c.fetchall()
                        for item in items:
                            sg.Print(item,size=(120,30))
                            window1.close()
                        
                    
                    except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window1.close()

            elif event == "????????????????":
                    try:
                        c.execute("SELECT * FROM Charging")
                        items=c.fetchall()
                        for item in items:
                            sg.Print(item,size=(120,30))
                            window1.close()
                        
                    
                    except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window1.close()
            
            elif event == "??????????????????":
                    try:
                        c.execute("SELECT * FROM Charger")
                        items=c.fetchall()
                        for item in items:
                            sg.Print(item,size=(120,30))
                            window1.close()
                        
                    
                    except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window1.close()
            
            elif event == "??????????????":
                    try:
                        c.execute("SELECT * FROM Books")
                        items=c.fetchall()
                        for item in items:
                            sg.Print(item,size=(120,30))
                            window1.close()
                            
                        
                    
                    except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window1.close()
                
            
            elif event == "??????????????????":
                    try:
                        c.execute("SELECT * FROM Location")
                        items=c.fetchall()
                        for item in items:
                            sg.Print(item,size=(120,30))
                            window1.close()
                        
                    
                    except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window1.close()
            
            elif event == "????????????????":
                    try:
                        c.execute("SELECT * FROM Has")
                        items=c.fetchall()
                        for item in items:
                            sg.Print(item,size=(120,30))
                            window1.close()
                        
                    
                    except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window1.close()
            
            elif event in  (sg.WIN_CLOSED,"Confirm"):
                window1.close()
                break
                 
#a function that updates the data of our tables.
def update_data():
    with conn:
        while True:
            sg.theme("Green")
            layout1	=[[sg.Text('???????? ???????????? ???????????? ???? ??????????????????????;',font=("Calibri", 15))],	
               [sg.Button("??????????????",size=(13,1),font=("Calibri", 18)) , sg.Button("????.????????????????????",size=(13,1),font=("Calibri", 18)),sg.Button("??????????????",size=(14,1),font=("Calibri", 18))],
                [sg.Button("??????????????",size=(13,1),font=("Calibri", 18)),sg.Button("????????????????",size=(13,1),font=("Calibri", 18)),sg.Button("??????????????????",size=(14,1),font=("Calibri", 18))],
                [sg.Button("??????????????",size=(13,1),font=("Calibri", 18)),sg.Button("??????????????????",size=(13,1),font=("Calibri", 18)),sg.Button("????????????????",size=(14,1),font=("Calibri", 18))]
                ,[sg.Submit(button_text="Apply",button_color="Black",key="Confirm",size=(100,1),font=("Calibri",15)),]]
            window1	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,270)).Layout(layout1) 
            event,value = window1.read()

            if event == "??????????????":
                layout2=[
                [sg.Text("???????? id ????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? id ????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ??????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ??????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ????.??????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? email:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri light",15))]]
                window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,300)).Layout(layout2) 
                event2,value2=window2.read()
                
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Customer_Index ON Customer(id)")
                        c.execute("UPDATE Customer SET id=?,first_name=?,last_name=?,number=?,email=? WHERE id=?",(str(value2[1]),str(value2[2]),str(value2[3]),str(value2[4]),str(value2[5]),str(value2[0])) )
                        window2.close()
                        window1.close()
                    
                    except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window2.close()
                            window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()

            elif event == "????.????????????????????":
                layout2=[
                [sg.Text("???????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ?????????? :",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri",	15))]]
                window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,300)).Layout(layout2) 
                event2,value2=window2.read()

                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  El_Car_Index ON El_Car(license_plate)")
                        c.execute("UPDATE El_Car SET license_plate=?,brand=?,type=? WHERE license_plate=?",(str(value2[1]),str(value2[2]),str(value2[3]),str(value2[0])))
                        window2.close()
                        window1.close()
                        
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()
            
            elif event == "??????????????":
                layout2=[
                [sg.Text("???????? id ????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? id:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ???????????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ?????????????????? ????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ???????????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri ",	15))]]
                window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,300)).Layout(layout2) 
                event2,value2=window2.read()
                
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Payment_Index ON Payment(id)")
                        c.execute("Update Payment SET id=?,charger_code=?,sale_promo_code=?,method=? WHERE id=?",(str(value2[1]),str(value2[2]),str(value2[3]),str(value2[4]),str(value2[0])) )
                        window2.close()
                        window1.close()
            
                                                
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()
                        
                
                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()

            elif event == "??????????????":
                layout2=[
                [sg.Text("???????? ?????????? ??????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ?????????? ??????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? pluscode:",font=("Calibri", 15)),sg.InputText(font=("Calibri",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri",15))]]
                window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,300)).Layout(layout2) 
                event2,value2=window2.read()
                
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Station_Index ON Charging_station(name_code)")
                        c.execute("UPDATE Charging_station SET name_code=?,pluscode=? WHERE name_code=?",(str(value2[1]),str(value2[2]),str(value2[0])))
                        window2.close()
                        window1.close()
            
                                                
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()

            elif event == "????????????????":
                layout2=[
                [sg.Text("???????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ???????????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ???????????????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ??????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri ",15))]]
                window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,300)).Layout(layout2) 
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Charging_Index ON El_Car(license_plate)")
                        c.execute("UPDATE Charging SET license_plate=?,charger_code=?,charging_time=?,voltage=?,power=? WHERE license_plate=?",(str(value2[1]),str(value2[2]),str(value2[3]),str(value2[4]),str(value2[5]),str(value2[0])))
                        window2.close()
                        window1.close()

                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()								

            elif event == "??????????????????":
                    layout2=[
                    [sg.Text("???????? ???????????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                    [sg.Text("?????????????????? ???????????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                    [sg.Text("?????????????????? ???????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                    [sg.Text("?????????????????? ????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                    [sg.Submit(key="-SUMBIT-",font=("Calibri",15))]]
                    window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,300)).Layout(layout2) 
                    event2,value2=window2.read()
                    if event2=="-SUMBIT-":
                        try:
                            c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Charger_Index ON Charger(code)")
                            c.execute("UPDATE Charger SET code=?,type=?,cost=? WHERE code=?",(str(value2[1]),str(value2[2]),str(value2[3]),str(value2[0])))
                            window2.close()
                            window1.close()
                            
                                
                        except sqlite3.Error as er:
                            sg.popup_error("Error",er,icon=ic)
                            window2.close()
                            window1.close()

                    elif event2==sg.WIN_CLOSED:
                        window2.close()
                        window1.close()		

            elif event == "??????????????":
                layout2=[
                [sg.Text("???????? id ????????????:",font=("Calibri",15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? id ????????????:",font=("Calibri",15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ???????????? ????????????????:",font=("Calibri",15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ?????? ????????????????:",font=("Calibri",15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ???????????????????? ????????????????:",font=("Calibri",15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri",15))]]
                window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,300)).Layout(layout2) 
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Books_Index ON Books(id)")
                        c.execute("UPDATE Books SET id=?,charger_code=?,book_time=?,date=? WHERE id=?",(str(value2[1]),str(value2[2]),str(value2[3]),str(value2[4]),str(value2[0])))
                        window2.close()
                        window1.close()
                
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()		

            elif event == "??????????????????":
                layout2=[
                [sg.Text("???????? pluscode:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? pluscode:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri light",15))]]
                window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,300)).Layout(layout2) 
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Location_Index ON Location(pluscode)")
                        c.execute("UPDATE Location SET pluscode=?,city=? WHERE pluscode=?",(str(value2[1]),str(value2[2]),str(value2[0])))
                        window2.close()
                        window1.close()
                                
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    window1.close()		

            elif event == "????????????????":
                layout2=[
                [sg.Text("???????? ???????????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ???????????? ????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ?????????? ??????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ????????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Text("?????????????????? ?????????? ??????????????????????:",font=("Calibri", 15)),sg.InputText(font=("Calibri light",15))],
                [sg.Submit(key="-SUMBIT-",font=("Calibri ",	15))]]
                window2	= sg.Window("?????????????????? ??????????????????",icon=ic,size=(500,300)).Layout(layout2) 
                event2,value2=window2.read()
                if event2=="-SUMBIT-":
                    try:
                        c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS  Has_Index ON Has(charger_code)")
                        c.execute("UPDATE Has SET station_name_code=?,charger_code=?,booked=?,out_of_order=? WHERE charger_code=?",(str(value2[1]),str(value2[2]),str(value2[3]),str(value2[4]),str(value2[0])))	
                        window2.close()
                        window1.close()
                                                
                    except sqlite3.Error as er:
                        sg.popup_error("Error",er,icon=ic)
                        window2.close()
                        window1.close()	

                elif event2==sg.WIN_CLOSED:
                    window2.close()
                    
            elif event in (sg.WIN_CLOSED,"Confirm") :
                window1.close()
                break

#making the gui main menu.
sg.theme("Green")
layout = [[sg.Text("Database Management System:",size=(200,1),font=("Calibri light", 20), justification="center")],  [sg.Image( filename= "companylogo.png")],
 [ sg.Button("Start", size=(100, 1),font=("Calibri", 15) )]  ]

window = sg.Window("Database Management System", icon=ic, size=(500,400)).Layout(layout)

while True:
    event, values = window.read()
    if event == "Start" :

        sg.theme('Green')

        lo = [[ sg.Button("??????????????",size=(11,3),font=("Calibri", 30)) , sg.Button("??????????????????",size=(11,3),font=("Calibri", 30))],

            [sg.Button("???????????????? ??????????????????",size=(11,3),font=("Calibri", 19)) , sg.Button("???????????????? ??????????????????",size=(11,3),font=("Calibri", 19)),sg.Button("?????????????????? ??????????????????",size=(11,3),font=("Calibri", 19))],
            [sg.Button("Exit",size=(50,3),font=("Calibri", 15))] ]
        
        win=sg.Window("???????????????? ??????????", icon=ic, size=(500,400)).Layout(lo)

        while True:
            event, values= win.read()

            if event in (sg.WIN_CLOSED , "Exit") :
                win.close()
                break
                
            elif event == "???????????????? ??????????????????" :
                lo1 = [[sg.Text('???? ???????? ???????????? ???????????? ???? ???????????????? ????????????????;',font=("Calibri", 11),size=(30,2))], [sg.Button("??????????????????",size=(26,2),font=("Calibri", 15)) ],
                [sg.Button("??????????????",size=(26,2),font=("Calibri", 15))],
                [sg.Button("??????????????????",size=(26,2),font=("Calibri", 15))],
                [sg.Button("Back",button_color="Black",size=(5,1))] ]
                
                win1=sg.Window("???????????????? ??????????????????",  icon=ic, size=(300,300)).Layout(lo1)

                while True:
                    e, values = win1.read()
                    if e in (sg.WIN_CLOSED , "Back") :
                        win1.close()
                        break

                    elif e == '??????????????????':
                        while True:
                            layout3	=	[	
                            [sg.Text('???????????????? ???????? ????????????????:',font=("Calibri", 18))],	[sg.VPush()],	
                            [sg.Text('??????????????:',size=(10,1),font=("Calibri light",17)),sg.InputText(font=("Calibri light",15))],	[sg.VPush()],	
                            [sg.Text('?????????? ????????????????:',size=(13,1),font=("Calibri light",17)),sg.InputText(font=("Calibri light",15))], [sg.VPush()],	
                            [sg.Text('????????????:',size=(10,1),font=("Calibri light",17)),sg.InputText(font=("Calibri light",15))], [sg.VPush()],	
                            [sg.Submit(key="-SUBMIT-",font=("Calibri",16))],[sg.VPush()] ]	
                            
                            window3	= sg.Window("?????????? ?????????????????? ??????????????????",icon=ic,size=(500,300)).Layout(layout3) 
                            event3, values = window3.read()

                            if event3 == "-SUBMIT-" :
                                insert_data_Charger(values[0],values[1],values[2])
                                window3.close()
                            elif event3 == sg.WIN_CLOSED:
                                window3.close()
                                break
                    elif e == '??????????????????':
                        while True:
                            layout2	=	[	
                            [sg.Text('???????????????? ???????? ????????????????????:',font=("Calibri", 18))],	[sg.VPush()],	
                            [sg.Text('Pluscode:',size=(10,1),font=("Calibri light",17)),sg.InputText(font=("Calibri light",15))],	[sg.VPush()],	
                            [sg.Text('????????:',size=(10,1),font=("Calibri light",17)),sg.InputText(font=("Calibri light",15))], [sg.VPush()],	
                            [sg.Submit(key="-SUBMIT-",font=("Calibri",16))],[sg.VPush()]
                            ]	
                            window2	=	sg.Window("?????????? ?????????????????? ??????????????????",icon=ic,size=(450,250)).Layout(layout2)
                            event2,values = window2.read()	
                            if	event2	==	"-SUBMIT-" :
                                insert_data_Location(values[0],values[1])
                                window2.close()
                            elif event2 == sg.WIN_CLOSED:
                                window2.close()	
                                break

                    elif e == '??????????????':
                        while True:
                            layout1	=	[	
                            [sg.Text('???????????????? ???????? ??????????????:',font=("Calibri", 18))],	[sg.VPush()],	
                            [sg.Text('?????????? ??????????????:',size=(13,1),font=("Calibri light",17)),sg.InputText(font=("Calibri light",15))],	[sg.VPush()],	
                            [sg.Text('Pluscode:',size=(10,1),font=("Calibri light",17)),sg.InputText(font=("Calibri light",15))], [sg.VPush()],	
                            [sg.Submit(key="-SUBMIT-",font=("Calibri",16))],[sg.VPush()]]	
                            window1	= sg.Window("?????????? ?????????????????? ??????????????????",	icon=ic,size=(450,250)).Layout(layout1)
                            event1, values = window1.read()
                            
                            if event1 == "-SUBMIT-" :
                                insert_data_Charging_station(values[0],values[1])
                                window1.close()
                            elif event1 == sg.WIN_CLOSED:
                                window1.close()
                                break
    
            elif event == '??????????????????':
                lo2 = [[sg.Button("?????????????? ??????????????????",size=(20,2),font=("Calibri", 15))],
                    [sg.Button("??????????????????",size=(20,2),font=("Calibri", 15))],
                    [sg.Button("Back",button_color="Black",size=(5,1))] ]
            
                win2 =sg.Window("??????????????????",icon=ic, size=(250,200)).Layout(lo2)	

                while True:	
                    e2, values = win2.read()
                    if e2 in (sg.WIN_CLOSED , "Back") :
                        win2.close()
                        break
    
                    elif e2 == "?????????????? ??????????????????":
                        while True: 
                            lo2a = [[[sg.Button("???????????????????? ??????????????????",size=(22,2),font=("Calibri", 15)), sg.Button("???????????????????? ??????????????????",size=(22,2),font=("Calibri", 15))]],
                                [sg.Button("?????????? ???????????????? ????????????",size=(22,2),font=("Calibri", 15)),sg.Button("5 ?????? ??????????????????   ????????????????????",size=(22,2),font=("Calibri", 15))],
                                [sg.Button("???????????????????? ??????????????????",size=(22,2),font=("Calibri", 15)), sg.Button("?????? ?????????????????? ?????????? ??????????????????????",size=(22,2),font=("Calibri", 15))],
                                [sg.Button("?????? ?????????? ?? ??????????????",size=(22,2),font=("Calibri", 15)), sg.Button("???????? ???? PLUSCODE",size=(22,2),font=("Calibri", 15))],
                                [sg.Button("???????? ????????????",size=(22,2),font=("Calibri", 15)), sg.Button("???????????? ???? ???????? ?????? QUERY",size=(22,2),font=("Calibri", 14))],
                                [sg.Button("Back",button_color="Black",size=(5,1))] ]

                            win2a = sg.Window("??????????????????",icon=ic, size=(500,420)).Layout(lo2a)
                            e2a, values =  win2a.read()
        
                            if e2a in (sg.WIN_CLOSED , "Back") :
                                win2a.close()
                                break
        
                            elif e2a == '???????????????????? ??????????????????':
                                try:
                                    sg.Print(broken_chargers_query())
                                    win2a.close()
                                    break

                                except sqlite3.Error as er: 
                                    win2a.close()
                                    sg.popup_error("Error", er ,icon=ic)

                            elif e2a == "???????????????????? ??????????????????":
                                try:
                                    sg.Print(available_chargers_query())
                                    win2a.close()
                                    break

                                except sqlite3.Error as er: 
                                    sg.popup_error("Error", er,icon=ic)
                               
                            
                            elif e2a == "?????????? ???????????????? ????????????":
                                try:
                                    sg.Print(charge_count_query ())
                                    win2a.close()
                                    break
                                except sqlite3.Error as er: 
                                    sg.popup_error("Error", er,icon=ic)
                                
                        
                            elif e2a ==  "???????????????????? ??????????????????":
                                try:
                                    sg.Print(power_per_station_query())
                                    win2a.close()
                                    break

                                except sqlite3.Error as er:
                                    sg.popup_error("Error", er,icon=ic)

        
                            elif e2a ==  "?????? ?????????????????? ?????????? ??????????????????????":
                                try:
                                    sg.Print(most_popular_cartype_query ())
                                    win2a.close()
                                    break
                                except sqlite3.Error as er:
                                    sg.popup_error("Error", er,icon=ic)
            
                            elif e2a ==  "5 ?????? ??????????????????   ????????????????????":
                                try:
                                    sg.Print(popular_locations_query())
                                    win2a.close()
                                    break 

                                except sqlite3.Error as er:
                                    sg.popup_error("Error", er,icon=ic)
        
                            elif e2a == "???????? ???? PLUSCODE" :
                                try:
                                    sg.Print(find_pluscodes_query())
                                    win2a.close()
                                    break

                                except sqlite3.Error as er:
                                    sg.popup_error("Error", er,icon=ic)

        
                            elif e2a == "?????? ?????????? ?? ??????????????" :
                                try:
                                    sg.Print(whereisthestation_query())
                                    win2a.close()
                                    break
                                except sqlite3.Error as er:
                                    sg.popup_error("Error", er,icon=ic)
                            
                            elif e2a == "???????? ????????????" :
                                try:
                                    sg.Print(rush_hour_query())
                                    win2a.close()
                                    break
                                except sqlite3.Error as er:
                                    sg.popup_error("Error", er,icon=ic)
                            
                            elif e2a == "???????????? ???? ???????? ?????? QUERY" : 
                                win2a.close()
                                custom_query()


                    elif e2 =="??????????????????":
                        search_data()
                
            elif event == "???????????????? ??????????????????":
                delete_data()
        
            elif event == "?????????????????? ??????????????????":
                update_data()
            
            elif event == "??????????????":
                tables()     
    
    elif event == sg.WIN_CLOSED:
        window.close()  
        break 
