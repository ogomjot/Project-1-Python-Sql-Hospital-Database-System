import pymysql
conn=pymysql.connect(host='localhost',user='root',password='ayan@123')
cur=conn.cursor()
def create():
    try:
        cur.execute('create database hospital')
    except:
        print('Database is Already Present')
        cur.execute('Use hospital')
    try:
        cur.execute('''create Table HOSPITAL(patient_id int primary key
, patient_name varchar(40) not null , age int not null
, contact_number bigint not null , diagnosis varchar(50) not null, doctor_treating varchar(50) not null , department varchar(50) not null
, date_of_admission date not null , date_of_discharging date not null , fees float(10,2) not null
, payment_status varchar(20) not null )''')
    except:
        print('Table already exists.')
def add():
    pID=int(input('Enter Patient Id: '))
    Pname=input('Enter Patient Name: ')
    age=int(input('Enter Age of the Patient: '))
    C_no=int(input('Enter Patient Contact Number: '))
    D=input('Enter Patient Diagnosis: ')
    D_Name=input('Enter Patient Doctor Name: ')
    dept=input('Enter Patient Doctor Dept: ')
    Add_Date=input('Enter Patient Date of admission: ')
    End_Date=input('Enter Patient Date of Discharging: ')
    Fees=float(input('Enter Patient Fees: '))
    P_Status=input('Enter Payment status of Patient: ')
    sql='''insert into hospital values({},"{}",{},{},"{}","{}","{}","{}","{}",{},"{}")'''.format(pID,Pname,age,C_no,D,D_Name,dept,Add_Date,End_Date,Fees,P_Status)
    cur.execute(sql)
    conn.commit()
def view():
    cur.execute('select * from HOSPITAL')
    r=cur.fetchall()
    c=cur.rowcount
    print('Total No. of records are ',c)
    for i in r:
        print(i)
def search():
    pID=int(input('Enter Patient Id you want to search for: '))
    cur.execute('Select * from HOSPITAL where patient_id={}'.format(pID,))
    r=cur.fetchone()
    if r==None:
        print('Patient ID not found')
    else:
        print('Patient with Patient ID ',pID,'has the following info:')
        print('Patient name is',r[1])
        print('Patient age is',r[2])
        print('Patient Contact No. is',r[3])
        print('Patient Diagnosis is',r[4])
        print("Patient's Doctor's name is",r[5])
        print("Patient's Doctor's department is",r[6])
        print("Patient's Date of Admission is",r[7])
        print("Patient's Date of Discharging is",r[8])
        print("Patient's Fees is",r[9])
        print("Patient's Payment Status is",r[10])
