from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

# 全局数据库配置
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


# 数据表声明
class User(db.Model):
    __tablename__ = 'user'
    user_type = db.Column(db.Integer, primary_key=True)
    account=db.Column(db.String(18),primary_key=True)
    passwd=db.Column(db.String(18))
    name=db.Column(db.String(18))

class User_info(db.Model):
    __tablename__= 'user_info'
    user_type = db.Column(db.Integer,primary_key=True)
    account = db.Column(db.String(18),primary_key=True)
    name = db.Column(db.String(18))
    email = db.Column(db.String(18))
    tele = db.Column(db.String(18))
    id_no= db.Column(db.String(18))
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['user_type', 'account'],
            ['user.user_type', 'user.account']
        ),
    )

# 全局变量的声明
curr_user=None



# @app.route('/index',methods=['GET','POST'])
# def index():
#     if request.method=='GET':
#         return render_template('index.html')
#     elif request.method=='POST':
#         u_type=int(request.form.get('type'))
#         name=request.form.get('username')
#         passwd=request.form.get('password')
#         print('name is {}'.format(name))
#         print('passwd is {}'.format(passwd))
#         with app.app_context():
#             new_user=User(name=name,passwd=passwd)
#             db.session.add(new_user)
#             db.session.commit()
#         return 'wait'


@app.route('/')
def home():
    """
    根目录
    :return: 网站主页
    """
    return render_template('homepage.html')

@app.route('/register',methods=['GET','POST'])
def register():
    """
    注册页面，学生注册
    :return:
    """
    if request.method=='GET':
        # 注册页面
        return render_template('register.html')
    elif request.method=='POST':
        # 提交表单之后跳转至登录页面
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
        user_info_new=User_info(user_type=u_type,account=account,name=name)
        db.session.add(user_info_new)
        db.session.commit()

        return redirect(url_for("login"))

@app.route('/login',methods=['GET','POST'])
def login():
    """
    登录页面
    :return:
    """
    if request.method=='GET':
        # 登录页面
        return render_template('login.html')
    elif request.method=='POST':
        # 提交表单之后，跳转到学生主页
        u_type=request.form.get('type')
        account=request.form.get('account')
        passwd=request.form.get('passwd')
        user=db.session.query(User).filter(User.user_type==u_type,User.account==account).first()
        if user and user.passwd==passwd:
            global curr_user
            curr_user = user
            if u_type=='0':
                return redirect(url_for('student_page'))
            elif u_type=='1':
                return redirect(url_for('teacher_page'))


        else:
            return '登录失败'

@app.route('/student',methods=['GET','POST'])
def student_page():
    """
    学生主页
    :return:
    """
    if curr_user is None:
        # 未登录状态
        return 'not login in'
    else:
        # 基本信息查询
        user_info = db.session.query(User_info).filter(
            User_info.user_type == curr_user.user_type,
            User_info.account == curr_user.account
        ).first()
        if request.method=='GET':
                return render_template(
                    'Stu_page.html',
                    username=user_info.name,
                    account = user_info.account,
                    name= user_info.name,
                    email=user_info.email,
                    telephone=user_info.tele,
                    id_no=user_info.id_no
                )
        elif request.method=='POST':
            # 信息的更新
            user_info.email=request.form.get('email')
            user_info.tele=request.form.get('telephone')
            user_info.id_no=request.form.get('id_no')
            db.session.add(user_info)
            db.session.commit()
            return redirect(url_for('student_page'))

@app.route('/teacher',methods=['GET','POST'])
def teacher_page():
    if curr_user is None:
        # 未登录状态
        return 'not login in'
    else:
        # 基本信息查询
        user_info = db.session.query(User_info).filter(
            User_info.user_type == curr_user.user_type,
            User_info.account == curr_user.account
        ).first()
        if request.method == 'GET':
            return render_template(
                'Tea_page.html',
                username=user_info.name,
                account=user_info.account,
                name=user_info.name,
                email=user_info.email,
                telephone=user_info.tele,
                id_no=user_info.id_no
            )
        elif request.method == 'POST':
            # 信息的更新
            user_info.email = request.form.get('email')
            user_info.tele = request.form.get('telephone')
            user_info.id_no = request.form.get('id_no')
            db.session.add(user_info)
            db.session.commit()
            return redirect(url_for('teacher_page'))

@app.route('/agreement')
def agreement():
    return render_template('agreement.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/student/exams')
def stu_exams():
    return render_template('stu_exams.html')

@app.route('/teacher/publish')
def tea_publish():
    return render_template('tea_publish.html')

@app.route('/confirm')
def confirm():
    return render_template('confirm.html')

if __name__ =='__main__':
    with app.app_context():
        # db.drop_all()
        # db.create_all()

        if db.engine.has_table('user'):
            print('已经存在')
        else :
            db.drop_all()
            db.create_all()

        print('here')
        # role1=Role(name='admin')
        # role2=Role(name='admin1')
        # db.session.add_all([role1,role2])
        # db.session.commit()
    app.run()