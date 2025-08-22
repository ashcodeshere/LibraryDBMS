import mysql.connector as mysql1
from datetime import date,datetime,timedelta
import getpass as g
import hashlib
from dotenv import load_dotenv
import os
load_dotenv()
con=mysql1.connect(host='localhost',user=os.getenv("DB_USER"),password=os.getenv("DB_PASSWORD"),database='libraryDBMS',auth_plugin='mysql_native_password')

# -------------------------------------------------------------------------------------------------------------------------

def addbooks():
    cursor=con.cursor()
    bookname=input("Enter book name : ")
    authorname=input("Enter author name : ")
    publishername=input("Enter publisher name : ")
    category=input("Enter category : ")
    status=input("Enter status : (Issuable or not)")
    s1="insert into booksdetails (name,author,publisher,category,status) values(%s, %s, %s, %s, %s)"
    values=(bookname,authorname,publishername,category,status)
    try:
        cursor.execute(s1,values)
        con.commit()
        print("Record Inserted")
    except mysql1.Error as err:
        print("Error Occured while insertion",err)
        con.close()
    finally:
        cursor.close()


def adduser():
    cursor=con.cursor()
    username=input("Enter Your Name : ")
    phoneno=input("Enter Phone Number : ") 
    s2="insert into userdetails (name,PhoneNo) values (%s,%s)"
    values=(username,phoneno)
    try:
        cursor.execute(s2,values)
        con.commit()
        print("User Details Inserted")
    except mysql1.Error as err:
        print("Error occured while insertion",err)
        con.close()
    finally:
        cursor.close()


def editusername():
    cursor=con.cursor()
    uid=input("Enter uid : ")
    username=input("Enter Username : ")
    s3="UPDATE userdetails set name=%s where id=%s"
    values=(username,uid)
    try:
        cursor.execute(s3,values)
        con.commit()
        print("User Details Updated")
    except mysql1.Error as err:
        print("Error occured while insertion",err)
        con.close()
    finally:
        cursor.close()
        
        
def edituserPNo():
    cursor=con.cursor()
    uid=input("Enter Uid : ")
    PhoneNo=input("Enter Phone Number : ")
    s3="UPDATE userdetails set PhoneNo=%s where id=%s"
    values=(PhoneNo,uid)
    try:
        cursor.execute(s3,values)
        con.commit()
        print("User Details Updated")
    except mysql1.Error as err:
        print("Error occured while insertion",err)
        con.close()
    finally:
        cursor.close()    
   
        
def issuebooks():
    cursor=con.cursor()
    uid=int(input("Enter User ID : "))
    if checkuser(uid)==False:
        print("No User for this ID")
    else:
        if checkfinebyuid(uid)==0:
            bid=int(input("Enter Book ID : "))
            if checkbook(bid)==False:
                print("No Book for this ID")
            else:
                if isissuable(bid)==True:
                    s4="insert into booksissued (id,bid) values(%s, %s)"
                    s5="UPDATE userdetails set booksissued=booksissued+1 where id=%s"
                    s6="Update booksdetails set status='NonIssuable' where bid=%s"
                    values1=(uid,bid)
                    values2=(uid,)
                    values3=(bid,)
                    try:
                        cursor.execute(s4,values1)
                        cursor.execute(s5,values2)
                        cursor.execute(s6,values3)
                        con.commit()
                        print("Book Issued")
                    except mysql1.Error as err:
                        print("Error occured while insertion",err)
                        con.rollback()
                    finally:
                        cursor.close()
                else:
                    print("Book can't be issued")
        else :
            print(f"Fine Pending : {checkfinebyuid(uid)}")
            print("Book can't be issued until fine is Paid")


def isissuable(bid):
    cursor=con.cursor()
    s7="SELECT status FROM booksdetails where bid=%s;"
    values=(bid,)
    try:
        cursor.execute(s7,values)
        y=cursor.fetchone()
        if y[0].lower()!="issuable":
            return False
        else:
            return True
        con.commit()
    except mysql1.Error as err:
        con.close()
    finally:
        cursor.close()
        

