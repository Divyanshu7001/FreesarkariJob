from flask import Flask, request, render_template, redirect,session,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json
from datetime import datetime 
from scraper import govt_job_scraper 
from apscheduler.schedulers.background import BackgroundScheduler
from auth import send_otp
from notification import send_mail
import time 

''' CONFIGURE START'''

params = json.load(open('config.json','r'))['params']
Web_Title = params['Title']
sql_uri = params['local_uri'] 
owner_gmail = params['tracking_gmail']
''' CONFIGURE END'''

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = sql_uri
db = SQLAlchemy(app)
app.secret_key = 'a35FOAU9043(Q34-50)jkhkw3f5435'


''' ***** initialize the sql table ***** '''

# bsic job data
class basic_info(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    counter_id = db.Column(db.String, nullable = False)
    genre = db.Column(db.String, nullable = False)
    posts = db.Column(db.Integer, nullable = False)
    post_name = db.Column(db.String, nullable = False)
    qualification = db.Column(db.String, nullable = False)
    date = db.Column(db.String, nullable = False)
    link = db.Column(db.String, nullable = False)

class admit_info(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    counter_id = db.Column(db.String, nullable = False)
    title = db.Column(db.String, nullable = False)
    data = db.Column(db.JSON, nullable = False)

class result_info(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    counter_id = db.Column(db.String, nullable = False)
    title = db.Column(db.String, nullable = False)
    data = db.Column(db.JSON, nullable = False)

class job_details(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    counter_id = db.Column(db.String, nullable = False)
    overview = db.Column(db.JSON, nullable = False)
    basic_details = db.Column(db.JSON, nullable = False)
    discription = db.Column(db.JSON, nullable = False)
    date = db.Column(db.JSON, nullable = False)
    eligibility = db.Column(db.JSON, nullable = False)
    payment = db.Column(db.JSON, nullable = False)
    links = db.Column(db.JSON, nullable = False)

class user(db.Model):
    sno = db.Column(db.Integer, primary_key =True)
    name= db.Column(db.String,nullable =False)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    date = db.Column(db.DateTime, nullable = False)

""" ******** supporting functions for datasending oparations ********  """

""" sending page_1 """

# sending detailed information of jobs

def send_job_details(job_data):
    ''' this function is a part of pushing data for the details of data'''
    # this returns a list of data
    file = job_data

    for i in file:
        counter_id = i['id']
        data_chunk = i['data']
        overview = data_chunk['overview']
        basic = data_chunk['basic']
        discription = data_chunk['discription']
        dates = data_chunk['dates']
        payment = data_chunk['payment']
        eligibility = data_chunk['eligibility']
        links = data_chunk['links']

        entry = job_details(counter_id=counter_id, overview=overview ,basic_details=basic ,discription=discription ,date=dates,eligibility=eligibility ,payment=payment ,links=links)
        print(counter_id)
        db.session.execute(text('SET @num :=0; UPDATE job_details SET sno = @num:= @num+1; ALTER TABLE job_details AUTO_INCREMENT =1;'))
        db.session.add(entry)
        db.session.commit()
        print('done')

# sending basic details and detailed details of jobs to database
def send_jobs():

    basic_data,detailed_data = govt_job_scraper.get_job()
    data = basic_data['data']
    print('pushing basic info for jobs')
    for i in data:
        title = i['title']
        for itr, info  in enumerate(i['col_id']):
            counter_id = info
            genre = i['col1'][itr]
            post_number = i['col2'][itr]
            post_name = i['col3'][itr]
            qualificaiton = i['col4'][itr]
            date = i['col5'][itr]
            link = i['col6'][itr]

            entry = basic_info( title = title ,genre = genre , posts = post_number, post_name = post_name, qualification = qualificaiton, date = date, link = link, counter_id = counter_id)
            db.session.execute(text('SET @num :=0; UPDATE basic_info SET sno = @num:= @num+1; ALTER TABLE basic_info AUTO_INCREMENT =1;'))
            db.session.add(entry)
            db.session.commit()

    print('Updated basic!')
    db.session.execute(text('DELETE FROM job_details'))
    send_job_details(detailed_data)
    print('Updated full details!')


# send admits data to the db
def send_admit():

    details =  govt_job_scraper.get_admit()
    for i in details:
        id = i['id']
        title = i['title']
        info = i['data']
        print(title)
        entry = admit_info(counter_id = id, title = title, data=info)
        db.session.execute(text('SET @num :=0; UPDATE admit_info SET sno = @num:= @num+1; ALTER TABLE admit_info AUTO_INCREMENT =1;'))
        db.session.add(entry)
        db.session.commit()

# send results info to the db
def send_result():
    details =  govt_job_scraper.get_result()

    for i in details:
        id = i['id']
        title = i['title']
        info = i['data']
        print(title)
        entry = result_info(counter_id = id, title = title, data=info)
        db.session.execute(text('SET @num :=0; UPDATE result_info SET sno = @num:= @num+1; ALTER TABLE result_info AUTO_INCREMENT =1;'))
        db.session.add(entry)
        db.session.commit()

# pushing to the database
def push_to_db():
    db.session.execute(text('DELETE FROM basic_info'))
    send_jobs()
    db.session.execute(text('DELETE FROM admit_info'))
    send_admit()
    db.session.execute(text('DELETE FROM result_info'))
    send_result()
    return 'data push done'

# notification sending
def notify():
    jobs_data = basic_info.query.order_by(basic_info.date.asc()).all()
    jobs = [[i.title, i.post_name,i.posts,i.link, i.counter_id] for i in jobs_data[:5]]
    print(params['host'])
    user_emails = [i.email for i in user.query.all()]
    subject = params['notification']['subject']
    for email in user_emails:
        print('email',email)
        for i in jobs:
            if 'govtjobguru' in i[3]:
                link= f"{params['host']}/all_jobs/{i[4]}"
            else:
                link = i[3]
            print(link)
            content_str = '''
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Lato|Lato:i,b,bi">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style type="text/css">
        h1 {font-size:56px}
        h2{font-size:28px;font-weight:900}
        p{font-weight:100}
        td{vertical-align:top}
        #email{margin:auto;width:600px;background-color:#fff}
        </style>
    </head>'''+f'''
    <body bgcolor="#F5F8FA" style="width: 100%; font-family:Lato, sans-serif; font-size:18px;">
    <div id="email">
        <table role="presentation" width="100%">
            <tr>
                <td bgcolor="#00A4BD" align="center" style="color: white;">
                    <h1> Welcome!</h1>
                </td>
        </table>
        <table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 30px 30px 30px 60px;">
            <tr>
                <td>
                    <h2>{i[0] }{ i[1]}</h2>
                    <p>
                        {i[0] }{ i[1]}{ i[2] }
                    </p>
                    <a href="{link}">vist</a>
                </td>
            </tr>
        </table>
    </div>
    </body>
    </html>
'''
            content = content_str
            send_mail(email,subject,content)

''' ******** START *********'''

'''  ***** SCHEDULE TASKS START *****'''
def schedule_task():
    push_to_db()
    notify()

# scheduler = BackgroundScheduler(daemon = True)
# scheduler.add_job(schedule_task, 'interval', weeks=1)
# scheduler.start()

'''  ***** SCHEDULE TASKS END *****'''


''' SUPPORTING FUNCTIONS START '''

valid = lambda x: x-1 if x-1 >=0 else 0

''' SUPPORTING FUNCTIONS END '''
# @app.route('/db')
# def something():
#     schedule_task()
#     return "done"



''' MAIN PROGRAM START '''

@app.route('/')
def home():
    genre = basic_info.query.with_entities(basic_info.title).all()
    data_list = [row[0] for row in genre]
    set_data = set()
    for i in data_list:
        set_data.add(i)
    # by post_name
    details = basic_info.query.all()

    toggel=False
    if session.get('user'):
        toggel = True
    else:
        toggel =False

    return render_template('index.html',job_name = set_data, details=details, web_title = Web_Title, toggel=toggel)

'''SHOW STD DETAILS ROUTES START'''

@app.route('/jobs/<job_name>', methods =['GET'])
def job_names(job_name):
    try:
        data = basic_info.query.filter(basic_info.title.contains(job_name) | basic_info.genre.contains(job_name) | basic_info.post_name.contains(job_name)).all()
    except:
        data = []
    return render_template('commonpage.html',data = data, admit = [] ,result = [], total = len(data),  web_title = Web_Title)

@app.route('/all_jobs', methods=['GET','POST'])
def all_jobs():
    data = basic_info.query.order_by(basic_info.date.desc()).all()
    number = len(data)
    toggel=False
    if session.get('user'):
        toggel = True
    else:
        toggel =False

    ''' SEARCH BLOCK '''
    if request.method =='POST':
        job_name = request.form.get('job_name')

        # job results
        try:
            data = basic_info.query.filter(basic_info.title.contains(job_name) | basic_info.genre.contains(job_name) | basic_info.post_name.contains(job_name)).all()
        except:
            data = []

        try:
            admit = admit_info.query.filter(admit_info.title.contains(job_name)).all()
        except:
            admit = []

        try:
            result = result_info.query.filter(result_info.title.contains(job_name)).all()
        except:
            result = []

        number = len(data)+len(result) + len(admit)

        return render_template('commonpage.html',data = data, admit = admit,result = result, total = number,  web_title = Web_Title, toggel=toggel)
    ''' END SEARCH BLOCK '''
    return render_template('commonpage.html',data = data, admit = [] ,result = [], total = len(data),  web_title = Web_Title)

@app.route('/admits')
def admit_data():
    admit = admit_info.query.all()
    toggel=False
    if session.get('user'):
        toggel = True
    else:
        toggel =False
    return render_template('commonpage.html', data =[], admit = admit, result = [],total = len(admit),  web_title = Web_Title, toggel=toggel)

@app.route('/results')
def result_data():
    result = result_info.query.all()
    toggel=False
    if session.get('user'):
        toggel = True
    else:
        toggel =False
    return render_template('commonpage.html', data =[], admit = [], result = result,total = len(result), web_title = Web_Title,toggel=toggel)

'''SHOW STD DETAILS ROUTE END'''


''' FILTER THE SHOWING DATA '''
@app.route('/state/<state_name>')
def state(state_name):
    # job results
        toggel=False
        if session.get('user'):
            toggel = True
        else:
            toggel =False
        try:
            data = basic_info.query.filter(basic_info.title.contains(state_name) | basic_info.genre.contains(state_name) | basic_info.post_name.contains(state_name)).all()
        except:
            data = []

        try:
            admit = admit_info.query.filter(admit_info.title.contains(state_name)).all()
        except:
            admit = []

        try:
            result = result_info.query.filter(result_info.title.contains(state_name)).all()
        except:
            result = []

        number = len(data)+len(result) + len(admit)
        return render_template('commonpage.html',data = data, admit = admit,result = result, total = number, web_title = Web_Title,toggel=toggel)

@app.route('/qualification/<etitle>', methods=["GET"])
def education(etitle):

    try:
        data=basic_info.query.filter(basic_info.qualification.contains(etitle)).all()
    except:
        data=[]
    number=len(data)
    toggel=False
    if session.get('user'):
        toggel = True
    else:
        toggel =False
    return render_template('commonpage.html',data=data,admit=[],result=[],total=number,Web_Title=Web_Title,toggel=toggel)

''' FILTER THE SHOWING DATA END '''

''' SHOW DETAILS ROUTE'''
# jobs
@app.route('/job_details/<u_id>')
def details(u_id):
    data = job_details.query.filter_by(counter_id = u_id).first()

    print(type(u_id),type(data))
    basic = basic_info.query.all()[:10]
    toggel=False
    if session.get('user'):
        toggel = True
    else:
        toggel =False
    return render_template('detailspage.html',data = data, latest=basic, web_title = Web_Title,toggel=toggel)

# admit
@app.route('/admit_details/<a_id>')
def admit_details(a_id):
    data = admit_info.query.filter_by(counter_id = a_id).first()
    toggel=False
    if session.get('user'):
        toggel = True
    else:
        toggel =False
    return render_template('result_admit.html',data = data, web_title = Web_Title,toggel=toggel)

# result
@app.route('/result_details/<r_id>')
def result_details(r_id):
    data = result_info.query.filter_by(counter_id = r_id).first()
    toggel=False
    if session.get('user'):
        toggel = True
    else:
        toggel =False
    return render_template('result_admit.html',data=data, web_title = Web_Title,toggel=toggel)


''' SHOW DETAILS ROUTE END'''

@app.route('/update_db')
def update():
    push_to_db()
    return 'update is done'

""" CONTACT ITEMS """

@app.route('/contact_us', methods=['GET','POST'])
def contact():
    if session.get('user'):

        email = session.get('user')
        if request.method =="POST":
            subject = request.form.get('subject')
            content = request.form.get('message')
            print(email)

            send_mail(owner_gmail,subject,f'{content} \n Sender: {email}')
            flash('We Wil Get Back To You Soon ...')
            time.sleep(1)
            return redirect('/')
        toggel=False
        if session.get('user'):
            toggel = True
        else:
            toggel =False
        return render_template('contact.html', email = email,toggel=toggel)
    else:
        return redirect('/login')
""" CONTACT END """

"""  LOGIN SYSTEM """


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' not in session:
        if request.method == 'POST':
            login_user = request.form.get('u_name')
            log_password = request.form.get('u_pass')

            data_user = user.query.filter(user.email == login_user).first()

            if data_user and log_password == data_user.password:
                # Store user identifier in the session
                session['user'] = data_user.email
                flash('Login successful!', 'success')
                return redirect('/')
            else:
                flash('Invalid credentials. Please try again.', 'danger')

        return render_template('login.html')

    return redirect('/')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if   email != user.query.filter_by(email = email):

            session['name']=name
            session['email'] = email
            session['password'] = password
            session['otp'] = send_otp(email)
            return redirect('/verification')

        elif user.query.filter_by(email=email):
            flash(f'{email} - Already registered')

    return render_template('login.html')

@app.route('/verification')
def verifiy_otp():
    email = session.get('email')

    otp = session.get('otp')
    flash(f'otp has been sent to {email}')

    flash(f'otp is {otp}')

    return render_template('otp.html')

@app.route('/otp_validate',methods = ["POST"])
def otp_validate():
    name = session.get('name')
    password = session.get('password')
    email = session.get('email')
    otp = session.get('otp')
    otp1=request.form.get('otp1')
    otp2=request.form.get('otp2')
    otp3=request.form.get('otp3')
    otp4=request.form.get('otp4')
    verify_otp = otp1 + otp2 + otp3 + otp4
    print(int(verify_otp) is otp)
    if verify_otp == str(otp):
        print('success')
        entry = user(name=name,  email = email, password = password, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        session['user'] = email
        session.pop('name')
        session.pop('email')
        session.pop('password')
        session.pop('otp')
        return redirect('/')
    else:
        flash('Wrong otp...Try Again')
    return redirect('/verification')

@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect('/')
    return redirect('/login')

"""  LOGIN SYSTEM END """

'''  terms AND CONDITIONS  '''

@app.route('/terms')
def terms():
    toggel=False
    if session.get('user'):
        toggel = True
    else:
        toggel =False
    return render_template('terms.html',toggel=toggel)

@app.route('/privacy')
def privacy():
    toggel=False
    if session.get('user'):
        toggel = True
    else:
        toggel =False
    return render_template('privacy.html',toggel=toggel)

''' END terms AND CONDITONS '''

"""  ERROR HANDLEING START  """
@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(501)
@app.errorhandler(503)
def resource_not_found(e):
    return render_template('404.html')

"""  ERROR HANDLEING END  """
if __name__ == '__main__':
    app.run(host="0.0.0.0",port =5000,debug=True)