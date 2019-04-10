import re
import os
import xlrd


class getAns(object):
    # 提取xls里面的题目和对应的正确答案
    def __init__(self, ):
        self.result = dict()
        self.ansList = []
        self.Ans = {
            "A": 2,
            "B": 3,
            "C": 4,
            "D": 5,
            "E": 6

        }
        myfile = xlrd.open_workbook('exercise.xls')
        lenOfXls = len(myfile.sheets())
        # 存储sheet名字的列表
        sheet_names = myfile.sheet_names()
        # 题库excel文件的类型
        # 3：单 双 判断
        # 2：单 双
        # 1：单 判断
        if len(sheet_names) == 3:
            excel_type = 3
        elif '多选题' in sheet_names:
            excel_type = 2
        else:
            excel_type = 1
        # 读取XLS中的题目和答案，存进字典
        for x in range(0, lenOfXls):
            xls = myfile.sheets()[x]
            for i in range(1, xls.nrows):
                ansstr = ''# 初始化答案字符串
                title = xls.cell(i, 0).value.strip()  # 获取题目
                if x == 1 and lenOfXls == 2:  # 如果存在2个sheets且目前在第二个
                    if excel_type == 2:  # 如果excel文件为单选和多选
                        answer = xls.cell(i, 7).value  # 则现在处在多选题，且答案在第7列
                    else:  # 如果excle文件类型为单选和判断
                        answer = xls.cell(i, 2).value  # 则现在处在判断题，且答案在第2列
                elif x == 1 and lenOfXls == 3:  # 三个都有
                    answer = xls.cell(i, 7).value
                    # answer = answer.replace(',', '')
                    # answer = answer.replace('，', '')
                    # print(answer)
                    list = []
                    for a in answer:

                        ansstr = str(xls.cell(i, self.Ans[a]).value)
                        ansstr = ansstr.replace('.0', '')
                        list.append(ansstr)

                    # print(ansstr)									#多选答案
                elif x == 2 and lenOfXls == 3:
                    list = []
                    list.append(xls.cell(i, 2).value)  # 判断答案
                else:
                    list = []

                    answer = xls.cell(i, 7).value
                    ansstr = str(xls.cell(i, self.Ans[answer]).value)
                    ansstr = ansstr.replace('.0', '')

                    list.append(ansstr)  # 单选答案
                self.result[title] = list

    def answer_func(self, title):
        return self.result.get(title, "Not Found")

    def getAnswer(self, quesList=[]):
        for i in quesList:
            i = i.replace(' ', '')
            #print(i)
            self.ansList.append(self.answer_func(i))
        return self.ansList

    def writeAns(self, ansList=[]):
        i = 1
        with open('answer.txt','w') as f:
            for line in ansList:
                #print(line)
                f.write(str(i) + '==>')
                # 有时line为数字，必须用str()转化类型
                f.write(str(line) + '\n')
                if i % 5 == 0:
                    f.write('\n')
                i = i + 1
            f.close()
        return i-1



