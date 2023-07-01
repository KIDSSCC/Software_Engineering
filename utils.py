import json

def print_json_content(file_path):

    with open(file_path, 'r',encoding='utf-8') as file:
        json_data = json.load(file)
        print(json.dumps(json_data, indent=4,ensure_ascii=False))

# 指定 JSON 文件的路径
file_path = 'teacher_试卷1.json'

# 调用函数打印 JSON 内容
print_json_content(file_path)
