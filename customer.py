import pymysql
import re
from time import gmtime, strftime
import sys
from transactions import transactions

class cust_login:
        def signin(self):
            db = pymysql.connect("localhost","root","","login" )
            cursor = db.cursor()
            id=input("ENTER YOUR CUSTOMER ID :: ")
            sql="""SELECT CUST_ID FROM LOGIN_INFO WHERE CUST_ID=%s"""
            data=(id)
            x=cursor.execute(sql,data)
            if x>=1:
                db1 = pymysql.connect("localhost","root","","banking_system" )
                cursor1 = db1.cursor()
                sql="""SELECT CUST_ID FROM transaction WHERE CUST_ID=%s AND (acc_close='YES' OR blocked='YES')"""
                data=(id)
                n=cursor1.execute(sql,data)
                if n>=1:
                    print("Your account may be closed or blocked.")
                    print("\n")
                else:
                    var=1
                    c=0
                    t=1
                    if(x>=1):
                        password=input("PLEASE ENTER YOUR PASSWORD :: ")
                        while var==1:
                            sql="""SELECT CUST_ID FROM LOGIN_INFO WHERE PASSWORD=%s"""
                            data=(password)
                            x=cursor.execute(sql,data)
                            if(x>=1):
                                print("::: SUCCESSFULLY LOGGED IN :::")
                                ob=transactions()
                                while t==1:
                                    print("1.ADDRESS UPDATE\n2.DEPOSIT\n3.WITHDRAW\n4.PRINT STATEMENT\n5.TRANSFER MONEY\n6.ACCOUNT CLOSE\n7.LOG OUT")
                                    opt=int(input("Choose your option"))   
                                    if opt==1:
                                        ob.address_update(id)
                                    if opt==2:
                                        ob.deposit(id)
                                    elif opt==3:
                                        ob.withdraw(id)
                                    elif opt==4:
                                        ob.print_statement(id)
                                    elif opt==5:
                                        ob.transfer_money(id)
                                    elif opt==6:
                                        ob.acc_close(id)
                                    elif opt==7:
                                        print("::: SUCCESSFULLY LOGGED OUT :::")
                                        db1.commit()
                                        db1.close()
                                        t=3
                                    else:
                                        print("Invalid option!")
                                    var=2
                            else:
                                c=c+1
                                print("Password is not correct")
                                print("CAUTION :: YOU WILL BE BLOCKED AFTER 3 WRONG INPUTS!")
                                password=input("Please re-enter your correct password :: ")
                            if c==2:
                                sql="UPDATE transaction SET BLOCKED=%s WHERE cust_id=%s"
                                data=("YES",id)
                                x=cursor1.execute(sql,data)
                                if x>=1:
                                    print("::: BLOCKED :::")
                                break
            else:
                print("Customer Id is Incorrect !")
            db.close()
        def signup(self):
            showtime=strftime("%Y-%m-%d %H:%M:%S",gmtime())
            db = pymysql.connect("localhost","root","","banking_system")
            db1 = pymysql.connect("localhost","root","","login")
            cursor = db.cursor()
            cursor1 = db1.cursor()
            sql="SELECT cust_id,COUNT(*) FROM cust_info"
            cursor.execute(sql)
            t=cursor.fetchone()[1]
            cust_id=t+1
            print("YOUR CUSTOMER ID IS :: ",cust_id) 
            p = re.compile('[a-zA-Z0-9]')
            z=1
            while z==1:
                pwd= input("PLEASE ENTER YOUR PASSWORD :: ")
                if len(pwd)>=8:
                    if re.search(p, pwd):
                        z=0
                        print('::: PASSWORD SET :::') 
                    else:
                        print("Invalid password!")  
                else:
                    print("Enter more than 8 characters!")
            var=1
            while var==1:
               fn=input("Please enter your First name :: ")
               if(fn==""):
                   var=1
               else:
                   var=2
            var=1
            while var==1:
                ln=input("Please enter your Last name :: ")
                if(ln==""):
                    var=1
                else:
                    var=2
            var=1
            addr=input("Please enter your Address :: ")
            pin=input("Please enter your Pin code :: ")
            city=input("Please enter your city :: ")
            while var==1:
                acctype=input("enter account type ::")
                if(acctype==""):
                    var=1
                else:
                    var=2
            sql="INSERT INTO login_info VALUES(%s,%s)"
            data=(cust_id,pwd)
            x=cursor1.execute(sql,data)
            if acctype=='savings':
                sql="""INSERT INTO cust_info VALUES(%s,%s,%s,%s,%s,%s,%s,0)"""
                data=(cust_id,fn,ln,addr,pin,city,acctype)
                x=cursor.execute(sql,data)
                sql="INSERT INTO transaction VALUES(%s,0,0,0,0,'"+showtime+"','NO','NO')"
                data=(cust_id)
                x=cursor.execute(sql,data)
                if x==1:
                    print(":: Details inserted ::")
                else:
                    print(":: Error in insertion ::")
            else:
                sql="""INSERT INTO cust_infO VALUES(%s,%s,%s,%s,%s,%s,%s,0)"""
                data=(cust_id,fn,ln,addr,city,pin,acctype)
                x=cursor.execute(sql,data)
                sql="INSERT INTO transaction VALUES(%s,0,0,0,0,'"+showtime+"','NO','NO')"
                data=(cust_id)
                x=cursor.execute(sql,data)
                if x==1:
                    print(":: Details inserted ::")
                else:
                    print(":: Error in insertion ::")
            db.commit()
            db1.commit()
            db.close()
            db1.close()
        def admin_login(self):
            db = pymysql.connect("localhost","root","","admin" )
            cursor = db.cursor()
            db1 = pymysql.connect("localhost","root","","banking_system" )
            cursor1 = db1.cursor()
            db2 = pymysql.connect("localhost","root","","login" )
            cursor2 = db2.cursor()
            id=input("Enter Admin Id :: ")
            pwd=input("Enter admin password ::")
            sql="SELECT admin_id FROM admin_info WHERE admin_id=%s"
            data=(id)
            x=cursor.execute(sql,data)
            if x==1:
                sql="SELECT password FROM admin_info WHERE password=%s"
                data=(pwd)
                x=cursor.execute(sql,data)
                if x==1:
                    print("ADMIN IS LOGGED IN NOW!")
                    tmp=1
                    while tmp==1:
                        print("1.Print closed accounts\n2.Admin logout")
                        opt=int(input("enter option"))
                        if opt==1:
                            sql="SELECT * FROM cust_info,transaction WHERE cust_info.CUST_ID=transaction.CUST_ID AND transaction.ACC_CLOSE='YES'"
                            x=cursor1.execute(sql)
                            if x>=1:
                                lst=cursor1.fetchall()
                                for i in lst:
                                    print(i)
                            else:
                                print("Not a closed account")
                        elif opt==2:
                            tmp=0
                            db.close()
                            print("ADMIN LOGGED OUT")
                        else:
                            print("enter correct option")
                else:
                    print("invalid password")
            else:
                print("invalid id and password")
        def quit(self):
            print(":: YOU ARE LOGGED OUT NOW ::")
            sys.exit()
            