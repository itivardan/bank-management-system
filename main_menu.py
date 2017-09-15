from customer import cust_login

ob=cust_login()
c=1
while c==1:
    print("-----------------------------------------------")
    print("1.SIGN UP\n2.SIGN IN\n3.ADMIN SIGN IN\n4.QUIT")
    opt=int(input(":: ENTER YOUR CHOICE ::\n"))
    if opt==1:
        ob.signup()
    elif opt==2:
        ob.signin()
    elif opt==3:
        ob.admin_login()
    elif opt==4:
        ob.quit()
    else:
        print(":: ENTER VALID OPTION ::\n")
    print("------------------------------------------------")