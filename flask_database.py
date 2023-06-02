from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

class Config:
    SQLALCHEMY_DATABASE_URI='mysql://root:k15648611412@localhost:3306/flaskdb'

app.config.from_object(Config)
app.config['SECRET_KEY'] = b'\xf0?a\x9a\\\xff\xd4;\x0c\xcbHi'
db=SQLAlchemy(app)

# class Role(db.Model):
#     __tablename__='role'
#     id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(32),unique=True)

# class User(db.Model):
#     __tablename__ = 'user'
#     user_type = db.Column(db.Integer, primary_key=True)
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), unique=True)
#     passwd=db.Column(db.String(128))
#     role_id=db.Column(db.Integer,db.ForeignKey('role.id'))


class User(db.Model):
    __tablename__ = 'user'
    user_type = db.Column(db.Integer, primary_key=True)
    account=db.Column(db.String(18),primary_key=True)
    passwd=db.Column(db.String(18))
    name=db.Column(db.String(18))






@app.route('/index',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('index.html')
    elif request.method=='POST':
        u_type=int(request.form.get('type'))
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
        u_type=request.form.get('type')
        account=request.form.get('account')
        passwd=request.form.get('passwd')
        check_passwd=request.form.get('check_passwd')
        name = request.form.get('name')
        # 密码校验
        print(type)
        if passwd !=check_passwd:
            # todo something
            return redirect(url_for("register"))

        user_n=User(user_type=u_type,account=account,passwd=passwd,name=name)
        db.session.add(user_n)
        db.session.commit()
        return redirect(url_for("login"))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        u_type=request.form.get('type')
        account=request.form.get('account')
        passwd=request.form.get('passwd')
        print('the type is {} ,the account is {},the passwd is {}'.format(u_type,account,passwd))
        user=db.session.query(User).filter(User.user_type==u_type,User.account==account).first()
        if user and user.passwd==passwd:
            return '登录成功'
        else:
            return '登录失败'

if __name__ =='__main__':
    app.run()
    with app.app_context():
        if db.engine.has_table('user'):
            print('已经存在')
        else :
            db.drop_all()
            db.create_all()

        # role1=Role(name='admin')
        # role2=Role(name='admin1')
        # db.session.add_all([role1,role2])
        # db.session.commit()
