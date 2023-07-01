import json



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


if __name__ == '__main__':
    json2class()





