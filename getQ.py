import requests
import json
from lxml import etree
from getA import getAns


class getQue(object):
    def __init__(self, username, password):
        requests.packages.urllib3.disable_warnings()
        self.examList = []
        self.record_id = []
        self.paper_url = 'str'
        self.anaJson_url = 'str'
        self.quesList=[]
        self.ses = requests.session()
        # 登陆url
        self.login_url = 'https://user.scctedu.com/login'
        # auth验证url
        self.auth_url = 'https://api.scctedu.com/api/authorizations'
        # 课程列表
        self.course_url = 'https://api.scctedu.com/api/student/course/list?learning_status=-1&page=1&limits=10'
        # 练习列表
        self.exer_url = 'https://api.scctedu.com/api/student/course/practice/list?course_id='
        # 考试列表url
        self.ExamList_url = 'https://api.scctedu.com/api/student/paper/list?is_join=all&exam_type=all&exam_name=&limit=10&page=1'
        # 进入练习系统的url
        self.enter_url = 'https://api.scctedu.com/api/student/paper/join?paper_id='
        # 开始练习的url
        self.startPaper_url = 'https://api.scctedu.com/api/student/paper/enter?my_paper_id='
        # 是否继续练习或者考试的url
        self.continueExam_url = 'https://api.scctedu.com/api/student/exam/records?continue=1&id='
        # 查看解析
        self.analy_url = 'https://api.scctedu.com/api/student/paper/analysis?id='
        self.exam_url = 'https://api.scctedu.com/api/student/exam/answer'
        # 登陆用headers
        self.headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Origin':'https://user.scctedu.com',
            'Referer':'https://user.scctedu.com/login'

        }
        # 获取试卷用headers
        self.headers2 = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
            'DNT': '1',
            'Referer': 'https://user.scctedu.com/login',
        }

        self.headers3 = {}
        self.logInfo ={
            "mobile": username,
            "password": password
        }

    # 获取登陆时的token
    def get_token(self):
        token_response = self.ses.get(url=self.login_url,headers=self.headers1,verify=False)
        token_data = token_response.content
        token_xpath = etree.HTML(token_data)
        token = token_xpath.xpath('//meta[@name="csrf-token"]/@content')
        return token

    # 将token放入headers1
    def set_headers1(self):
        token = self.get_token()
        self.headers1['X-CSRF-TOKEN'] = str(token[0])

    def home(self):
        response = self.ses.get(url='https://api.scctedu.com/api/student/center/info',headers=self.headers2,verify=False)
        #print(response.content)

    # 登陆创图教育
    def login(self):

        response = self.ses.post(url=self.login_url, headers=self.headers1, data=self.logInfo,verify=False)
        if response.status_code == 200:
            return True
        else:
            return False

    # 获取local_token
    def get_local_token(self):
        response = self.ses.post(url=self.auth_url, headers=self.headers1, data=self.logInfo,verify=False)
        local_token = response.json()['data']['token']
        #print(local_token)
        return local_token

    def set_headers2(self, local_token):
        self.headers2['Authorization'] = 'Bearer ' + local_token

    # 获取课程的course_id
    def get_courseId(self):
        courseList_response = self.ses.get(url=self.course_url,headers=self.headers2,verify=False)
        courseId = courseList_response.json()['data'][0]['course_id']
        return courseId

    # 获取形式与政策练习的record_id
    def get_recordId(self, courseId):
        self.exer_url = self.exer_url + str(courseId) + '&page=1&limit=10'
        exerList_response = self.ses.get(url=self.exer_url, headers=self.headers2, verify=False)
        #print(exerList_response.status_code)
        # for i in range(examLen-1):
        #     self.examList.append(exerList_response.json()['data'][0]['practice']['my_paper']['exam_records'][i]['id'])
        self.record_id.append(exerList_response.json()['data'][0]['practice']['my_paper']['exam_records'][-1]['id'])
        self.record_id.append(exerList_response.json()['data'][0]['practice']['my_paper']['exam_records'][-2]['id'])

    # 获取继续答题的题目的json网址
    def Con(self):
        con_response = self.ses.get(url=self.continueExam_url+str(self.record_id[0]), headers=self.headers2, verify=False)
        self.paper_url = con_response.json()['data']['mapped_image_file_path']

    # 获取解析的json网址
    def Ana(self):
        #print(self.record_id[-1])
        analy_response = self.ses.get(url=self.analy_url+str(self.record_id[-1]), headers=self.headers2, verify=False)
        #print(analy_response.content)
        self.anaJson_url = analy_response.json()['data']['mapped_image_full_file_path']

    # 设置headres3
    def set_headers3(self):
        self.headers3 = self.headers2
        del self.headers3['Authorization']

    # 获取试卷的json数据
    def get_paperJson(self):
        paper_response = self.ses.get(url=self.paper_url, headers=self.headers3, verify=False)
        paperDict = paper_response.json()
        return paperDict

    # 找出所有的question
    def find(self, paperDict):
        for x in paperDict['questionType']:
            for y in x['question']:
                self.quesList.append(y['question_name'])
        return self.quesList






