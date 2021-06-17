#Database connections
#function to connect to our database
def connectdb():
    from sqlalchemy import create_engine

    conn_string = 'mysql://{user}:{password}@{host}/{db}?charset={encoding}'.format(
        host = '35.245.25.171:3306',
        user = 'root',
        db = 'student',
        password = 'dwdstudent2015',
        encoding = 'utf8mb4')

    engine = create_engine(conn_string)
    
    con = engine.connect()
    return con

#===================================================================================================================#
#Password Hashing Functions
#returns a hashed version of the provided password
def hash_password(password):
    import hashlib, binascii, os
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
#checks a hashed password against a provided password
def verify_password(stored_password, provided_password):
    import hashlib, binascii, os
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

#===================================================================================================================#
#Logins
#login function for students, returns [-1] if failed to log in, otherwise, returns the student's group (or empty if they haven't been assigned a group yet)
def studentLogin(username, provided_password):
    con = connectdb()
    con.execute("USE team_building_tool")
    stored_password = con.execute('SELECT password FROM students WHERE username = ' + "'" + username + "'").fetchone()
    
    stored_password_str = str(stored_password)
    trim_password = stored_password_str[2:-3]
    
    verf_pass = verify_password(trim_password, provided_password)
    
    print(verf_pass)
    
    if verf_pass:
        group_no  = con.execute('SELECT group_no FROM students WHERE username = ' + "'" + username + "'").fetchone()

        group_no = str(group_no)
        group_no = group_no[1:-2]
        
        if group_no == '0':
            return []
        
        group = getStudentTeam(group_no)
        return group
        
    return [-1]

#login function for educators, returns true if log in is correct
def educatorLogin(username, provided_password):
    con = connectdb()
    con.execute("USE team_building_tool")
    stored_password = con.execute('SELECT password FROM teachers WHERE username = ' + "'" + username + "'").fetchone()
    
    stored_password_str = str(stored_password)
    trim_password = stored_password_str[2:-3]
    
    verf_pass = verify_password(trim_password, provided_password)
    return verf_pass

#===================================================================================================================#
#Check if users exists
#checks if student already exists in the students table, returns true if they are unique
def findstudent(student_username):  
    con = connectdb()
    con.execute('use team_building_tool')
    
    student_username.lower()
    
    student_un = con.execute("select * from students where username = " + "'" + student_username + "'").fetchone()
   
    if student_un is None:
        return True
        
    else:
        return False
    return False

#checks if educator already exists, returns true if they are unique
def findeducator(educator_username):
    con = connectdb()
    con.execute('use team_building_tool')
    
    educator_username.lower()
    
    educator_un = con.execute("select * from teachers where username = " + "'" + educator_username + "'").fetchone()
   
    if educator_un is None:
        return True
    else:
        return False
    return False

#checks if the students have already been grouped, returns true if they have
def checkteam(class_id):
    con = connectdb()
    con.execute("USE team_building_tool")
    number = con.execute("select group_no from students where class_id = " + "'" + class_id + "'").fetchone()
    
    num = str(number)
    num = num[1:-2]
    print(type(num))
    
    if num is "0":
        return False
    else:
        return True

#===================================================================================================================#
#Input informations
#inputs a student row into the student table
def inputInformation(username, class_id, password, name, analyst, diplomat, leader, explorer, skill1, skill2, skill3, skill4):
    con = connectdb()
    db_name = 'team_building_tool'
    table_name = 'students'
    con.execute("USE team_building_tool")
    
    student_id = con.execute("SELECT * FROM students ORDER BY student_id DESC LIMIT 1")
    
    username = username.strip().lower()
    password = password.strip()
    name = name.strip()
    
    row = student_id.fetchone()
    try:
        student_id = row[0] + 1
    except:
        student_id = 1
        
    hashed_password = hash_password(password)
    group_no = 0
    
    query_template = '''INSERT IGNORE INTO {db}.{table}(student_id, class_id, username, password, name, analyst, diplomat, leader, explorer, skill1, skill2, skill3, skill4, group_no) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(db=db_name, table=table_name)

    print("Inserting student", name)
    
    query_parameters = (student_id, class_id, username, hashed_password, name, analyst, diplomat, leader, explorer, skill1, skill2, skill3, skill4, group_no)
    con.execute(query_template, query_parameters)   

#inputs a class in the class table
def inputClassInformation(class_name, teacher_id, s1, s2, s3, s4, team_size, class_size):
    #input accordingly 
    import random
    con = connectdb()
    db_name = 'team_building_tool'
    table_name = 'class'
    con.execute("USE team_building_tool")
    
    class_name = class_name.strip()
    
    class_id = str(class_name) + str(teacher_id) + str(random.randint(1,999))
    class_id = class_id.strip()
    class_id = class_id.replace(" ","")
    
    s1 = s1.strip()
    s2 = s2.strip()
    s3 = s3.strip()
    s4 = s4.strip()
    
    query_template = '''INSERT IGNORE INTO {db}.{table}(class_id, class_name, teacher_id, skill1, skill2, skill3, skill4, team_size, class_size) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(db=db_name, table=table_name)

    print("Inserting class", class_name)
    query_parameters = (class_id, class_name, teacher_id, s1, s2, s3, s4, team_size, class_size)
    con.execute(query_template, query_parameters)
    return class_id

