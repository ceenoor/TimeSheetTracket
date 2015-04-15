import psycopg2
import psycopg2.extras
import urllib
import csv
import os
from flask import Flask, session, redirect, url_for, escape, render_template, request


app = Flask(__name__)
app.secret_key=os.urandom(24).encode('hex')
currentUser = ''

@app.route('/', methods = ['GET', 'POST'])
def mainIndex():
    if request.method == 'GET':
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if request.args.get('name') == None:
            return redirect(url_for('login'))
        else:
         name = request.args.get('name')
        print name
        if name in session['username']:
            print "welcome"
            query = ("select * from employees;")
            queryTwo = ("select * from job_info;")
            queryThree = ("select * from timesheet;")
            cur.execute(query)
            result = cur.fetchall()
            cur.execute(queryTwo)
            resultTwo = cur.fetchall()
            cur.execute(queryThree)
            resultThree = cur.fetchall()
            print result
            return render_template('index.html', selectedMenu='Home', loggedIn=True, error=False, myList=result, myListTwo=resultTwo, timeSheet=resultThree)
        else:
            return render_template('login.html', selectedMenu='Log In', loggedIn=False, error=True)
    return render_template('index.html', selectedMenu='Home', loggedIn=True, error=False)

def connectToDB():
  connectionString = 'dbname=payroll user=postgres password=payroll host=localhost'
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print "1"
        username= request.form['username']
        pw= request.form['password']
        query = ("select * from users WHERE username = %s AND password = %s;")
        print query
        cur.execute(query, (username,pw))
        result = cur.fetchone()
        print "hi"
        if result:
            print "test"
            session["username"] = username
            return redirect(url_for('mainIndex', name=username))
        else:
            return render_template('login.html', selectedMenu='Log In', error=True)
    return render_template('login.html', selectedMenu='Log In', error=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST': 
        print "1"
        username= request.form['username']
        pw= request.form['password']
        if username == "" or pw == "":
            return render_template('register.html', selectedMenu='Register', loggedIn=False, error=True)
        query = ("select * from users where username = '" + username + "';")
        print query
        cur.execute(query, (username))
        result = cur.fetchone()
        print result
        if result != None:
            print "Here 2"
            return render_template('register.html', selectedMenu='Register', loggedIn=False, error=True)
        else:
            print "3"
            userType = request.form['type']
            query = "INSERT INTO users values (%s, %s, %s);"
            print query
            cur.execute(query,(username, pw, userType))
            conn.commit()
            session["username"] = username
            return redirect(url_for('mainIndex', name=username))
    return render_template('register.html', selectedMenu='Register', loggedIn=False, error=False)
    
@app.route('/addEmployee', methods = ['GET', 'POST'])
def addEmployee():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        firstName= request.form['first']
        lastName= request.form['last']
        query = ("select * from employees where first_name = '" + firstName + "' AND last_name = '" + lastName + "';")
        print query
        cur.execute(query, (firstName, lastName))
        result = cur.fetchone()
        if result != None:
            print "Here 2"
            return redirect(url_for('addEmployee'))
        else:
            query = ("select count(employee_id) from employees;")
            cur.execute(query)
            result = cur.fetchone()
            print result
            query = "INSERT INTO employees values (%s, %s, %s);"
            print query
            resultTwo = int(result[0])
            resultTwo = resultTwo + 1
            cur.execute(query,(str(resultTwo), firstName, lastName))
            conn.commit()
            return render_template('addEmployeeConfirm.html', selectedMenu='Add Employee', loggedIn=True, error=True)
    return render_template('addEmployee.html', selectedMenu='Add Employee', loggedIn=True, error=True)
    

@app.route('/addJob', methods = ['GET','POST'])
def addJob():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        jobName = request.form['jobName']
        jobID = request.form['jobID']
        if jobName == "" or jobID == "":
            return render_template('addJob.html', selectedMenu='Add Job', loggedIn=True, error=True)
        query = ("SELECT * FROM job_info WHERE job_name = '" + jobName + "' AND job_id = '" + jobID + "';")
        print query
        cur.execute(query, (jobName, jobID))
        result = cur.fetchone()
        if result != None:
             print "WUSUP"
             return redirect(url_for('addJob'))
        else:
            query = ("select count(job_id) from job_info;")
            cur.execute(query)
            result = cur.fetchone()
            print result
            query = ("INSERT INTO job_info values (%s, %s, %s, '');")
            print query
            resultThree = int(result[0])
            resultThree = resultThree + 1
            cur.execute(query, (str(resultThree), jobName, jobID))
            conn.commit()
            return render_template('addJobConfirm.html', selectedMenu ='Add Job', loggedIn = True, error = True)
    return render_template('addJob.html', selectedMenu ='Add Job', loggedIn=True)
    
@app.route('/deleteEmployee', methods =['GET', 'POST'])
def deleteEmployee():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    queryThree = ("SELECT * FROM employees;")
    print queryThree
    cur.execute(queryThree)
    resultThree = cur.fetchall()
    if request.method == 'POST':
        employeeID = request.form['employee']
        query = ("DELETE from timesheet WHERE employee_id = %s;")
        query2 = ("DELETE from employees WHERE employee_id = %s;")
        print query
        cur.execute(query,(employeeID))
        cur.execute(query2,(employeeID))
        conn.commit()
        return render_template('deleteEmployeeConfirm.html', selectedMenu='Delete Employee', loggedIn=True, error=True)
    return render_template('deleteEmployee.html', selectedMenu ='Delete Employee', loggedIn=True, myList=resultThree)

    
@app.route('/enterHours', methods = ['GET', 'POST'])
def enterHours():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = ("SELECT * FROM employees;")
    print query
    cur.execute(query)
    result = cur.fetchall()
    queryTwo = ("SELECT * from job_info;")
    print queryTwo
    cur.execute(queryTwo)
    resultTwo = cur.fetchall()
    if request.method == 'POST':
        employeeID = request.form['employee']
        jobID = request.form['jobId']
        startTimeAM = request.form['startTimeAM']
        startTimeMin = request.form['startTimeMin']
        startTimeHour = request.form['startTimeHour']
        endTimeAM = request.form['endTimeAM']
        endTimeHour = request.form['endTimeHour']
        endTimeMin = request.form['endTimeMin']
        startMin = int(startTimeMin)
        startHour = int(startTimeHour)
        endMin = int(endTimeMin)
        endHour = int(endTimeHour)
        if startTimeAM == "PM" and endTimeAM == "AM":
            return render_template('enterHours.html', selectedMenu ='Enter Hours', loggedIn=True, myList=result, myListTwo=resultTwo, error=True)
        if startTimeAM == "PM":
            startHour += 12
        if endTimeAM == "PM":
            endHour += 12
        query = "INSERT INTO timesheet values (%s, %s, %s, %s, %s, %s, %s);"
        print query
        cur.execute(query,(employeeID, jobID, str(startMin), str(endMin), int(startHour), str(endHour), 0))
        conn.commit()
        return render_template('enterHourConfirm.html', selectedMenu='Enter Hours', loggedIn=True, error=True)
    return render_template('enterHours.html', selectedMenu ='Enter Hours', loggedIn=True, myList=result, myListTwo=resultTwo)
    
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return render_template('login.html', selectedMenu='Log In', loggedIn=False, error=False)
    
@app.route('/download', methods = ['GET', 'POST'])
def download():
   conn = connectToDB()
   cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
   query = "select * FROM timesheet"
   cur.execute(query)
   result = cur.fetchall()
   conn.commit()
   
   #writes to the file exportOutput.txt in the payroll folder
   
   fo = open("exportOutput.txt", "wb")
   fo.write("Timesheet Log" + "\n\n") 
   
   for resul in result:
    fo.write( str(resul)+"\n");
   fo.close()
   
   #maybe something like this to allow client to download file
   
   #testfile = urllib.URLopener()
   #testfile.retrieve("https://ide.c9.io/payroll430/payroll/exportOutput.txt", "exportOutput.txt")
   
  
   print("It's been downloaded!")
   return render_template('downloadtable.html', selectedMenu= 'Log In', loggedIn=True, error=False) 



if __name__ == '__main__':
    app.debug=True
    app.secret_key = 'AB9830923CJDH90TH32L/'
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(8080), debug=True)
