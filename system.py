from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json
from Item_structure import *

app = Flask(__name__)


# 全局数据库配置
class Config:
    SQLALCHEMY_DATABASE_URI='mysql://root:k15648611412@localhost:3306/flaskdb'

app.config.from_object(Config)
app.config['SECRET_KEY'] = b'\xf0?a\x9a\\\xff\xd4;\x0c\xcbHi'
db = SQLAlchemy(app)


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
    time=db.Column(db.Integer)

class ExamList(db.Model):
    # 学生参加考试的情况
    __tablename__ = 'exam_info_list'
    id = db.Column(db.Integer, primary_key=True)
    student=db.Column(db.String(18))
    paper=db.Column(db.Integer)
    choice_score=db.Column(db.Integer)
    subject_score=db.Column(db.Integer)
    total_score=db.Column(db.Integer)
    submission_time=db.Column(db.String(25))

# 全局变量的声明
curr_user = None
paper_name = None
paper_description = None
exam_time = None
curr_choice_score = None

paper_for_student = None
curr_mark_paper=None


all_choice = []
all_subject = []
exam_limit_time = None
stu_ans ={}
stu_choicescore = 0


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
            elif u_type=='2':
                return redirect(url_for('admin_page'))


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


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    """
    管理员主页
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
        if request.method == 'GET':
            return render_template(
                'Adm_page.html',
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
            return redirect(url_for('admin_page'))


@app.route('/student/agreement')
def agreement():
    return render_template('agreement.html')


@app.route('/student/select', methods=['GET', 'POST'])
def selectExam():
    if request.method == 'GET':
        results = Published_paper.query.all()
        return render_template('selectExam.html', all_paper=results)
    elif request.method == 'POST':
        account = curr_user.account
        button_id = request.form.get('paper_id')
        # 考试信息表添加新项
        new_record = ExamList(student=account, paper=button_id, choice_score=0, subject_score=0, total_score=0)
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
    # 学生选择进行考试
    uncompleted_exam = ExamList.query.filter(ExamList.student == curr_user.account, ExamList.choice_score == 0).all()
    completed_exam = ExamList.query.filter(ExamList.student == curr_user.account, ExamList.choice_score != 0).all()
    uncompleted = []
    completed = []
    for item in uncompleted_exam:
        uncompleted.append(Published_paper.query.filter(Published_paper.id == item.paper).first())
    for item in completed_exam:
        completed.append(Published_paper.query.filter(Published_paper.id == item.paper).first())
    return render_template('stu_exams.html', completed_exam=completed, uncompleted_exam=uncompleted)


@app.route('/teacher/publish', methods=['GET', 'POST'])
def tea_publish():
    if request.method == 'GET':
        results = Published_paper.query.all()
        return render_template('tea_publish.html', all_paper=results)
    elif request.method == 'POST':
        if request.form.get('Add') == '添加':
            # 记录下新添加进来的试卷名以及试卷说明
            global paper_name
            global paper_description
            global exam_time
            paper_name = request.form.get('试卷名称')
            paper_description = request.form.get('说明')
            exam_time = request.form.get('考试时间')
            return redirect(url_for('publish_new_paper'))
        else:
            return 'other'


@app.route('/teacher/publish/new_paper', methods=['GET', 'POST'])
def publish_new_paper():
    if request.method == 'GET':
        return render_template('new_paper.html')
    elif request.method == 'POST':
        # 需要保存试卷信息，确定试卷名
        useraccount = curr_user.account
        path = useraccount + '_' + paper_name + '.json'
        data = request.form
        # 将表单数据转换为字典
        data_dict = {}
        for key in data.keys():
            data_dict[key] = data.get(key)

        # 将字典保存为 JSON 文件
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data_dict, file, ensure_ascii=False)

        # 已经保存了json文件，开始进行数据库的处理
        user_n = Published_paper(account=useraccount, paper_name=paper_name, paper_description=paper_description,
                                 time=exam_time, path=path, Answer_num=0)
        db.session.add(user_n)
        db.session.commit()

        return 'add paper'


@app.route('/confirm')
def confirm():
    return render_template('confirm.html')


@app.route('/student/take_exams', methods=['GET', 'POST'])
def take_exams():
    # 根据post请求中提供的试卷id展示对应的试卷
    if request.method == 'POST':
        data = request.form.get('试卷id')
        # 先根据id在publish_paper表中查找对应的试卷表项，获取文件路径
        global paper_for_student
        paper_for_student = Published_paper.query.filter_by(id=data).first()

        global all_choice, all_subject
        all_choice, all_subject = json2class(paper_for_student.path)
        # 向页面中传递信息，包括选择题，主观题，与考试时间
        return '/student/take_exams'
        # return render_template('take_exams.html',all_choice=all_choice,all_subject=all_subject,time=paper.time)
    elif request.method == 'GET':
        return render_template('take_exams.html', all_choice=all_choice, all_subject=all_subject,
                               time=str(paper_for_student.time))


@app.route('/student/take_exams/settle', methods=['POST'])
def settleAccount():
    useraccount = curr_user.account
    path = 'stu' + useraccount + '_' + paper_for_student.paper_name + '.json'
    data = request.form
    data_dict = {}
    global stu_ans

    for key in data.keys():
        data_dict[key] = data.get(key)
        if key[:3]=='选择题':
            ID = data[key].split("选择题编号:")[1].split("标准答案:")[0].strip()
            # stuchoice = data[key].split("选择答案:")[1].strip()
            stuchoice = data[key].split("选择答案:")[1].split("分值:")[0].strip()
            stu_ans[ID]=stuchoice

    #print(stuans)

    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data_dict, file, ensure_ascii=False)

    global stu_choicescore
    stu_choicescore = int(data.get('客观题总分'))
    # 进行数据库的处理，更新自动阅卷分数
    entry = ExamList.query.filter_by(student=curr_user.account, paper=paper_for_student.id).first()
    entry.choice_score = int(data.get('客观题总分'))
    entry.submission_time=data.get('提交时间')
    db.session.commit()

    return 'here'


@app.route('/student/take_exams/report',methods=['GET'])
def report_card():
    return render_template('show_choicescore.html',all_choice=all_choice,stu_ans=stu_ans,stu_choicescore=stu_choicescore)

@app.route('/changepwd', methods=['GET', 'POST'])
def change_pwd():
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
            u_type = user_info.user_type
            if u_type == 0:
                return render_template('stu_changepwd.html', username=user_info.name)
            elif u_type == 1:
                return render_template('tea_changepwd.html', username=user_info.name)
            elif u_type == 2:
                return render_template('adm_changepwd.html', username=user_info.name)
            return "人员类型不存在！"
        elif request.method == 'POST':
            # 信息的更新
            dbpwd = user_info.passwd
            oldpwd = request.form.get('oldpwd')
            newpwd = request.form.get('newpwd')
            newpwd1 = request.form.get('newpwd1')

            if dbpwd != oldpwd:
                return "原密码错误"
            elif newpwd == oldpwd:
                return "新密码不可与原密码一致"
            elif newpwd != newpwd1:
                return "两次输入的新密码不一致"
            else:
                user_info.passwd = newpwd
                db.session.commit()
                return redirect(url_for('change_pwd'))


@app.route('/forgetpwd', methods=['GET', 'POST'])
def forgetpwd():
    if request.method == 'GET':
        # 注册页面
        return render_template('forgetpwd.html')
    elif request.method == 'POST':
        # 提交表单之后，跳转到学生主页
        u_type = request.form.get('type')
        account = request.form.get('account')
        email = request.form.get("email")
        user = db.session.query(User_info).filter(User_info.user_type == u_type, User_info.account == account).first()
        if user and user.email == email:
            global curr_user
            curr_user = user
            if u_type == '0':
                return redirect(url_for('student_page'))
            elif u_type == '1':
                return redirect(url_for('teacher_page'))
            elif u_type == '2':
                return redirect(url_for('admin_page'))
        else:
            return '邮箱验证错误'


@app.route('/admin/user_management', methods=['GET', 'POST'])
def adm_usermanagement():
    if request.method == 'GET':
        results = User_info.query.all()
        return render_template('adm_usermanage.html', all_user=results)
    elif request.method == 'POST':
        if request.form.get('Add') == '添加':
            type = request.form.get('用户类型')
            account = request.form.get('用户id')
            name = request.form.get('用户名')
            pwd = request.form.get('密码')
            email = request.form.get('邮箱')
            tele = request.form.get('电话号')
            sfzh = request.form.get('身份证号')
            user_n = User_info(user_type=type, account=account, name=name, passwd=pwd, email=email, tele=tele,
                               id_no=sfzh)
            db.session.add(user_n)
            db.session.commit()
            return redirect(url_for('adm_usermanagement'))
        elif request.form.get('Update') == '更新':
            type = request.form.get('用户类型')
            account = request.form.get('用户id')
            user_info = db.session.query(User_info).filter(
                User_info.user_type == type,
                User_info.account == account
            ).first()

            user_info.name = request.form.get('用户名')
            user_info.passwd = request.form.get('密码')
            user_info.email = request.form.get('邮箱')
            user_info.tele = request.form.get('电话号')
            user_info.id_no = request.form.get('身份证号')

            db.session.commit()

            return redirect(url_for('adm_usermanagement'))
        elif request.form.get('delete') == '删除':
            type = request.form.get('用户类型')
            account = request.form.get('用户id')
            user_info = db.session.query(User_info).filter(
                User_info.user_type == type,
                User_info.account == account
            ).first()
            db.session.delete(user_info)
            db.session.commit()

            return redirect(url_for('adm_usermanagement'))
        else:
            return 'other'


@app.route('/admin/exam_management', methods=['GET', 'POST'])
def adm_exammanagement():
    if request.method == 'GET':
        results = Published_paper.query.all()
        return render_template('adm_exammanage.html', all_exam=results)
    elif request.method == 'POST':
        if request.form.get('Add') == '添加':
            id = request.form.get('试卷id')
            account = request.form.get('发布教师id')
            name = request.form.get('试卷名称')
            desc = request.form.get('试卷描述')
            path = request.form.get('试卷路径')
            num = request.form.get('考生人数')

            paper = Published_paper(id=id, account=account, paper_name=name, paper_description=desc, path=path,
                                    Answer_num=num)
            db.session.add(paper)
            db.session.commit()
            return redirect(url_for('adm_exammanagement'))

        elif request.form.get('Update') == '更新':
            id = request.form.get('试卷id')
            exam_info = db.session.query(Published_paper).filter(
                Published_paper.id == id
            ).first()
            exam_info.account = request.form.get('发布教师id')
            exam_info.paper_name = request.form.get('试卷名称')
            exam_info.paper_description = request.form.get('试卷描述')
            exam_info.path = request.form.get('试卷路径')
            exam_info.Answer_num = request.form.get('考生人数')

            db.session.commit()

            return redirect(url_for('adm_exammanagement'))
        elif request.form.get('delete') == '删除':
            id = request.form.get('试卷id')
            exam_info = db.session.query(Published_paper).filter(
                Published_paper.id == id
            ).first()

            db.session.delete(exam_info)
            db.session.commit()

            return redirect(url_for('adm_exammanagement'))
        else:
            return 'other'

@app.route('/teacher/select_to_mark')
def select_to_mark():
    # 需要查询当前教师所发布的所有试卷
    entries = Published_paper.query.filter_by(account=curr_user.account).all()
    return render_template('select_to_mark.html',all_paper=entries)

@app.route('/teacher/select_student',methods=['POST'])
def select_student():
    # 根据试卷ID查询哪些学生报名了考试，
    data=request.form.get('试卷ID')
    # 所有已经答题的学生和报名之后未答题的学生
    already_answer=ExamList.query.filter(ExamList.paper == data,ExamList.choice_score != 0).all()
    not_answer=ExamList.query.filter(ExamList.paper == data,ExamList.choice_score == 0).all()
    # 对于所有已经答题的学生，分为已阅卷和未阅卷
    answer_stu=[]
    not_answer_stu=[]
    for item in already_answer:
        name=User_info.query.filter(User_info.user_type==0,User_info.account==item.student).first().name
        answer_stu.append(student_answer_brief(data,name,item.submission_time,item.choice_score,item.subject_score,item.total_score))
    for item in not_answer:
        name=User_info.query.filter(User_info.user_type==0,User_info.account==item.student).first().name
        not_answer_stu.append(name)
    return render_template('select_student.html',already_answer=answer_stu,not_answer=not_answer_stu)

@app.route('/teacher/mark_paper',methods=['POST'])
def mark_paper():
    if request.form.get('主观题总分') is None:
        # 是选择了学生进入当前的页面，提供学生的试卷供教师进行评阅
        global curr_mark_paper
        curr_mark_paper=request.form
        # 根据试卷ID查一下试卷名，以确定最终的路径
        paper_id=curr_mark_paper.get('试卷ID')
        exam_name=Published_paper.query.filter(Published_paper.id==paper_id).first().paper_name
        # 需要根据学生姓名查一下学生账号
        name=curr_mark_paper.get('学生姓名')
        account=User_info.query.filter(User_info.name==name).first().account
        # 形成最终的路径
        path='stu'+account+'_'+exam_name+'.json'

        choice,subject,choicescore,_=json2ans(path)
        return render_template('mark_paper.html',all_choice=choice,all_subject=subject,choicescore=choicescore)
    else:
        # 教师提交了评阅结果
        print(request.form.get('主观题总分'))
        paper_id=curr_mark_paper.get('试卷ID')
        name = curr_mark_paper.get('学生姓名')
        account = User_info.query.filter(User_info.name == name).first().account
        target_entry=ExamList.query.filter(ExamList.student==account,ExamList.paper==paper_id).first()
        target_entry.subject_score=int(request.form.get('主观题总分'))
        target_entry.total_score=target_entry.choice_score+target_entry.subject_score
        db.session.commit()
        # 更新json数据：存储键值对：每一道主观题：主观题对应的得分
        data_dict=dict()
        for key,value in request.form.items():
            if key !='主观题总分':
                data_dict[key]=value
        exam_name=Published_paper.query.filter(Published_paper.id==paper_id).first().paper_name
        path='stu'+account+'_'+exam_name+'.json'
        saveSubjectScore(data_dict,path)
        return 'here'

@app.route('/student/scores')
def stu_scores():
    # 学生选择进行考试
    completed_exam = ExamList.query.filter(ExamList.student == curr_user.account, ExamList.choice_score != 0).all()
    completed = []
    for item in completed_exam:
        completed.append(Published_paper.query.filter(Published_paper.id == item.paper).first())
    return render_template('stu_scores.html', completed_exam=completed)


all_choice_for_list=None
all_subject_for_list=None
total_choice_score=0
total_subject_score=0
@app.route('/student/getscorelist',methods=['GET', 'POST'])
def stu_getscorelist():

    if request.method=='POST':
        examname=request.form.get('试卷名')
        #print(examname)
        useraccount = curr_user.account
        path = 'stu' + useraccount + '_' + examname + '.json'
        #print(path)
        # all_choice1, all_subject1,choice_score= json2ans(path)
        global all_choice_for_list,all_subject_for_list,total_choice_score,total_subject_score
        all_choice_for_list,all_subject_for_list,total_choice_score,total_subject_score=json2ans(path)
        for item in all_choice_for_list:
            item.print()
        return 'here'
        # return render_template('show_allscore.html',all_choice1=all_choice_for_list)

    elif request.method=='GET':
        return render_template('show_allscore.html',all_choice1=all_choice_for_list,total_choice_score=int(total_choice_score),all_subject_for_list=all_subject_for_list,total_subject_score=total_subject_score)


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run()