def update():
    c='y'
    while c=='y':   
        choice=int(input('''what do you want to update : 1.Name
2.Age
3.Contact_No
4.Diagnosis
5.Name_of_Doctor
6.Department_of_Doctor
7.Admission_Date
8.Discharging_Date
9.Fees
10.Payment_Status :'''))
        if choice==1:
            pID=int(input("Patient ID :"))
            sql="select * from HOSPITAL where patient_id={}".format(pID,)
            cur.execute(sql)
            r=cur.fetchone()
            if r==None:
                print('Patient is not Present')
            else:
                Pname=input('Enter Patient Name you want to change: ')
                sql='Update HOSPITAL set patient_name="{}" where patient_id={}'.format(Pname,pID)
                cur.execute(sql)
                conn.commit()
        elif choice==2:
            pID=int(input("Patient ID :"))
            sql="select * from HOSPITAL where patient_id={}".format(pID,)
            cur.execute(sql)
            r=cur.fetchone()
            if r==None:
                print('Patient is not Present')
            else:
                age=input('Enter Patient age you want to change: ')
                sql='Update HOSPITAL set age={} where patient_id={}'.format(age,pID)
                cur.execute(sql)
                conn.commit()
        elif choice==3:
            pID=int(input("Patient ID :"))
            sql="select * from HOSPITAL where patient_id={}".format(pID,)
            cur.execute(sql)
            r=cur.fetchone()
            if r==None:
                print('Patient is not Present')
            else:
                C_no=input('Enter Patient contact you want to change: ')
                sql='Update HOSPITAL set contact_number="{}" where patient_id={}'.format(C_no,pID)
                cur.execute(sql)
        
                conn.commit()
        elif choice==4:
            pID=int(input("Patient ID :"))
            sql="select * from HOSPITAL where patient_id={}".format(pID,)
            cur.execute(sql)
            r=cur.fetchone()
            if r==None:
                print('Patient is not Present')
            else:
                D=input('Enter Patient Diagnosis you want to change: ')
                sql='Update HOSPITAL set diagnosis="{}" where patient_id={}'.format(D,pID)
                cur.execute(sql)
                conn.commit()
        elif choice==5:
            pID=int(input("Patient ID :"))
            sql="select * from HOSPITAL where patient_id={}".format(pID,)
            cur.execute(sql)
            r=cur.fetchone()
            if r==None:
                print('Patient is not Present')
            else:
                D_name=input('Enter Doctor Name you want to change: ')
                sql='Update HOSPITAL set docteor_treating="{}" where patient_id={}'.format(D_name,pID)
                cur.execute(sql)
                conn.commit()
        elif choice==6:
            pID=int(input("Patient ID :"))
            sql="select * from HOSPITAL where patient_id={}".format(pID,)
            cur.execute(sql)
            r=cur.fetchone()
            if r==None:
                print('Patient is not Present')
            else:
                dept=input('Enter Department of Doctor you want to change: ')
                sql='Update HOSPITAL set department="{}" where patient_id={}'.format(dept,pID)
                cur.execute(sql)
        elif choice==7:
            pID=int(input("Patient ID :"))
            sql="select * from HOSPITAL where patient_id={}".format(pID,)
            cur.execute(sql)
            r=cur.fetchone()
            if r==None:
                print('Patient is not Present')
            else:
                Add_Date=input('Enter Admission Date you want to change: ')
                sql='Update HOSPITAL set date_of_admission="{}" where patient_id={}'.format(Add_Date,pID)
                cur.execute(sql)
                conn.commit()
        elif choice==8:
            pID=int(input("Patient ID :"))
            sql="select * from HOSPITAL where patient_id={}".format(pID,)
            cur.execute(sql)
            r=cur.fetchone()
            if r==None:
                print('Patient is not Present')
            else:
                End_Date=input('Enter Discharged Date you want to change: ')
                sql='Update HOSPITAL set date_of_discharging="{}" where patient_id={}'.format(End_Date,pID)
                cur.execute(sql)
                conn.commit()
        elif choice==9:
            pID=int(input("Patient ID :"))
            sql="select * from HOSPITAL where patient_id={}".format(pID,)
            cur.execute(sql)
            r=cur.fetchone()
            if r==None:
                print('Patient is not Present')
            else:
                Fees=input('Enter Fees you want to change: ')
                sql='Update HOSPITAL set fees={} where patient_id={}'.format(Fees,pID)
                cur.execute(sql)
                conn.commit()
        elif choice==10:
            pID=int(input("Patient ID :"))
            sql="select * from HOSPITAL where patient_id={}".format(pID,)
            cur.execute(sql)
            r=cur.fetchone()
            if r==None:
                print('Patient is not Present')
            else:
                P_Status=input('Enter Payment status you want to change: ')
                sql='Update HOSPITAL set payment_status="{}" where patient_id={}'.format(Pname,pID)
                cur.execute(sql)
                conn.commit()
                conn.commit()
        else:
            print('Invalid choice')
            break
        c=input('do you want to enter more (y/n) :')
def menu():
        b='y'
        while b=='y':
            a=int(input('''what do you want to do :
1.create
2.add
3.view
4.search
5.update
6.Exit'''))
            if a==1:
                create()
            elif a==2:
                add()
            elif a==3:
                view()
            elif a==4:
                search()
            elif a==5:
                update()      
            else:
                print('THANK YOU FOR VISITING')
                break
            
            b=input('Do you want to continue(y/n): ')
menu()
conn.close()
