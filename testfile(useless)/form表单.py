from flask import Flask,render_template,request
from wtforms import StringField
app=Flask(__name__)

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('index.html')
    elif request.method=='POST':
        name=request.form.get('name')
        passwd=request.form.get('password')
        print('name is {} and passwd is {}'.format(name,passwd))
        return 'this is post'

@app.route('/data')
def getdata():
    datas={
       'mylist':[1,2,3,4,5,6]
    }
    return render_template('totop.html',data=datas)

if __name__ =='__main__':
    app.run()