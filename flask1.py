# from flask import Flask
# from werkzeug.routing import BaseConverter
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
#
# @app.route('/hi',methods=['GET','POST'],endpoint='hi')
# def hi():
#     return 'hihihihi'
#
# @app.route('/user/<id>')
# def index(id):
#     if int(id)==1:
#         return 'this is case 1'
#     if int(id)==2:
#         return 'this is case 2 '
#
# # 转换器
# @app.route('/transform/<string:id>')
# def transform(id):
#     if(id =='1'):
#         return 'hello'
#
# class MyConvert(BaseConverter):
#     def __init__(self,url_map,regex):
#         super(MyConvert, self).__init__(url_map)
#         self.regex=regex
#
# app.url_map.converters['re']=MyConvert
# @app.route('/myconvert/<re("123"):value>')
# def myconv(value):
#     return 'my own convert'
#
#
# if __name__ == '__main__':
#     app.run()




