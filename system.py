from flask import Flask,render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json

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
# class User(db.Model):
#     __tablename__ = 'user'
#     user_type = db.Column(db.Integer, primary_key=True)
#     account=db.Column(db.String(18),primary_key=True)
#     passwd=db.Column(db.String(18))
#     name=db.Column(db.String(18))
# 数据表的声明
class User_info(db.Model):
    # 用户的个人信息
    __tablename__= 'user_info'
    user_type = db.Column(db.Integer,primary_key=True)
    account = db.Column(db.String(18),primary_key=True,index=True)
    name = db.Column(db.String(18))
    passwd = db.Column(db.String(18))
    email = db.Column(db.String(30))
    tele = db.Column(db.String(18))
    id_no= db.Column(db.String(18))

class Published_paper(db.Model):
    # 所有教师用户已经发布的试卷
    __tablename__ = 'published_paper'
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(18), db.ForeignKey('user_info.account'))
    paper_name=db.Column(db.String(18))
    paper_description=db.Column(db.String(256))
    path=db.Column(db.String(20))
    Answer_num=db.Column(db.Integer)

class ExamList(db.Model):
    # 学生参加考试的情况
    __tablename__ = 'exam_info_list'
    id = db.Column(db.Integer, primary_key=True)
    student=db.Column(db.String(18))
    paper=db.Column(db.Integer)
    choice_score=db.Column(db.Integer)
    subject_score=db.Column(db.Integer)
    total_score=db.Column(db.Integer)


# 全局变量的声明
curr_user=None
paper_name=None
paper_description=None



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
        if passwd !=check_passwd:
            # todo something
            return redirect(url_for("register"))

        user_n=User_info(user_type=u_type,account=account,passwd=passwd,name=name)
        db.session.add(user_n)
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
        user=db.session.query(User_info).filter(User_info.user_type==u_type,User_info.account==account).first()
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

@app.route('/student/agreement')
def agreement():
    return render_template('agreement.html')


@app.route('/student/select',methods=['GET','POST'])
def selectExam():
    if request.method == 'GET':
        results = Published_paper.query.all()
        return render_template('selectExam.html', all_paper=results)
    elif request.method == 'POST':
        account=curr_user.account
        button_id = request.form.get('paper_id')
        # 考试信息表添加新项
        new_record = ExamList(student=account, paper=button_id,choice_score=0,subject_score=0,total_score=0)
        db.session.add(new_record)
        db.session.commit()
        # 更新试卷表中的考试人数
        paper = Published_paper.query.get(button_id)
        paper.Answer_num += 1
        db.session.commit()
        return redirect(url_for('selectExam'))


@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/student/exams')
def stu_exams():
    return render_template('stu_exams.html')

@app.route('/teacher/publish',methods=['GET','POST'])
def tea_publish():
    if request.method == 'GET':
        results = Published_paper.query.all()
        return render_template('tea_publish.html',all_paper=results)
    elif request.method == 'POST':
        if request.form.get('Add')=='添加':
            # 记录下新添加进来的试卷名以及试卷说明
            global paper_name
            global paper_description
            paper_name=request.form.get('试卷名称')
            paper_description=request.form.get('说明')
            return redirect(url_for('publish_new_paper'))
        else:
            return 'other'

@app.route('/teacher/publish/new_paper',methods=['GET','POST'])
def publish_new_paper():
    if request.method == 'GET':
        return render_template('new_paper.html')
    elif request.method == 'POST':
        # 需要保存试卷信息，确定试卷名
        useraccount=curr_user.account
        path=useraccount+'_'+paper_name+'.json'
        data = request.form
        # 将表单数据转换为字典
        data_dict = {}
        for key in data.keys():
            data_dict[key] = data.get(key)

        # 将字典保存为 JSON 文件
        with open(path, 'w',encoding='utf-8') as file:
            json.dump(data_dict, file,ensure_ascii=False)

        # 已经保存了json文件，开始进行数据库的处理
        user_n = Published_paper(account=useraccount, paper_name=paper_name, paper_description=paper_description, path=path,Answer_num=0)
        db.session.add(user_n)
        db.session.commit()

        return 'add paper'


@app.route('/confirm')
def confirm():
    return render_template('confirm.html')

@app.route('/student/take_exams')
def take_exams():
    return render_template('take_exams.html')

if __name__ =='__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()

        # if db.inspect(db.engine).has_table('user_info') and db.inspect(db.engine).has_table('published_paper'):
        #     print('已经存在')
        # else :
        #     db.drop_all()
        #     db.create_all()
    app.run()