def userdetails():
    cursor=con.cursor()
    uid=int(input("Enter UserId: "))
    s="SELECT * FROM userdetails where id=%s;"
    values=(uid,)
    try:
        cursor.execute(s,values)
        y=cursor.fetchall()
        if y:
            print(f"{'User_Id':<10}{'User_Name':<30}{'PhoneNumber':<20}{'BooksIssued':<20}{'Fines':<30}")
            print("-"*110)
            for row in y:
                User_Id,User_Name,PhoneNumber,BooksIssued,Fines=row
                print(f"{User_Id:<10}{User_Name:<30}{PhoneNumber:<20}{BooksIssued:<20}{Fines:<30}")
    except mysql1.Error as err:
        print("Error occured while fetching")
        con.close()
    finally:
        cursor.close()
 

def booksissued():
    cursor=con.cursor()
    s7="SELECT * FROM booksissued;"
    try:
        cursor.execute(s7)
        y=cursor.fetchall()
        print("Books Issued")        
        if y:
            print(f"{'User_Id':<10}{'Book_Id':<10}{'Date&TimeIssued':<20}")
            print("-"*40)
            for row in y:
                user_id=row[0]
                book_id=row[1]
                dt=row[2]
                print(f"{user_id:<10}{book_id:<10}{dt.strftime('%Y-%m-%d %H-%M-%S'):<20}")
        else:
            print("No Books were issued!!")        
        con.commit()
    except mysql1.Error as err:
        print("Error occured while Fetching Data")
        con.close()
    finally:
        cursor.close()


def booksToBeOrdered():
    cursor=con.cursor()
    s8="select name,author,publisher,category from booksdetails where status=%s"
    values=("ToBeOrdered",)
    try:
        cursor.execute(s8,values)
        y=cursor.fetchall()
        print("Books to Be Ordered :\n")
        
        if y:
            print(f"{'Book_Name':<40}{'Author_Name':<40}{'PublisherName':<40}{'Category':<10}")
            print("-"*130)
            for row in y:
                bookname,authorname,publishername,category=row
                print(f"{bookname:<40}{authorname:<40}{publishername:<40}{category:<10}")        
        else:
            print("No Books to be ordered")
        con.commit()
    except mysql1.Error as err:
        print("Error occured while fetching data ",err)
        con.close()
    finally:
        cursor.close()
        
        
def booksdetails():
    cursor=con.cursor()
    bid=int(input("Enter Book ID : "))
    s8="select name,author,publisher,category,status from booksdetails where bid=%s"
    values=(bid,)
    try:
        cursor.execute(s8,values)
        y=cursor.fetchall()
        
        if y:
            print(f"{'Book_Name':<35}{'Author_Name':<30}{'PublisherName':<30}{'Category':<20}{'Status':<15}")
            print("-"*130)
            for row in y:
                bookname,authorname,publishername,category,status=row
                print(f"{bookname:<35}{authorname:<30}{publishername:<30}{category:<20}{status:<15}")        
        else:
            print("No Books with this id")
        con.commit()
    except mysql1.Error as err:
        print("Error occured while fetching data ",err)
        con.close()
    finally:
        cursor.close()
        

