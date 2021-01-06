
**算法实现**

```
核心代码有三个文件：
ZhihuTest1: 访问question页面，获取高赞answer，保存结果
ZhihuTest2: 访问topic页面，获取questions_url，
            如果为article，保存结果；
            如果为question，进入ZhihuTest1
ZhihuTest3: 主程序，进入ZhihuTest2，记录了有4个考研相关topic供选 
爬取的数据保存到comments.csv中
```
另提供.csv文件在线转markdown表格的宝藏网站：<a href="http://web.chacuo.net/charsettextmarkdown" target="_blank"></a>http://web.chacuo.net/charsettextmarkdown

**代码运行说明**

1. 目前ZhihuTest3.py提供的爬取的topic有如下几个：
```
topic = [['19768572','考研数学'],
     ['19803441','计算机考研'],
     ['19905290', '考研英语'],
     ['19609318', '考研政治']]
```

2. 若想爬取例如`计算机考研`的高赞回答，除了修改main函数中的形参为`topic[1][0], topic[1][1]`，还需修改的有：
- Zhihu2.py的find()方法中，将`math`改为`cs`
- 将之前爬取的comments.csv内容删去，因为写文件`DataFrame.to_csv()`的mode参数是a，在结尾添加

3. 另外关于点赞数的筛选在Zhihu1.py的`parse_data()`方法中，我筛选的是点赞数大于1500的回答
   一次获取的页面内容可在Zhihu2.py的`get_questions_url()`和`get_answers_url()`方法中自行修改，我选择的每次获取10篇回答，10个问题
   同样爬取的总篇幅数也可在Zhihu2.py的`get_question_answer()`以及Zhihu3.py的`course()`进行更改

