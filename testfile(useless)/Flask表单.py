from flask import Flask,render_template
from wtforms import StringField,PasswordField,SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,EqualTo

app=Flask(__name__)

# 定义表单模型类
class Register(FlaskForm):
    user_name=StringField(label='用户名',validators=[DataRequired('用户名不能为空')])
    passwd=PasswordField(label='密码',validators=[DataRequired('密码不能为空')])
    passwd2=PasswordField(label='密码',validators=[DataRequired('密码不能为空'),EqualTo('passwd')])
    submit=SubmitField(label='提交')


@app.route('/register')
def register():
    form =Register()
    return render_template('tmp.html')

if __name__ =='__main__':
    app.run()