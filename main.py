import mysql.connector as mysql1
import functions as f
import Security as s
if(s.authenticate()):
    if(f.is_db_connected):
        print("Welcome to Library Database Management System")
        print("-"*46)
        while True:
            print("Press corresponding digit to perform operations: ")
            print("1. IssueBooks")
            print("2. Return Books")
            print("3. Show User Details")
            print("4. Show Books Details")
            print("5. New Registration")
            print("6. Check Books Issued")
            print("7. Search Books")
            print("8. Edit Userdata")
            print("9. Check Fine")
            print("10. Check limit")
            print("11. Update Fine")
            print("12. Change Admin Password")
            print("13. Exit")
            
            x=int(input("Enter your choice: "))


            if x==1:
                f.issuebooks()
            
            elif x==2:
                f.returnbook()
            
            elif x==3:
                f.userdetails()
            
            elif x==4:
                f.booksdetails()
            
            elif x==5: 
                while True:
                    print(f'{'-'*7}New Registration{'-'*7}')
                    print("1. Add User")
                    print("2. Add Book")
                    i=int(input("Enter corresponding number"))
                    if i==1:
                        f.adduser()
                    elif i==2:
                        f.addbooks()
            
            elif x==6:
                f.booksissued()
            
            elif x==7:
                f.searchbooksby()
            
            elif x==8:
                while True:
                    print(f'{'-'*7}Edit User Data{'-'*7}')
                    print("1. Edit Username")
                    print("2. Edit User Phone Number")
                    i=int(input("Enter corresponding number"))
                    if i==1:
                        f.editusername()
                    elif i==2:
                        f.edituserPNo()
            
            elif x==9:
                f.checkfine()
            
            elif x==10:
                f.checklimit()
            
            elif x==11:
                f.updatefine()
            
            elif x==12:
                s.change_password()
            
            elif x==13:
                print("Thank Youuuu")
                break
            elif x==14:
                f.isreturnable(3,1)
            
            i=input("Do you want to continue?(Yes/No) : ")
            if i.lower()!="yes":
                print("Thank Youuuuu")
                break
    else:
        print("Database can't be collected")
    # Print Slip for Issuing Books with book details, customer details, issuedate, returndate 
else:
    print("Password Doesn't Match")
    