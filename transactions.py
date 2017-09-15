import pymysql

class transactions:
    def address_update(self,id):
        db = pymysql.connect("localhost","root","","banking_system" )
        cursor = db.cursor()
        self.id =id
        add= input("enter address")
        sql="UPDATE cust_info SET ADDRESS=%s WHERE cust_id=%s"
        data=(add,id)
        x=cursor.execute(sql,data)
        if(x>=1):
            print(":: UPDATED SUCCESSFULLY ::")
        else:
            print(":: UPDATION FAILED ::")
        db.commit()
        db.close()
    def deposit(self,id):
        db = pymysql.connect("localhost","root","","banking_system" )
        cursor = db.cursor()
        self.id =id
        amt= int(input("Enter amount to be deposited"))
        sql="SELECT ACCOUNTTYPE FROM cust_info WHERE cust_id=%s"""
        data=(id)
        cursor.execute(sql,data)
        t=cursor.fetchone()
        a=str(t[0])
        z=1
        while z==1:
            if a=='savings':
                if amt>5000:
                    sql="SELECT balance FROM CUST_INFO WHERE CUST_ID=%s"
                    data=(id)
                    cursor.execute(sql,data)
                    t=cursor.fetchone()
                    a=str(t[0])
                    v=int(a)
                    v=v+amt
                    sql="UPDATE cust_info,transaction SET cust_info.balance=%s,transaction.deposit=%s WHERE cust_info.cust_id=%s and cust_info.cust_id=transaction.cust_id"
                    data=(v,amt,id)
                    x=cursor.execute(sql,data)
                    if x>=1:
                        print(":: DEPOSITED ::")
                        z=0
                    else:
                        print(":: DEPOSITION FAILED ::")
                else:
                    print("Enter correct amount ::")
                    amt= int(input("Enter amount to be deposited"))
            else:
                if amt>0:
                    sql="SELECT balance FROM CUST_INFO WHERE CUST_ID=%s"
                    data=(id)
                    cursor.execute(sql,data)
                    t=cursor.fetchone()
                    a=str(t[0])
                    v=int(a)
                    v=v+amt
                    sql="UPDATE cust_info,transaction SET cust_info.balance=%s,transaction.deposit=%s WHERE cust_info.cust_id=%s and cust_info.cust_id=transaction.cust_id"
                    data=(v,amt,id)
                    x=cursor.execute(sql,data)
                    if x>=1:
                        print(":: DEPOSITED ::")
                        z=0
                    else:
                        print(":: DEPOSITION FAILED ::")
                else:
                    print("Enter correct amount ::")
                    amt= int(input("Enter amount to be deposited"))
        db.commit()
        db.close()
    def withdraw(self,id):
        db = pymysql.connect("localhost","root","","banking_system" )
        cursor = db.cursor()
        self.id=id
        amt =int(input("Enter withdraw money ::"))
        sql="SELECT balance FROM CUST_INFO WHERE CUST_ID=%s"
        data=(id)
        cursor.execute(sql,data)
        t=cursor.fetchone()
        a=str(t[0])
        v=int(a)
        v=v-amt
        if(v>0):
            sql="SELECT ACCOUNTTYPE FROM cust_info WHERE cust_id=%s"""
            data=(id)
            cursor.execute(sql,data)
            t=cursor.fetchone()
            a=str(t[0])
            if(a=='current'):
                sql="UPDATE cust_info,transaction SET cust_info.BALANCE=%s,transaction.withdrawl=%s WHERE cust_info.cust_id=%s and cust_info.cust_id=transaction.cust_id"
                data=(v,amt,id)
                x=cursor.execute(sql,data) 
                if x>=1:
                     print(":: WITHDRAWN ::")
                else:
                     print(":: ERROR IN WITHDRAWING MONEY ::")
            else:
                if(v>5000):
                    sql="UPDATE cust_info,transaction SET cust_info.BALANCE=%s,transaction.withdrawl=%s WHERE cust_info.cust_id=%s and cust_info.cust_id=transaction.cust_id"
                    data=(v,amt,id)
                    x=cursor.execute(sql,data) 
                    if(x>=1):
                        print(":: WITHDRAWN ::")
                    else:
                        print(":: ERROR IN WITHDRAWING MONEY ::")
                else:
                    print("NOT SUFFICIENT AMOUNT")
            db.commit()
            db.close() 
        else:
            print(":: INSUFFICIENT BALANCE ::")     
    def print_statement(self,id):
        db = pymysql.connect("localhost","root","","banking_system" )
        cursor = db.cursor()
        self.id =id
        sql="""SELECT CUST_ID FROM cust_info WHERE cust_id=%s"""
        data=(id)
        x=cursor.execute(sql,data)
        if x>=1:
            sql="SELECT cust_info.balance,transaction.date FROM cust_info,transaction WHERE cust_info.cust_id=%s AND cust_info.cust_id=transaction.cust_id"
            data=(id)
            cursor.execute(sql,data)
            t=cursor.fetchall()
            print(t)
    def transfer_money(self,id):
        db = pymysql.connect("localhost","root","","banking_system" )
        cursor = db.cursor()
        self.id=id
        amt =int(input("Enter amount to be transferred ::"))
        id1=input("Enter id of account in which you want to transfer ::")
        sql="""SELECT CUST_ID FROM cust_info WHERE CUST_ID=%s"""
        data=(id1)
        x=cursor.execute(sql,data)
        if x>=1:
            sql="SELECT balance FROM CUST_INFO WHERE CUST_ID=%s"
            data=(id)
            cursor.execute(sql,data)
            t=cursor.fetchone()
            a=str(t[0])
            v=int(a)
            sub=v-amt
            sql="SELECT balance FROM CUST_INFO WHERE CUST_ID=%s"
            data=(id1)
            cursor.execute(sql,data)
            t=cursor.fetchone()
            a=str(t[0])
            y=int(a)
            add=y+amt
            if(v>0):
                sql="SELECT ACCOUNTTYPE FROM cust_info WHERE cust_id=%s"""
                data=(id)
                cursor.execute(sql,data)
                t=cursor.fetchone()
                a=str(t[0])
                if(a=='savings'):
                    sql="""UPDATE cust_info,transaction SET cust_info.BALANCE=%s,transaction.withdrawl=%s 
                        WHERE cust_info.cust_id=%s and cust_info.cust_id=transaction.cust_id"""
                    data=(sub,amt,id)
                    x=cursor.execute(sql,data) 
                    sql="""UPDATE cust_info,transaction SET cust_info.BALANCE=%s,transaction.deposit=%s 
                        WHERE cust_info.cust_id=%s and cust_info.cust_id=transaction.cust_id"""
                    data=(add,amt,id1)
                    x=cursor.execute(sql,data) 
                    if x>=1:
                        print(":: TRANSFERRED SUCCESSFULLY ::")
                else:
                    if(v>5000):
                        sql="""UPDATE cust_info,transaction SET cust_info.BALANCE=%s,transaction.withdrawl=%s 
                            WHERE cust_info.cust_id=%s and cust_info.cust_id=transaction.cust_id"""
                        data=(sub,amt,id)
                        x=cursor.execute(sql,data)
                        sql="""UPDATE cust_info,transaction SET cust_info.BALANCE=%s,transaction.deposit=%s WHERE 
                            cust_info.cust_id=%s and cust_info.cust_id=transaction.cust_id"""
                        data=(add,amt,id1)
                        x=cursor.execute(sql,data)  
                        if(x>=1):
                            print(":: TRANSFERRED SUCCESSFULLY ::")  
                    else:
                        print(":: INSUFFICIENT BALANCE ::")    
            else:
                print(":: INSUFFICIENT BALANCE ::") 
            db.commit()
            db.close()
        else:
            print("Invalid id")
    def acc_close(self,id):
        db = pymysql.connect("localhost","root","","banking_system" )
        cursor = db.cursor()
        self.id =id
        sql="""UPDATE transaction,cust_info SET acc_close='YES' WHERE 
            transaction.cust_id=cust_info.cust_id AND cust_info.cust_id=%s"""
        data=(id)
        x=cursor.execute(sql,data)
        if x>=1:
            print(":: ACCOUNT CLOSED ::")
        else:
            print(":: Error in closing. Re-check details ::")
        db.commit()
        db.close()