#inputs a teacher in the teacher table
def inputTeacherInformation(username, password, name):
    con = connectdb()
    db_name = 'team_building_tool'
    table_name = 'teachers'
    con.execute("USE team_building_tool")
    
    teacher_id = con.execute("SELECT * FROM teachers ORDER BY teacher_id DESC LIMIT 1")
    
    username = username.strip().lower()
    password = password.strip()
    name = name.strip()
    
    row = teacher_id.fetchone()
    try:
        teacher_id = row[0] + 1
    except:
        teacher_id = 1
        
    hashed_password = hash_password(password)
    
    query_template = '''INSERT IGNORE INTO {db}.{table}(teacher_id, username, password, name) 
                        VALUES (%s, %s, %s, %s)'''.format(db=db_name, table=table_name)

    print("Inserting teacher", name)
    
    query_parameters = (teacher_id, username, hashed_password, name)
    con.execute(query_template, query_parameters)
    
#inputs the group numbers of each student in the students table
def inputGroupNo(students, class_id):

    con = connectdb()
    db_name = 'team_building_tool'
    table_name = 'students'
    
    con.execute("USE team_building_tool")
    con.execute("SET SQL_SAFE_UPDATES = 0")
    teamsize = con.execute("select team_size from class where class_id = '" + class_id + "'")
    
    group_no = 0
    
    sizerow = teamsize.fetchone()
    size = int(sizerow[0])
    
    import algorithm as algo
    
    group_len = algo.algorithm(students, size)
        
    for group in group_len:
        group_no = group_no + 1
        
        for individual in group:
            con.execute("UPDATE students set group_no = " + str(group_no) + " WHERE student_id = '" + str(individual) +"'")
    return True

#===================================================================================================================#
#return a list of teams in a given class, if the teams have already been assigned from the SQL workbench
def getExistingTeams(class_id):
    import pandas as pd
    
    con = connectdb()
    con.execute("USE team_building_tool")
    
    groups = "SELECT group_no, name FROM students WHERE class_id = '" + class_id + "'"
    
    data = pd.read_sql(groups, con)
    
    grouped = data.values.tolist()
    grouped.sort(key=lambda x: x[0])
    
    group = []
    finalgroups = []
    previous = 1
    
    for g in grouped:
        current = g[0]
        if current == previous:
            group.append(g[1])
        else:
            previous = current
            finalgroups.append(group)
            group = [g[1]]
            
    finalgroups.append(group)
    
    return finalgroups

#returns the names of each team member for a given group
def getStudentTeam(group_no):
    con = connectdb()
    con.execute("USE team_building_tool")
    
    group_list = []
    
    group = con.execute("SELECT name FROM students WHERE group_no =" + str(group_no))
    
    for name in group:
        name = str(name)
        name = name[2:-3]
        group_list.append(name)
        
    return(group_list)

#return an educators id and username from the SQL workbench
def getEducator(username):
    con = connectdb()
    con.execute("USE team_building_tool")
    
    educatorinfo = con.execute("SELECT name, teacher_id FROM teachers WHERE username = '" + username + "'")
    
    my_list = []

    for i in educatorinfo:
        my_list.append(i)
        
    return my_list[0]
             
