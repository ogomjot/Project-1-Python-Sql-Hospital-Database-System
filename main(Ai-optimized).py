import pymysql

# Password is asked at runtime so it never gets uploaded to GitHub
password = input('Enter MySQL password: ')
conn = pymysql.connect(host='localhost', user='root', password=password)
cur = conn.cursor()


def create():
    cur.execute('create database if not exists hospital')
    cur.execute('use hospital')
    cur.execute('''create table if not exists HOSPITAL(
        patient_id int primary key,
        patient_name varchar(40) not null,
        age int not null,
        contact_number bigint not null,
        diagnosis varchar(50) not null,
        doctor_treating varchar(50) not null,
        department varchar(50) not null,
        date_of_admission date not null,
        date_of_discharging date not null,
        fees decimal(10,2) not null,
        payment_status varchar(20) not null)''')
    print('Database and table are ready.')


def add():
    pID = int(input('Enter Patient Id: '))
    cur.execute('select * from HOSPITAL where patient_id=%s', (pID,))
    if cur.fetchone() is not None:
        print('Patient ID already exists')
        return
    Pname = input('Enter Patient Name: ')
    age = int(input('Enter Age of the Patient: '))
    C_no = int(input('Enter Patient Contact Number: '))
    D = input('Enter Patient Diagnosis: ')
    D_Name = input('Enter Patient Doctor Name: ')
    dept = input('Enter Patient Doctor Dept: ')
    Add_Date = input('Enter Patient Date of admission (YYYY-MM-DD): ')
    End_Date = input('Enter Patient Date of Discharging (YYYY-MM-DD): ')
    Fees = float(input('Enter Patient Fees: '))
    P_Status = input('Enter Payment status of Patient: ')
    sql = '''insert into HOSPITAL
        (patient_id, patient_name, age, contact_number, diagnosis,
         doctor_treating, department, date_of_admission,
         date_of_discharging, fees, payment_status)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    cur.execute(sql, (pID, Pname, age, C_no, D, D_Name, dept,
                      Add_Date, End_Date, Fees, P_Status))
    conn.commit()
    print('Patient added.')


def view():
    cur.execute('select * from HOSPITAL')
    r = cur.fetchall()
    print('Total No. of records are', len(r))
    for i in r:
        print(i)


def search():
    pID = int(input('Enter Patient Id you want to search for: '))
    cur.execute('select * from HOSPITAL where patient_id=%s', (pID,))
    r = cur.fetchone()
    if r is None:
        print('Patient ID not found')
    else:
        labels = ['Patient ID', 'Name', 'Age', 'Contact No.', 'Diagnosis',
                  "Doctor's name", "Doctor's department", 'Date of Admission',
                  'Date of Discharging', 'Fees', 'Payment Status']
        print('Patient with Patient ID', pID, 'has the following info:')
        for label, value in zip(labels, r):
            print(label, 'is', value)


def update():
    fields = {
        1: ('patient_name', 'Enter Patient Name you want to change: ', str),
        2: ('age', 'Enter Patient age you want to change: ', int),
        3: ('contact_number', 'Enter Patient contact you want to change: ', int),
        4: ('diagnosis', 'Enter Patient Diagnosis you want to change: ', str),
        5: ('doctor_treating', 'Enter Doctor Name you want to change: ', str),
        6: ('department', 'Enter Department of Doctor you want to change: ', str),
        7: ('date_of_admission', 'Enter Admission Date you want to change: ', str),
        8: ('date_of_discharging', 'Enter Discharged Date you want to change: ', str),
        9: ('fees', 'Enter Fees you want to change: ', float),
        10: ('payment_status', 'Enter Payment status you want to change: ', str),
    }
    while True:
        choice = int(input('''what do you want to update :
1.Name
2.Age
3.Contact_No
4.Diagnosis
5.Name_of_Doctor
6.Department_of_Doctor
7.Admission_Date
8.Discharging_Date
9.Fees
10.Payment_Status : '''))
        if choice not in fields:
            print('Invalid choice')
            break
        pID = int(input('Patient ID : '))
        cur.execute('select * from HOSPITAL where patient_id=%s', (pID,))
        if cur.fetchone() is None:
            print('Patient is not Present')
        else:
            column, prompt, converter = fields[choice]
            value = converter(input(prompt))
            cur.execute('update HOSPITAL set {}=%s where patient_id=%s'.format(column),
                        (value, pID))
            conn.commit()
            print('Record updated.')
        if input('do you want to update more (y/n) : ').lower() != 'y':
            break


def menu():
    b = 'y'
    while b == 'y':
        try:
            a = int(input('''
what do you want to do :
1.create
2.add
3.view
4.search
5.update
6.Exit
Enter choice: '''))
            if a == 1:
                create()
            elif a == 2:
                add()
            elif a == 3:
                view()
            elif a == 4:
                search()
            elif a == 5:
                update()
            elif a == 6:
                break
            else:
                print('Invalid choice, enter a number from 1 to 6')
        except ValueError:
            print('Please enter numbers only where a number is asked')
        except pymysql.MySQLError as e:
            print('Database error:', e)
        b = input('Do you want to continue(y/n): ').lower()
    print('THANK YOU FOR VISITING')


# 'use hospital' is needed before add/view/etc, so create() runs once at start
create()
menu()
conn.close()
