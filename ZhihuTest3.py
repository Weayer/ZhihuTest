#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/12/25 20:08
# @Author: Weayer
# @File  : ZhihuTest3.py
import ZhihuTest1
import ZhihuTest2
# topic
topic = [['19768572','考研数学'],
     ['19803441','计算机考研'],
     ['19905290', '考研英语'],
     ['19609318', '考研政治']]
# 19768572 考研数学
# 19803441 计算机考研
# 19905290 考研英语
# 19609318 考研政治
def course(id, name):
    answers = []
    title = "topic:"+name+"，url='https://www.zhihu.com/topic/"+id+"/top-answers',点赞数,评论数,创建时间,更新时间"
    answers.append(title)
    ZhihuTest1.save_data(answers)
    for questions in range(5):
        ZhihuTest2.get_questions(int(id), questions)

if __name__ == '__main__':
    course(topic[0][0], topic[0][1])