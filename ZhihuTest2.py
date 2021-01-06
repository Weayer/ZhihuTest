#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/12/25 19:15
# @Author: Weayer
# @File  : ZhihuTest2.py
import requests
import json
import urllib3
import ZhihuTest1

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# maxnum = 1000
num = 0
question_ids = []

math = ['汤家凤', '张宇', '数学', '李永乐']
cs = ['计算机', '408', '天勤', '王道']
english = ['英语', '语法', '长难句', '阅读', '作文']
polity = ['政治', '肖秀荣', '米神']

def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                      '/57.0.2987.98 Safari/537.36',
    }
    try:
        r = requests.get(url, verify=False, headers=headers)
        content = r.content.decode('utf-8')
        return content
    except requests.exceptions.ConnectionError:
        return False

def get_questions_url(topic_id, page_no):
    limit = 10
    offset = page_no * limit
    url = "https://www.zhihu.com/api/v4/topics/" \
          + str(topic_id) + "/feeds/essence?include=data%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Danswer)%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)%5D.target.data%5B%3F(target.type%3Darticle)%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dtopic_sticky_module)" \
                    "%5D.target.data%5B%3F(target.type%3Dpeople)%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Danswer)%5D.target.annotation_detail%2Ccontent%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F(target.type%3Danswer)%5D.target.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Darticle)%5D.target.annotation_detail%2Ccontent%2Cauthor.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B%3F(target.type%3Dquestion)%5D.target.annotation_detail%2Ccomment_count&limit=" \
          + str(limit) + "&offset=" + str(offset)
    return url

def get_answers_url(question_id, page_no):
    limit = 10
    offset = page_no * limit
    url = 'https://www.zhihu.com/api/v4/questions/' \
          + str(question_id) + '/answers?include=data[*].is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2' \
                       'Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata[*].mark_infos[*].url%3Bdata[*].author.follower_count%2Cbadge[*].topics%3Bdata[*].settings.table_of_content.enabled&' \
            'limit='+ str(limit) +'&offset='+str(offset)+'&platform=desktop&sort_by=default'
    return url

def find(title):
    for i in math:
        if(title.__contains__(i)):
            return True
    return False

def get_article_answer(item):
    global num
    article_title = item['target']['title'] # 判断title是否符合
    #if(find(article_title) == False):
       # return
    article_answer = []
    num  = num + 1
    article_answer.append(str(num)+". Article:{}".format(article_title))
    ZhihuTest1.save_data(article_answer)

    article_answers = []
    article_answer = []
    url = item['target']['url']
    article_answer.append(item['target']['url']) # 回答链接
    article_answer.append(item['target']['voteup_count']) # 点赞数
    article_answer.append(item['target']['comment_count'])# 评论数
    created = ZhihuTest1.strFtime(item['target']['created'])
    updated = ZhihuTest1.strFtime(item['target']['updated'])
    article_answer.append(created)# 创建时间
    article_answer.append(updated)# 更新时间

    article_answers.append(article_answer)
    ZhihuTest1.save_data(article_answers)

def get_question_answer(item):
    global num
    question_id = item["target"]["question"]['id']      # 获取question_id
    question_title = item["target"]["question"]["title"]  # 判断title是否符合
    if (find(question_title) == False):
        return
    if question_id in question_ids:
        return
    if int(item["target"]["voteup_count"]) < 1000:
        return
    # answer = ''.join(pre.findall(item["target"]["content"].replace("\n", "").replace( " " , "")))
    question_ids.append(question_id)  # 记录在questions队列
    answers = []
    num = num + 1
    answers.append(str(num)+". Answers:{}".format(question_title))
    ZhihuTest1.save_data(answers)
    '''
    with open("Data/comments.csv", 'a', encoding='utf-8', newline='') as csvfile:
        w = csv.writer(csvfile)
        w.writerow(comments)
    '''
    # question = item["target"]["question"]["title"].replace("\n", "")
    # 根据question_id继续查找高赞的answers
    for page in range(3):
        url = get_answers_url(question_id, page)
        content = ZhihuTest1.get_data(url)
        answers = ZhihuTest1.parse_data(content)
        ZhihuTest1.save_data(answers)
        # maxnum -= 1
    # content = sline + "\nQ: {}\nA: {}\nvote: {}\n".format(question, answer, vote_num)

def get_questions(topic_id, page_no):
    global  answer_ids, maxnum
    url = get_questions_url(topic_id, page_no)
    content = get_data(url)
    data = json.loads(content)
    items = data["data"]
    if len(items) <= 0:
        return True
    # pre = re.compile(">(.*?)<")
    for item in items:
        # if maxnum <= 0:
           # return True
        if item["target"]["type"] == "article":
            get_article_answer(item)    # 打开article页
        else:
            get_question_answer(item)   # 打开questions页面




