from getQ import getQue
from getA import getAns
import json


def get_queIdList(paperDict):
    queIdList = []
    for x in paperDict['questionType']:
        for y in x['question']:
            queIdList.append(y['id'])
    return queIdList

def get_ansIdlist(paperDict, ansList):
    ansIdList = []
    i = 0
    for x in paperDict['questionType']:
        for y in x['question']:
            ansIdList2 = []
            for z in y['answer']:
                a = str(z['answer_option'])
                if a in ansList[i]:
                    ansIdList2.append(z['id'])
                if x['question_type_name'] != '多选题':
                    continue
            ansIdList.append(ansIdList2)
            i = i + 1
    return ansIdList

getque = getQue('10359#2015212182', '2015212182')

getque.set_headers1()
if getque.login():
    local_token = getque.get_local_token()
    getque.set_headers2(local_token)
    course_Id = getque.get_courseId()
    getque.get_recordId(course_Id)
    getque.Con()

    getque.set_headers3()
    paperDict = getque.get_paperJson()
    quesList = getque.find(paperDict)
    with open('quetions.txt', 'w', encoding='utf-8') as qu:
        i = 1
        for line in quesList:
            qu.write(str(i) + '==>')
            # 有时line为数字，必须用str()转化类型
            qu.write(str(line))
            qu.write('\n')
            if i % 5 == 0:
                qu.write('\n')
            i = i + 1
    getans = getAns()
    ansList = getans.getAnswer(quesList=quesList)
    j = getans.writeAns(ansList)

    # queIdList = get_queIdList(paperDict)
    # ansIdList = get_ansIdlist(paperDict, ansList)
    # #print(ansList)
    # #print(queIdList)
    # dataList = []
    # record_id = getque.record_id[0]
    # answer = {
    #     "id": record_id,
    #     "question_id": 2,
    #     "answer": [1]
    # }
    # url = 'https://api.scctedu.com/api/student/exam/answer'
    # for o in range(len(queIdList)):
    #     #print(o)
    #     answer["question_id"] = queIdList[o]
    #     answer["answer"] = ansIdList[o]
    #


    # print(dataList)
    # print(len(dataList))