#===================================================================================================================#
#returns a list of student scores by student id for a given class
def getStudentScores(class_id):
    import pandas as pd

    con = connectdb()
    con.execute('use team_building_tool')
    traits = "select student_id, name, analyst, diplomat, leader, explorer, skill1, skill2, skill3, skill4 from students where class_id = '" + class_id + "'"
    groupno = con.execute("select group_no from students where class_id = '" + class_id + "'")
    class_size = con.execute("select class_size from class where class_id = '" + class_id + "'")
    
    data = pd.read_sql(traits, con)
    
    pivot = data.pivot_table(
        index = 'student_id',
        aggfunc = 'sum',
        values = ['analyst', 'diplomat', 'leader','explorer', 'skill1', 'skill2', 'skill3', 'skill4']
    )
        
    column_order = ['analyst', 'leader', 'diplomat','explorer', 'skill1', 'skill2', 'skill3', 'skill4']
    studentdata = pivot.reindex(column_order, axis=1)
    
    students = data.values.tolist()
    students = [x[0] for x in students]
    names = data.values.tolist()
    names = [x[1] for x in names]
    studentiddata = studentdata.values.tolist()
    
    try:
        grouprow = groupno.fetchone()
        group = int(grouprow[0])
        sizerow = class_size.fetchone()
        size = int(sizerow[0])
        if size > len(students):
            names.insert(0, 'inc')
            return names
        if group != 0:
            return ['grouped']
    except:
        return ['error']
    
    for i in range(0, len(studentiddata)):
        studentiddata[i].insert(0, students[i])
    
    return studentiddata

#===================================================================================================================#
#update's the teacher table with a new password if they forgot their old password
def createNewPassword(username, provided_password):
    con = connectdb()
    
    new_password = hash_password(provided_password)
    
    con.execute("SET SQL_SAFE_UPDATES = 0")
    con.execute("USE team_building_tool")
    con.execute("UPDATE teachers SET password = '" + new_password + "' WHERE username = '" + username + "'")
    return True

#===================================================================================================================#
#Pull for tags
#returns a list of skills in a given class
def pullskills(class_id):
    con = connectdb()
    con.execute("USE team_building_tool")
    skills = con.execute("select skill1, skill2, skill3, skill4 from class where class_id = " + "'" + class_id + "'").fetchone()
    
    skill_list = []
    for i in skills:
        skill_list.append(i)
        
    return skill_list

#returns a list of classes for a given teacher
def pullclasses(teacher_id):
    con = connectdb()
    con.execute("USE team_building_tool")
    classinfo = con.execute("select class_name, class_id from class where teacher_id = " + "'" + teacher_id + "'")
    
    classinfo_list = []
    classes = []
    
    for course in classinfo:
        for i in course:
            classinfo_list.append(i)
    
    if len(classinfo_list) == 0:
        return []
    
    for i in range(0, len(classinfo_list), 2):
        temp = [classinfo_list[i], classinfo_list[i + 1]]
        classes.append(temp)
    
    return classes

#===================================================================================================================#
#function to create pie chart of personality types
def createPicture():
    import matplotlib
    matplotlib.use('Agg')
    import pandas as pd
    con = connectdb()
    
    con.execute('use team_building_tool')
    personality = 'select student_id, analyst, diplomat, leader, explorer from students'
    
    data = pd.read_sql(personality, con)
    
    #Creating the Pivot
    pivot = data.pivot_table(
        index = 'student_id',
        aggfunc = 'sum',
        values = ['analyst', 'diplomat', 'leader','explorer']
    )
    
    #Renaming columns because Leader and Explorer are somehow switched
    pivot.columns = ['Analyst', 'Diplomat','Leader','Explorer']
    pivot

    #Aggregating Columns
    analyst_score = pivot['Analyst'].sum()
    diplomat_score = pivot['Diplomat'].sum()
    explorer_score = pivot['Leader'].sum()
    leader_score = pivot['Explorer'].sum()
    
    #Creating the picture
    pivot = pd.DataFrame(
        {'Score': [analyst_score, diplomat_score , leader_score, explorer_score]},  
        index=['Analyst', 'Diplomat', 'Leader', 'Explorer']
    )

    colors = ["#01afef", "#0f437a", "#e8f4f8","#aed7e5"]
    plot = pivot.plot.pie(y='Score', colors = colors, figsize=(5, 5),legend = False)
    
    #Saved a picture
    filename = 'static/test.png'
    fig = plot.get_figure()
    fig.savefig(filename, transparent=True)
    fig.clear()
    
    return filename
