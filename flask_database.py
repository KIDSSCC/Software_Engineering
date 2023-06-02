from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

class Config:
    SQLALCHEMY_DATABASE_URI='mysql://root:k15648611412@localhost:3306/flaskdb'

app.config.from_object(Config)
app.config['SECRET_KEY'] = b'\xf0?a\x9a\\\xff\xd4;\x0c\xcbHi'
db=SQLAlchemy(app)

class Role(db.Model):
    __tablename__='role'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(32),unique=True)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    passwd=db.Column(db.String(128))
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'))


class Student(db.Model):
    """
    创建学生数据表
    """
    __tablename__ = 'student'
    account=db.Column(db.String(128), primary_key=True)
    passwd = db.Column(db.String(128))
    name = db.Column(db.String(128))








@app.route('/index',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('index.html')
    elif request.method=='POST':
        print('here')
        name=request.form.get('username')
        passwd=request.form.get('password')
        print('name is {}'.format(name))
        print('passwd is {}'.format(passwd))
        with app.app_context():
            new_user=User(name=name,passwd=passwd)
            db.session.add(new_user)
            db.session.commit()
        return 'wait'


@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/register',methods=['GET','POST'])
def register():
    """
    注册页面，学生注册
    :return:
    """
    if request.method=='GET':
        return render_template('register.html')
    elif request.method=='POST':
        account=request.form.get('account')
        passwd=request.form.get('passwd')
        check_passwd=request.form.get('check_passwd')
        if passwd !=check_passwd:
            # todo something
            return redirect(url_for("register"))
        name=request.form.get('name')
        student_n=Student(account=account,passwd=passwd,name=name)
        db.session.add(student_n)
        db.session.commit()
        return 'wait'

@app.route('/login')
def login():
    return 'login page'

if __name__ =='__main__':
    app.run()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # role1=Role(name='admin')
        # role2=Role(name='admin1')
        # db.session.add_all([role1,role2])
        # db.session.commit()
