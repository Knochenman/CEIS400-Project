# • Reduce amount of processing time to check out tool to less 2 minutes 
#       user needs to be indexed to have fast processing time, toolID is also going to be indexed.
#       check if instock toolName in warehouseInventory, decrement inStock, increment employeeInventory
# •	Reduce amount of processing time of employee termination to less 2 minutes
#         user needs to be indexed to have fast processing time
#         tool by tool remove from employee inventory and increment warehouseInventory
# •	Less than 30 seconds to locate employee to whom the returned equipment belongs 
#           Index date to improve searching time in combination with toolID to see who has checked out X tool.
# •	System will validate that employee has proper skill classification for check out 
#           when checking out tool look up wareHouseInventory and Compare SkillID with ToolID for proper check
# •	Automated notification system upon equipment arrival/check-in 
#           print user turned in X tools and date and time it, commit this to records
# •	Staff has ability to obtain and create immediate access to records and reports 
#           staff can view logs and add/remove/update reports
# •	Provide each employee with periodic statement of their inventory and actions
#           create a table just for reports to keep track of current inventory, can possibly display reports on login of last report
# •	Classify employees based on good or bad standing according to equipment losses
#           # > 5 tools = bad standing 
#   Create GUI

import mysql.connector
from mysql.connector import Error

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'GB_Manufacturing Dashboard' #usedpythonspot.com to build interface
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        button = QPushButton('Employee Full Names', self)
        button.setToolTip('Will display all employees full names')
        button.move(100,100)
        button.clicked.connect(self.on_click)

        button = QPushButton('Install Database', self)
        button.setToolTip('Drops and Installs Database')
        button.move(100,70)
        button.clicked.connect(self.on_click_install)

        button = QPushButton('Withdraw Tools', self)
        button.setToolTip('Withdraw tools')
        button.move(100,130)
        button.clicked.connect(self.on_click_withdraw)
        
        button = QPushButton('Return Tools', self)
        button.setToolTip('Return tools')
        button.move(100,160)
        button.clicked.connect(self.on_click_return)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(460, 20)
        self.textbox.resize(140,20)
        
        # Create a button in the window
        self.button = QPushButton('Search', self)
        self.button.move(459,40)
        
        # connect button to function on_click
        self.button.clicked.connect(self.on_click_search)


        self.listwidget = QListWidget()
        self.listwidget.move(460, 60)
        self.listwidget.resize(140,60)
        self.show()
        self.listwidget.show()



    @pyqtSlot()
    def on_click(self):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                database='gb_manufacturing2',
                                                user='root',
                                                password ='password')
            
            #dumps all employee last names (Index1) #basic read from database can be manipulated later for other functions                            
            print (connection)
            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)  #dictionary allows us to use variable names rather than using record [1] index 1 to pull up lastNames
                query = """select * from employee;"""
                cursor.execute(query)
                records = cursor.fetchall()
                #print (records)
                for record in records:
                    #if you want just a full record dump, do just record
                    print (record["empFirstName"], record["empLastName"])

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
#stub functions to be filled out later
    def on_click_withdraw(self):
        print ("Withdraw")
    def on_click_return(self):
        print ("Return")


    def on_click_search(self):
        try:
            connection = mysql.connector.connect(host='localhost',
                                                database='gb_manufacturing2',
                                                user='root',
                                                password ='password')
            #function for search bar to select all things from employee LIKE what they're searching for                        
            #print (self.textbox.text()) #just prints what we're searching for.
            if connection.is_connected():
                cursor = connection.cursor()
                query = """select * from employee where empFirstName =%s"""
                #query = """select * from employee where empFirstName = "[{empFirstName}]";""".format(self.textbox.text(), 2) ##this works but it is vulnerable to SQL injections so the line above is safer.
                cursor.execute(query, (self.textbox.text(), ))                                    
                records = cursor.fetchall()
                #print (records)  #prints all the records for anyone named Mack
                for record in records:
                    print (record)
                    self.listwidget.addItem(record[1]+" "+record[2]) #Will display search results in QTwidget box for index 1 and 2
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    ##This is a button to install the database GB_Manufacturing2
    def on_click_install(self):
        print('Installing GB_Manufacturing2 Database')
        try:
            connection = mysql.connector.connect(host='localhost',
                                                user='root',
                                                password ='password')
                                        
            print (connection)
            if connection.is_connected():
                cursor = connection.cursor()
                query = """DROP DATABASE IF EXISTS gb_manufacturing2;"""
                cursor.execute(query)
                query = """CREATE DATABASE gb_manufacturing2;""" 
                cursor.execute(query)
                #add error handling
                connection.commit()
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
        try:
            connection = mysql.connector.connect(host='localhost',
                                                database='gb_manufacturing2',
                                                user='root',
                                                password ='password')
            #create and populate the employee table.                            
            print (connection)
            if connection.is_connected():
                cursor = connection.cursor()
                query = """create table employee(
                            empID varchar(3),
                            empLastName varchar(15) not null,
                            empFirstName varchar(15) not null,
                            SkillID varchar(15),
                            numTools int not null,
                            isStaff int not null,
                            primary key (empID)
                        );"""
                cursor.execute(query)
                query = """INSERT INTO employee (empID, empLastName,empFirstName,SkillID, numTools, isStaff)
                            VALUES
                                ('E1', 'Najorka', 'Mack', 'M1', 0, 1),
                                ('E2', 'Cousar', 'Ronell', 'C1', 0, 1),
                                ('E3', 'Rundio', 'Jacob', 'M1', 0, 0),
                                ('E4', 'Hall', 'Randel', 'C1', 0, 1),
                                ('E5', 'Baity', 'Brittany', 'C1', 0, 0);"""
                cursor.execute(query)


                query = """ create table WareHouseInventory(
                                SkillID varchar (15),
                                toolID varchar (4),
                                toolName varchar (20),
                                inStock int not null,
                                primary key (toolID)
                            );"""
                cursor.execute(query)
                query = """INSERT INTO WareHouseInventory (SkillID, toolID, toolName, inStock) VALUES
                                ("M1", "T1", "Impact Wrech", 100),
                                ("All", "T2", "Skrewdriver", 100),
                                ("All", "T3", "Shakeweight", 10),
                                ("C1", "T4", "Table Saw", 50);"""

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                connection.commit()
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

