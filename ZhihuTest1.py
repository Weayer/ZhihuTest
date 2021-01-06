#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/12/25 10:47
# @Author: Weayer
# @File  : ZhihuTest1.py
import requests
import json
import time
import pandas as pd

def get_data(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                          '/57.0.2987.98 Safari/537.36'}
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                             '/57.0.2987.98 Safari/537.36'}
    '''
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()    # 检查请求是否成功
        content = r.content.decode('utf-8')
        return content
    except requests.HTTPError as e:
        print("HTTPError")
    except requests.RequestException as e:
        print('RequestException')
    except:
        print('Unknown Error')

def strFtime(strStamp):     # 时间戳转日期
    timeArray = time.localtime(strStamp)
    str = time.strftime('%Y-%m-%d', timeArray)
    return str

def parse_data(content):    # 获取页面
    data = json.loads(content)
    items = data['data']
    answers = []
    try:
        for item in items:
            if(int(item['voteup_count']) <= 1500):
                continue
            answer = []
            # comment.append(item['question']['title'])
            url = 'https://www.zhihu.com/question/' + str(item['question']['id']) + '/answer/' + str(item['id'])
            answer.append(url)  # 回答链接
            answer.append(item['voteup_count'])  # 点赞数
            answer.append(item['comment_count'])  # 评论数
            create_time = strFtime(item['created_time'])    # 创建时间
            update_time = strFtime(item['updated_time'])    # 更新时间
            answer.append(create_time)
            answer.append(update_time)

            answers.append(answer)
        return answers
    except Exception as e:
        print(e)
        print(answer)


def save_data(answers):    # 保存页面
    filename = 'Data/comments.csv'
    dataframe = pd.DataFrame(answers)
    dataframe.to_csv(filename, mode='a', index=False, sep=',', header=False)
'''
if __name__ == '__main__':
    url = 'https://www.zhihu.com/api/v4/questions/275359100/answers?include=data[*].is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2' \
          'Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2' \
          'Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata[*].mark_infos[*].url%3Bdata[*].author.follower_count%2Cbadge[*].topics%3Bdata[*].settings.table_of_content.enabled&limit=5&offset=5&platform=desktop&sort_by=default'
    content = get_data(url)
    #totals = json.loads(content)['paging']['totals']
    #print(totals)
    answers = parse_data(content)
    save_data(answers)
'''