def searchbooksby():
    print("Search By: \n")
    print("1. Name\n")
    print("2. AuthorName\n")
    print("3. BookID\n")
    print("4. Category\n")
    print("5. PublisherName\n")
    print("6. Status\n")
    a=int(input("Enter your choice : "))
    cursor=con.cursor()
    if a==1:
        name=input("Enter Book name : ")
        s8="select bid,name,author,publisher,category,status from booksdetails where name=%s"
        values=(name,)
    elif a==2:
        author=input("Enter Author name : ")
        s8="select bid,name,author,publisher,category,status from booksdetails where author=%s"
        values=(author,)
    elif a==3:
        bookid=int(input("Enter Book ID : "))
        s8="select bid,name,author,publisher,category,status from booksdetails where bid=%s"
        values=(bookid,)
    elif a==4:
        category=input("Enter Category : ")
        s8="select bid,name,author,publisher,category,status from booksdetails where category=%s"
        values=(category,)   
    elif a==5:
        publisher=input("Enter Publisher name : ")
        s8="select bid,name,author,publisher,category,status from booksdetails where publisher=%s"
        values=(publisher,)    
    elif a==6:
        status=input("Enter status : ")
        s8="select bid,name,author,publisher,category,status from booksdetails where status=%s"
        values=(status,)    
    
    try:
        cursor.execute(s8,values)
        y=cursor.fetchall()
        
        if y:
            print(f"{'Book_Id':<10}{'Book_Name':<35}{'Author_Name':<30}{'PublisherName':<30}{'Category':<20}{'Status':<15}")
            print("-"*130)
            for row in y:
                bookid,bookname,authorname,publishername,category,status=row
                print(f"{bookid:<10}{bookname:<35}{authorname:<30}{publishername:<30}{category:<20}{status:<15}")        
        else:
            print("Not Available")
        con.commit()
    except mysql1.Error as err:
        print("Error occured while fetching data ",err)
        con.close()
    finally:
        cursor.close()
    
         
def isreturnable(uid,bid):
    cursor=con.cursor()
    s="SELECT * from BooksIssued where id=%s and bid=%s;"
    values2=(uid,bid)
    try:
        cursor.execute(s,values2)
        res=cursor.fetchone()
        if res==None:
            return False
        else:
            return True
    except mysql1.Error as err:
        print("Error occured while fetching data ",err)
        con.rollback()
        con.close()
    finally:
        cursor.close()
    
        
def returnbook():
    uid=int(input("Enter Uid : "))
    bid=int(input("Enter Bid : "))
    cursor=con.cursor()
    if isreturnable(uid,bid)==True:
        s9="UPDATE booksdetails set status=%s where bid=%s"
        values1=("Issuable",bid)
        s10="UPDATE userdetails set Booksissued=booksissued-1 where id=%s and Booksissued>0;"
        values2=(uid,)
        s11="DELETE FROM booksissued where Bid=%s"
        values3=(bid,)
        try:
            cursor.execute(s9,values1)
            cursor.execute(s10,values2)
            cursor.execute(s11,values3)
            print("Record Updated\n")
            print(f'Fine Pending : {checkfinebyuid(uid)}')
            con.commit()
        except mysql1.Error as err:
            print("Error occured while fetching data ",err)
            con.rollback()
            con.close()
        finally:
            cursor.close()
    else:
        print("No data")


def updatefinebyuid(uid,bid):
    cursor=con.cursor()
    s12="Select dateissued from booksissued where id=%s and bid=%s"
    s13="update userdetails set fines=%s where id=%s"
    s14="update booksissued set fines=%s where id =%s"
    values1=(uid,bid)
    try:
        cursor.execute(s12,values1)
        y=cursor.fetchone()
        if y:
            date_issued=y[0]
            curr_datetime=datetime.now()
            diff=(curr_datetime-date_issued).days
            alloweddays=14
            if diff>alloweddays:
                fine=(diff-alloweddays)*5
            else:
                fine=0
            if fine>0:
                values2=(fine,uid)
                cursor.execute(s13,values2)
                cursor.execute(s14,values2)
            
        else:
            print("No Record")
        con.commit()
    except mysql1.Error as err:
        print("Error occured ",err)
        con.close()
    finally:
        cursor.close()

        
