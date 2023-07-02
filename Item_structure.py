import json
import re


class choice_Item():
    def __init__(self,ID,question_stem,optionA,optionB,optionC,optionD,score,answer):
        self.ID=ID
        self.question_stem=question_stem
        self.optionA=optionA
        self.optionB=optionB
        self.optionC=optionC
        self.optionD=optionD
        self.score=score
        self.answer=answer
    def print(self):
        print("ID:", self.ID)
        print("Question Stem:", self.question_stem)
        print("Option A:", self.optionA)
        print("Option B:", self.optionB)
        print("Option C:", self.optionC)
        print("Option D:", self.optionD)
        print("Score:", self.score)
        print("Answer:", self.answer)

class subject_Item():
    def __init__(self,ID,question_stem,score):
        self.ID=ID
        self.question_stem=question_stem
        self.score=score
    def print(self):
        print("ID:", self.ID)
        print("Question Stem:", self.question_stem)
        print("Score:", self.score)


class student_answer_brief:
    def __init__(self,id,name,time,choice_score,subject_score=0,total_score=0):
        self.paper_id=id
        self.name=name
        self.time=time
        self.choice_score=choice_score
        self.subject_score=subject_score
        self.total_score=total_score
    def print(self):
        print("name:",self.name)
        print("time:",self.time)
        print("choice_score",self.choice_score)
        print("subject_score", self.subject_score)
        print("total_score",self.total_score)


class choice_answer():
    def __init__(self,id,ans,stu_ans,score):
        self.id=id
        self.ans=ans
        self.stu_ans=stu_ans
        self.score=score
    def print(self):
        print("id:",self.id)
        print("stu_ans:",self.stu_ans)
        print("ans:", self.ans)
        print("score",self.score)

class subject_answer():
    def __init__(self,id,score,stem,ans,getscore=0):
        self.id=id
        self.score=score
        self.stem=stem
        self.ans=ans
        self.getscore=getscore
    def print(self):
        print("id:",self.id)
        print("score",self.score)
        print("stem",self.stem)
        print("ans",self.ans)
        print("getscore",self.getscore)
        


def json2class(path='teacher_试卷1.json'):
    all_choice = []
    all_subject = []
    with open(path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        for key,value in json_data.items():
            ID = key[3:]
            if key[:3] == '选择题':
                question_stem = value.split("题目:")[1].split("选项:")[0].strip()
                # 提取选项
                options = value.split("选项:")[1].split("分数:")[0].strip().split("~")
                optionA, optionB, optionC, optionD = options
                # 提取分数
                score = int(value.split("分数:")[1].split("答案:")[0].strip())
                # 提取答案
                answer = value.split("答案:")[1].strip()
                # 创建 choice_Item 实例
                item = choice_Item(ID, question_stem, optionA, optionB, optionC, optionD, score, answer)
                all_choice.append(item)
                # item.print()

            elif key[:3] == '主观题':
                question_stem = value.split("主观题描述:")[1].split("分数:")[0].strip()
                score = value.split("分数:")[1].strip()
                item=subject_Item(ID,question_stem,score)
                all_subject.append(item)
                # item.print()
    return all_choice,all_subject

def json2ans(path):
    all_choice=[]
    all_subject=[]
    stu_choicescore=0
    stu_subjectscore=0
    with open(path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        for key,value in json_data.items():
            if key[:3] == '选择题':
                ID = int(re.search(r'\d+', key).group())
                ans = value.split("标准答案:")[1].split("选择答案:")[0].strip()
                stu_ans = value.split("选择答案:")[1].split("分值:")[0].strip()
                score = value.split("分值:")[1].strip()
                item=choice_answer(ID,ans,stu_ans,score)
                all_choice.append(item)
                # item.print()
            elif key[:3] == '客观题':
                stu_choicescore=value
                # print(stu_choicescore)
            elif key[:3] == '主观题':
                # 有两种可能，一种是在教师阅卷时，此时没有主观题得分，另一种是在展示成绩单时，此时有主观题得分
                ID=int(re.search(r'\d+', key).group())
                score = value.split("主观题分数:")[1].split("主观题题干:")[0].strip()
                stem=value.split("主观题题干:")[1].split("主观题答案:")[0].strip()
                ans=value.split("主观题答案:")[1].split("主观题得分:")[0].strip()
                if value.find("主观题得分") == -1:
                    item=subject_answer(ID,score,stem,ans)
                else:
                    getscore=value.split("主观题得分:")[1].strip()
                    item = subject_answer(ID, score, stem, ans,getscore)
                    stu_subjectscore+=int(getscore)
                all_subject.append(item)
                # item.print()
    return all_choice,all_subject,stu_choicescore,stu_subjectscore

def saveSubjectScore(data_dict,path):
    json_data=None
    with open(path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        for key, value in json_data.items():
            if key[:3]=='主观题':
                jsonID = int(re.search(r'\d+', key).group())
                subject_score=data_dict['主观题'+str(jsonID)+'得分']
                json_data[key]=json_data[key]+'主观题得分:'+str(subject_score)+'\n'
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False)




if __name__ == '__main__':
    json2ans('stustudent_试卷1.json')





