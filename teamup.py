from flask import Flask, render_template, request, url_for, redirect, session
from sqlalchemy import create_engine
import functions as func
from flask_mail import Mail, Message
from random import randint

app = Flask(__name__)

app.secret_key = "2secret4you"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'rwprojectmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'projectmail1!'

mail = Mail(app)

#page for recovering password
@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    if request.method == 'POST':
        try:
            #if user has succesfully verified their identity, let them reset their password
            if session['recovered']:
                try:
                    newpass = request.form['input']
                    if len(newpass) > 5:
                        func.createNewPassword(session['educatoremail'], newpass)
                        return redirect(url_for('educatorlogin'))
                    else:
                        return render_template("forgotpassword.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), prompt="Please create a new password", text="Sorry, that password is too short.")
                except:
                    return render_template("forgotpassword.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), prompt="Please create a new password", text="Sorry, that password is invalid.")
        except:
            pass
        try:
            #check if input is a code, then check the code against the sent code
            code = int(request.form['input'])
            if code == session['recoverycode']:
                session['recovered'] = True
                return render_template("forgotpassword.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), prompt="Please create a new password")
            else:
                return render_template("forgotpassword.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), prompt="Please enter the code sent to your email", text="Sorry, that code is incorrect.")
        except:
            pass
        try:
            #check if email is valid, then send a recovery code
            email = request.form['input']
            session['educatoremail'] = str(email)
            try:
                func.getEducator(str(email))
            except:
                return render_template("forgotpassword.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), text="Sorry, the email you entered does not match any existing records.", prompt="Please enter your email")
            session['recoverycode'] = randint(10000, 99999)
            msgbody = "Here is your recovery code: " + str(session['recoverycode'])
            msg = Message('TeamUp: Password Recovery', body = msgbody, sender = 'rwprojectmail@gmail.com', recipients = [str(email)])
            mail.send(msg)
            return render_template("forgotpassword.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), prompt="Please enter the code sent to your email (this may take a few minutes to arrive)")
        except:
            return render_template("forgotpassword.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), text="Sorry, we encountered an error. Please make sure you entered a valid email.", prompt="Please enter your email")
    return render_template("forgotpassword.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), prompt="Please enter your email")

#home page ====================================================================================================================
@app.route('/')
def index():
    return render_template("index.html", urle=url_for('educators'), urla=url_for('about'), urls=url_for('students'))

#about page
@app.route('/about')
def about():
    return render_template("about.html", urle=url_for('educators'), urli=url_for('index'), urls=url_for('students'))

#educator main page, includes login and sign up ==============================================================================
@app.route('/educators')
def educators():
    try:
        return render_template("educatorhome.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), urlc=url_for('createsurvey'), name=session['name'], urlr=url_for('educatorclasses'))
    except:
        pass
    return render_template("educators.html", urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), urlel=url_for('educatorlogin'), urles=url_for('educatorsignup'))

#educator login page
@app.route('/educatorlogin', methods=['GET', 'POST'])
def educatorlogin():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            result = func.educatorLogin(username, password)
            if result:
                teacher = func.getEducator(username)
                session['name'] = teacher[0]
                session['id'] = teacher[1]
                return render_template("educatorhome.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), urlc=url_for('createsurvey'), urlr=url_for('educatorclasses'), name=session['name'])
            else:
                return render_template("educatorlogin.html", urle=url_for('educators'), urlfp=url_for('forgotpassword'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), text="Sorry, the username and password do not match any existing records")
        except:
            return render_template("educatorlogin.html", urle=url_for('educators'), urlfp=url_for('forgotpassword'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), text="Sorry, we encountered an error")
    return render_template("educatorlogin.html", urle=url_for('educators'), urlfp=url_for('forgotpassword'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'))

#educator sign up page
@app.route('/educatorsignup', methods=['GET', 'POST'])
def educatorsignup():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            password2 = request.form['password2']
            name = request.form['fullname']
            session['name'] = name
            if len(username) < 5 or len(password) < 5 or len(name) < 5:
                return render_template("educatorsignup.html", urli=url_for('index'), urle=url_for('educators'), urla=url_for('about'), urls=url_for('students'), text="Sorry, your username, password, and name must be at least 5 characters.")
            if '@' not in username:
                return render_template("educatorsignup.html", urli=url_for('index'), urle=url_for('educators'), urla=url_for('about'), urls=url_for('students'), text="Sorry, please enter a valid email address.")
            if password != password2:
                return render_template("educatorsignup.html", urli=url_for('index'), urle=url_for('educators'), urla=url_for('about'), urls=url_for('students'), text="Sorry, your passwords must match.")
            if func.findeducator(username):
                func.inputTeacherInformation(username, password, name)
                teacher = func.getEducator(username)
                session['id'] = teacher[1]
                return render_template("educatorhome.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), urlc=url_for('createsurvey'), urlr=url_for('educatorclasses'), name=session['name'])
            else:
                return render_template("educatorsignup.html", urli=url_for('index'), urle=url_for('educators'), urla=url_for('about'), urls=url_for('students'), text="Sorry, the username you entered already exists.")
        except:
            return render_template("educatorsignup.html", urli=url_for('index'), urle=url_for('educators'), urla=url_for('about'), urls=url_for('students'), text="Sorry, we encountered an error.")
    return render_template("educatorsignup.html", urli=url_for('index'), urle=url_for('educators'), urla=url_for('about'), urls=url_for('students'))

#create a survey
@app.route('/createsurvey', methods=['GET', 'POST'])
def createsurvey():
    if request.method == 'POST':
        try:
            class_name = request.form['classname']
            s1 = request.form['skill1']
            s2 = request.form['skill2']
            s3 = request.form['skill3']
            s4 = request.form['skill4']
            team_size = int(request.form['teamsize'])
            class_size = int(request.form['classsize'])
            if len(s1) < 2 or len(s2) < 2 or len(s3) < 2 or len(s4) < 2 or len(class_name) < 2:
                return render_template("createsurvey.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), text="Sorry, we encountered an error. Please enter valid answers for all the questions.")
            if team_size < 4 or class_size < 4 * team_size or class_size > 120:
                return render_template("createsurvey.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), text="Sorry, the team size must be between 4 and 8 (inclusive) and there must be enough students to form at least four teams (with at most 120 students).")
            class_id = func.inputClassInformation(class_name, session['id'], s1, s2, s3, s4, team_size, class_size)
            return render_template("success.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), classname=class_name, classid=class_id)
        except:
            return render_template("createsurvey.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), text="Sorry, we encountered an error. Please enter valid answers for all the questions, and be sure to log in as an educator.")
    return render_template("createsurvey.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'))

#educator class select page
@app.route('/educatorclasses', methods=['GET', 'POST'])
def educatorclasses():
    #if the user has selected a class, retrieve the teams or generate the teams (if they haven't been generated yet) and store them
    if request.method == 'POST':
        try:
            classid = request.form['choice']
            students = func.getStudentScores(classid)
            if students[0] == 'inc':
                students.pop(0)
                return render_template("results.html", urla=url_for('about'), urle=url_for('educators'), urli=url_for('index'), urls=url_for('students'), text="It appears that not all students have completed the survey yet. Please check again later. Here are the students that have currently submitted their survey:", students=students)
            if students[0] == 'error':
                return render_template("results.html", urla=url_for('about'), urle=url_for('educators'), urli=url_for('index'), urls=url_for('students'), text="Sorry, we encountered an error. This may be a result of corrupted inputs from the surveys.")
            if students[0] == 'grouped':
                teams = func.getExistingTeams(classid)
                image = func.createPicture()
                return render_template("results.html", urla=url_for('about'), urle=url_for('educators'), urli=url_for('index'), urls=url_for('students'), teams=teams, image=image)
            func.inputGroupNo(students, classid)
            teams = func.getExistingTeams(classid)
            image = func.createPicture()
            return render_template("results.html", teams=teams, urla=url_for('about'), urle=url_for('educators'), urli=url_for('index'), urls=url_for('students'), image=image)
        except:
            classes = func.pullclasses(str(session['id']))
            return render_template("educatorclasses.html", urla=url_for('about'), classes=classes, urle=url_for('educators'), urli=url_for('index'), urls=url_for('students'), text="Sorry, we encountered an error. Please make sure you're signed in as an educator, and have shared the class ID with your students.")
    try:
        classes = func.pullclasses(str(session['id']))
        if not classes:
            return render_template("educatorclasses.html", urla=url_for('about'), urle=url_for('educators'), urli=url_for('index'), urls=url_for('students'), text="Sorry, you have not created any classes. Return to the educator page and create a survey to register a class.")
    except:
        return render_template("educatorclasses.html", urla=url_for('about'), urle=url_for('educators'), urli=url_for('index'), urls=url_for('students'), text="Sorry, we encountered an error.")
    return render_template("educatorclasses.html", classes=classes, urla=url_for('about'), urle=url_for('educators'), urli=url_for('index'), urls=url_for('students'))

#student home page, includes survey link and check teams ========================================================================
@app.route('/students')
def students():
    return render_template("students.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urlsu=url_for('selectclass'), urlsl=url_for('studentlogin'))

#student login page
@app.route('/studentlogin', methods=['GET', 'POST'])
def studentlogin():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            result = func.studentLogin(username, password)
            if not result:
                return render_template("studentresults.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), text="Sorry, the teams have not been assigned yet. Please check back later.")
            elif result[0] == -1:
                return render_template("studentlogin.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), text="Sorry, the username and password do not match any existing records")
            else:
                return render_template("studentresults.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), team=result)
        except:
            return render_template("studentlogin.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), text="Sorry, we encountered an error")
    return render_template("studentlogin.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'))

#select class page for students to find their class survey and populate the skills
@app.route('/selectclass', methods=['GET', 'POST'])
def selectclass():
    if request.method == 'POST':
        try:
            classcode = request.form['classcode']
            skills = func.pullskills(classcode)
            session['skill1'] = skills[0]
            session['skill2'] = skills[1]
            session['skill3'] = skills[2]
            session['skill4'] = skills[3]
            session['studentclass'] = classcode
        except:
            return render_template("selectclass.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), text="Sorry, that was not a valid class code.")
        return redirect(url_for('survey'))
    return render_template("selectclass.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'))

#survey page
@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        mbti = []
        result = ''
        E = 0
        I = 0
        S = 0
        N = 0
        T = 0
        F = 0
        J = 0
        P = 0
        username = ''
        password = ''
        name = ''
        #get user's username, password, and name, and check their validity
        try:
            username = request.form['username']
            password = request.form['password']
            password2 = request.form['password2']
            name = request.form['name']
            if len(username) < 5 or len(password) < 5 or len(name) < 5:
                return render_template("mbti.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), result="Sorry, your email, name, and password must be at least 5 characters.")
            if password != password2:
                return render_template("mbti.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), result="Sorry, your passwords must match.")
        except:
            result = "Sorry, please complete the form in its entirety."
            return render_template("mbti.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), result=result)
        for i in range(1, 21):
            question = 'q' + str(i)
            try:
                mbti.append(request.form[question])
            except:
                result = "Sorry, please complete the form in its entirety"
                return render_template("mbti.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), result=result)
        #get the skills scores
        try:
            skill1 = int(request.form['q21'])
            skill2 = int(request.form['q22'])
            skill3 = int(request.form['q23'])
            skill4 = int(request.form['q24'])
        except:
            result = "Sorry, please complete the form in its entirety"
            return render_template("mbti.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), result=result)
        #get the personality scores
        for i in range(0, 20):
            if mbti[i] == 'E':
                E += 1
            if mbti[i] == 'I':
                I += 1
            if mbti[i] == 'S':
                S += 1
            if mbti[i] == 'N':
                N += 1
            if mbti[i] == 'T':
                T += 1
            if mbti[i] == 'F':
                F += 1
            if mbti[i] == 'J':
                J += 1
            if mbti[i] == 'P':
                P += 1
        if E > I:
            result += 'E'
        else:
            result += 'I'
        if S > N:
            result += 'S'
        else:
            result += 'N'
        if T > F:
            result += 'T'
        else:
            result += 'F'
        if J > P:
            result += 'J'
        else:
            result += 'P'
        #calculate the personality type scores
        analyst = I + N + T
        diplomat = E + N + F
        leader = E + S + J
        explorer = I + S + P
        if not func.findstudent(username):
            return render_template("mbti.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), result="Sorry, the username you entered already exists")
        func.inputInformation(username, session['studentclass'], password, name, analyst, diplomat, leader, explorer, skill1, skill2, skill3, skill4)
        result = "Your MBTI type is: " + result
        return render_template("mbti.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), result=result, text1="Thank you for completing the survey! Your results have been recorded.", text2="To learn about what this means, check out our about page.")
    return render_template("survey.html", urle=url_for('educators'), urli=url_for('index'), urla=url_for('about'), urls=url_for('students'), skill1=session['skill1'], skill2=session['skill2'], skill3=session['skill3'], skill4=session['skill4'])

app.run(host='0.0.0.0', port=5000, debug=True)