def updatefine():
    cursor=con.cursor()
    uid=int(input("Enter Uid : "))
    bid=int(input("Enter Bid : "))
    s12="Select dateissued from booksissued where id=%s and bid=%s"
    s13="update userdetails set fines=%s where id=%s"
    s14="update booksissued set fines=%s where id =%s"
    values1=(uid,bid)
    try:
        cursor.execute(s12,values1)
        y=cursor.fetchone()
        if y:
            date_issued=y[0]
            curr_datetime=datetime.now()
            diff=(curr_datetime-date_issued).days
            alloweddays=14
            if diff>alloweddays:
                fine=(diff-alloweddays)*5
            else:
                fine=0
            if fine>0:
                values2=(fine,uid)
                cursor.execute(s13,values2)
                cursor.execute(s14,values2)
            
        else:
            print("No Record")
        con.commit()
    except mysql1.Error as err:
        print("Error occured ",err)
        con.close()
    finally:
        cursor.close()


def checkfine():
    cursor=con.cursor()
    uid=int(input("Enter Uid : "))
    s15="select fines from userdetails where id=%s"
    values=(uid,)
    try:
        cursor.execute(s15,values)
        y=cursor.fetchone()
        if y:
            con.commit()
            print(f'Your fine: {y[0]}')
        else:
            con.commit()
            return 0
    except mysql1.Error as err:
        print("Error Occured ",err)
        con.close()
    finally:
        cursor.close()


def checkfinebyuid(uid):
    cursor=con.cursor()
    # updatefine()
    s15="select fines from userdetails where id=%s"
    values=(uid,)
    try:
        cursor.execute(s15,values)
        y=cursor.fetchone()
        if y:
            con.commit()
            return y[0]
        else:
            con.commit()
            return 0
    except mysql1.Error as err:
        print("Error Occured ",err)
        con.close()
    finally:
        cursor.close()
        

def checklimit():
    cursor=con.cursor()
    uid=int(input("Enter Uid : "))
    bid=int(input("Enter Bid : "))
    s16="Select dateissued from booksissued where id=%s and bid=%s"
    values=(uid,bid)
    try:
        cursor.execute(s16,values)
        y=cursor.fetchone()
        if y:
            date_issued=y[0]
            curr_datetime=datetime.now()
            diff=(curr_datetime-date_issued).days
            alloweddays=14
            if diff>alloweddays:
                print("You have to return the book with fine as soon as possible!!!!!")
            else:
                print(f"{alloweddays-diff} Days Left !!")
                today=date.today()
                returnday=today+timedelta(alloweddays-diff)
                print(f"You should submit it on or before {returnday}")
        else:
            print("No Record")
            con.commit()
    except mysql1.Error as err:
        print("Error occured ",err)
        con.close()
    finally:
        cursor.close()
    

def checkbooksissued():
    cursor=con.cursor()
    uid=int(input("Enter Uid : "))
    s17="Select booksissued from userdetails where id=%s"
    values=(uid,)
    try:
        cursor.execute(s17,values)
        y=cursor.fetchone()
        if y is not None and y[0]>0:
            return y[0]
        else:
            return 0
    except mysql1.Error as err:
        print("Error occured ",err)
        con.close()
    finally:
        cursor.close()
    
    
def checkuser(uid):
    cursor=con.cursor()
    s18="Select id from userdetails "
    try:
        cursor.execute(s18)
        y=cursor.fetchall()
        for i in y:
            if uid==i[0]:
                return True
        return False
                
    except mysql1.Error as err:
        print("Error Occured ", err)
        con.close()
    finally:
        cursor.close()
        

def checkbook(bid):
    cursor=con.cursor()
    s19="Select bid from booksdetails "
    try:
        cursor.execute(s19)
        y=cursor.fetchall()
        for i in y:
            if bid==i[0]:
                return True
        return False
                
    except mysql1.Error as err:
        print("Error Occured ", err)
        con.close()
    finally:
        cursor.close()
        
        
def is_db_connected():
    try:
        con=mysql1.connect(host="localhost",user=os.getenv("DB_USER"),password=os.getenv("DB_PASSWORD"),database='libraryDBMS',auth_plugin='mysql_native_password')
        con.close()
        return True
    except Exception as e:
        return False

