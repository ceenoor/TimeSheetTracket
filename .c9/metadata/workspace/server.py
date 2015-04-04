{"changed":true,"filter":false,"title":"server.py","tooltip":"/server.py","value":"import psycopg2\nimport psycopg2.extras\nimport os\nfrom flask import Flask, session, redirect, url_for, escape, render_template, request\n\n\napp = Flask(__name__)\napp.secret_key=os.urandom(24).encode('hex')\ncurrentUser = ''\n\n@app.route('/', methods = ['GET', 'POST'])\ndef mainIndex():\n    if request.method == 'GET':\n        conn = connectToDB()\n        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)\n        if request.args.get('name') == None:\n            return redirect(url_for('login'))\n        else:\n         name = request.args.get('name')\n        print name\n        if name in session['username']:\n            print \"welcome\"\n            query = (\"select * from employees;\")\n            queryTwo = (\"select * from job_info;\")\n            cur.execute(query)\n            result = cur.fetchall()\n            cur.execute(queryTwo)\n            resultTwo = cur.fetchall()\n            print result\n            return render_template('index.html', selectedMenu='Home', loggedIn=True, error=False, myList=result, myListTwo=resultTwo)\n        else:\n            return render_template('login.html', selectedMenu='Log In', loggedIn=False, error=True)\n    return render_template('index.html', selectedMenu='Home', loggedIn=True, error=False)\n\ndef connectToDB():\n  connectionString = 'dbname=payroll user=postgres password=payroll host=localhost'\n  try:\n    return psycopg2.connect(connectionString)\n  except:\n    print(\"Can't connect to database\")\n\n@app.route('/login', methods=['GET', 'POST'])\ndef login():\n    if request.method == 'POST':\n        conn = connectToDB()\n        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)\n        print \"1\"\n        username= request.form['username']\n        pw= request.form['password']\n        query = (\"select * from users WHERE username = %s AND password = %s;\")\n        print query\n        cur.execute(query, (username,pw))\n        result = cur.fetchone()\n        print \"hi\"\n        if result:\n            print \"test\"\n            session[\"username\"] = username\n            return redirect(url_for('mainIndex', name=username))\n        else:\n            return render_template('login.html', selectedMenu='Log In', error=True)\n    return render_template('login.html', selectedMenu='Log In', error=False)\n\n@app.route('/register', methods=['GET', 'POST'])\ndef register():\n    conn = connectToDB()\n    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)\n    if request.method == 'POST': \n        print \"1\"\n        username= request.form['username']\n        query = (\"select * from users where username = '\" + username + \"';\")\n        print query\n        cur.execute(query, (username))\n        result = cur.fetchone()\n        print result\n        if result != None:\n            print \"Here 2\"\n            return render_template('register.html', selectedMenu='Register', loggedIn=False, error=True)\n        else:\n            print \"3\"\n            pw= request.form['password']\n            userType = request.form['type']\n            query = \"INSERT INTO users values (%s, %s, %s);\"\n            print query\n            cur.execute(query,(username, pw, userType))\n            conn.commit()\n            session[\"username\"] = username\n            return redirect(url_for('mainIndex', name=username))\n    return render_template('register.html', selectedMenu='Register', loggedIn=False, error=False)\n    \n@app.route('/addEmployee', methods = ['GET', 'POST'])\ndef addEmployee():\n    conn = connectToDB()\n    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)\n    if request.method == 'POST':\n        firstName= request.form['first']\n        lastName= request.form['last']\n        query = (\"select * from employees where first_name = '\" + firstName + \"' AND last_name = '\" + lastName + \"';\")\n        print query\n        cur.execute(query, (firstName, lastName))\n        result = cur.fetchone()\n        if result != None:\n            print \"Here 2\"\n            return redirect(url_for('addEmployee'))\n        else:\n            query = (\"select count(employee_id) from employees;\")\n            cur.execute(query)\n            result = cur.fetchone()\n            print result\n            query = \"INSERT INTO employees values (%s, %s, %s);\"\n            print query\n            resultTwo = int(result[0])\n            resultTwo = resultTwo + 1\n            cur.execute(query,(str(resultTwo), firstName, lastName))\n            conn.commit()\n            return render_template('addEmployeeConfirm.html', selectedMenu='Add Employee', loggedIn=True, error=True)\n    return render_template('addEmployee.html', selectedMenu='Add Employee', loggedIn=True, error=True)\n    \n\n@app.route('/addJob', methods = ['GET','POST'])\ndef addJob():\n    conn = connectToDB()\n    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)\n    if request.method == 'POST':\n        jobName = request.form['jobName']\n        jobID = request.form['jobID']\n        query = (\"SELECT * FROM job_info WHERE job_name = '\" + jobName + \"' AND job_id = '\" + jobID + \"';\")\n        print query\n        cur.execute(query, (jobName, jobID))\n        result = cur.fetchone()\n        if result != None:\n             print \"WUSUP\"\n             return redirect(url_for('addJob'))\n        else:\n            query = (\"select count(job_id) from job_info;\")\n            cur.execute(query)\n            result = cur.fetchone()\n            print result\n            query = \"INSERT INTO job_info values (%s, %s, %s, '');\"\n            print query\n            resultThree = int(result[0])\n            resultThree = resultThree + 1\n            cur.execute(query, (str(resultThree), jobName, jobID))\n            conn.commit()\n            return render_template('addJobConfirm.html', selectedMenu ='Add Job', loggedIn = True, error = True)\n    return render_template('addJob.html', selectedMenu ='Add Job', loggedIn=True)\n\n    \n@app.route('/enterHours', methods = ['GET', 'POST'])\ndef enterHours():\n    conn = connectToDB()\n    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)\n    query = (\"SELECT * FROM employees;\")\n    print query\n    cur.execute(query)\n    result = cur.fetchall()\n    queryTwo = (\"SELECT * from job_info;\")\n    print queryTwo\n    cur.execute(queryTwo)\n    resultTwo = cur.fetchall()\n    if request.method == 'POST':\n        jobName = request.form['jobName']\n        jobID = request.form['jobID']\n        if result != None:\n             print \"WUSUP\"\n             return redirect(url_for('addJob'))\n        else:\n            query = (\"select count(job_id) from job_info;\")\n            cur.execute(query)\n            result = cur.fetchone()\n            print result\n            query = \"INSERT INTO job_info values (%s, %s, %s, '');\"\n            print query\n            resultThree = int(result[0])\n            resultThree = resultThree + 1\n            cur.execute(query, (str(resultThree), jobName, jobID))\n            conn.commit()\n            return render_template('addJobConfirm.html', selectedMenu ='Enter Hours', loggedIn = True, error = True)\n    return render_template('enterHours.html', selectedMenu ='Enter Hours', loggedIn=True, myList=result, myListTwo=resultTwo)\n    \n@app.route('/logout')\ndef logout():\n    # remove the username from the session if it's there\n    session.pop('username', None)\n    return render_template('login.html', selectedMenu='Log In', loggedIn=False, error=False)\n    \n#@app.route('/download', methods = ['GET'])\n#def download():\n#   conn = connectToDB()\n#   cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)\n#   \n\n\nif __name__ == '__main__':\n    app.debug=True\n    app.secret_key = 'AB9830923CJDH90TH32L/'\n    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(8080), debug=True)\n","undoManager":{"mark":39,"position":39,"stack":[[{"group":"doc","deltas":[{"start":{"row":87,"column":2},"end":{"row":87,"column":3},"action":"insert","lines":["#"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":102},"end":{"row":76,"column":103},"action":"remove","lines":["e"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":101},"end":{"row":76,"column":102},"action":"remove","lines":["u"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":100},"end":{"row":76,"column":101},"action":"remove","lines":["r"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":99},"end":{"row":76,"column":100},"action":"remove","lines":["T"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":99},"end":{"row":76,"column":100},"action":"insert","lines":["f"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":100},"end":{"row":76,"column":101},"action":"insert","lines":["a"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":101},"end":{"row":76,"column":102},"action":"insert","lines":["l"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":101},"end":{"row":76,"column":102},"action":"remove","lines":["l"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":100},"end":{"row":76,"column":101},"action":"remove","lines":["a"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":99},"end":{"row":76,"column":100},"action":"remove","lines":["f"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":99},"end":{"row":76,"column":100},"action":"insert","lines":["F"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":100},"end":{"row":76,"column":101},"action":"insert","lines":["A"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":101},"end":{"row":76,"column":102},"action":"insert","lines":["L"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":102},"end":{"row":76,"column":103},"action":"insert","lines":["S"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":103},"end":{"row":76,"column":104},"action":"insert","lines":["E"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":103},"end":{"row":76,"column":104},"action":"remove","lines":["E"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":102},"end":{"row":76,"column":103},"action":"remove","lines":["S"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":101},"end":{"row":76,"column":102},"action":"remove","lines":["L"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":100},"end":{"row":76,"column":101},"action":"remove","lines":["A"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":100},"end":{"row":76,"column":101},"action":"insert","lines":["a"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":101},"end":{"row":76,"column":102},"action":"insert","lines":["l"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":102},"end":{"row":76,"column":103},"action":"insert","lines":["s"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":103},"end":{"row":76,"column":104},"action":"insert","lines":["e"]}]}],[{"group":"doc","deltas":[{"start":{"row":87,"column":2},"end":{"row":87,"column":3},"action":"remove","lines":["#"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":103},"end":{"row":76,"column":104},"action":"remove","lines":["e"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":102},"end":{"row":76,"column":103},"action":"remove","lines":["s"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":101},"end":{"row":76,"column":102},"action":"remove","lines":["l"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":100},"end":{"row":76,"column":101},"action":"remove","lines":["a"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":99},"end":{"row":76,"column":100},"action":"remove","lines":["F"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":99},"end":{"row":76,"column":100},"action":"insert","lines":["T"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":100},"end":{"row":76,"column":101},"action":"insert","lines":["r"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":101},"end":{"row":76,"column":102},"action":"insert","lines":["u"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":102},"end":{"row":76,"column":103},"action":"insert","lines":["e"]}]}],[{"group":"doc","deltas":[{"start":{"row":87,"column":91},"end":{"row":87,"column":95},"action":"remove","lines":["True"]}]}],[{"group":"doc","deltas":[{"start":{"row":87,"column":91},"end":{"row":87,"column":92},"action":"insert","lines":["F"]}]}],[{"group":"doc","deltas":[{"start":{"row":87,"column":92},"end":{"row":87,"column":93},"action":"insert","lines":["a"]}]}],[{"group":"doc","deltas":[{"start":{"row":87,"column":93},"end":{"row":87,"column":94},"action":"insert","lines":["l"]}]}],[{"group":"doc","deltas":[{"start":{"row":87,"column":94},"end":{"row":87,"column":95},"action":"insert","lines":["s"]}]}],[{"group":"doc","deltas":[{"start":{"row":87,"column":95},"end":{"row":87,"column":96},"action":"insert","lines":["e"]}]}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":5,"column":0},"end":{"row":5,"column":0},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1428003019000}