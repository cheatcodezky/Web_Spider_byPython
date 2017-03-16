# -*- coding:utf-8 -*-
# author :Max

import re
import urllib
import urllib2
import cookielib




# 通过创建Spider类,用Spider类的两个方法来实现爬虫
class Spider:
    filename = 'cookie.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

    def __init__(self, url, account, password, xnd, xqd):
        self.url = url
        self.account = account
        self.password = password
        self.xnd = xnd
        self.xqd = xqd

    def loginWeb(self):
        message = urllib2.urlopen(self.url).read()
        __ViewState = re.findall('<input type="hidden" name="__VIEWSTATE" value="(.*?)" />', message)

        if __ViewState == None:
            print 'no __VIewState'
            return
        headers = {'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1;Miser Report)'}
        data = urllib.urlencode({
            'TextBox1': self.account, 'TextBox2': self.password, 'RadioButtonList1': 'ѧ��', 'Button1': '',
            '__VIEWSTATE': __ViewState[0]})
        request = urllib2.Request(self.url, data, headers)
        try:
            response = Spider.opener.open(request).read().decode('gb2312').encode('utf-8')
            pattern = '<span id="xhxm">.*?  (.*?)同学</span></em>'
            # name = re.findall(pattern, response)
            # return name
        except urllib2.HTTPError, e:
            print 'HTTPError = ' + e.code
            return 'Error'

    def timeTable(self):
        referer = 'http://jwxt.jiangnan.edu.cn/jndx/xs_main.aspx?xh=' + self.account

        url = 'http://jwxt.jiangnan.edu.cn/jndx/xskbcx.aspx?xh=' + self.account + '&xm=%D6%DC%BF%C6%D3%F0&gnmkdm=N121603'

        headers = {'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1;Miser Report)', 'Referer': referer}
        request_test = urllib2.Request(url, headers=headers)
        message = Spider.opener.open(request_test).read().decode('gb2312', 'ignore').encode('utf-8')

        __ViewState = re.findall('<input type="hidden" name="__VIEWSTATE" value="(.*?)" />', message)
        # print __ViewState[0]
        # data = urllib.urlencode({'__EVENTTARGET':'xqd','__EVENTARGUMENT':'','__VIEWSTATE':__ViewState[0],
        #      'xnd':self.xnd,'xqd':self.xqd})
        #
        #
        # request = urllib2.Request(url,data,headers)
        # response = Spider.opener.open(request).read().decode('gb2312','ignore').encode('utf-8')
        # print response
        lesson_message = []
        lesson_table = []*12

        for i in range(1,13):
            pattern = '第'+str(i)+'节(.*?)<td class="noprint" align="Center"'
            answer = re.findall(pattern,message)
            lesson_message.append(answer[0])
        
        lesson_classroom = []
        lesson_teacher = []
        lesson_time = []
        lesson_start = []
        lesson_name = []
        lesson_week = []
        for i in range(0,12):
            pattern = '<td align="Center".*?>(.*?)</td>'
            lessons = re.findall(pattern,lesson_message[i])
            week = 0
            for lesson in lessons:
                week = week + 1

                information = lesson.split('<br>')
                if len(lesson) <30:
                    lesson_start.append(i + 1)
                    lesson_name.append('null')
                    lesson_time.append('null')
                    lesson_classroom.append('null')
                    lesson_teacher.append('null')
                    lesson_week.append(week)
                    continue
                if information.__len__() > 7:
                    # 上课的名字、时间、教室分别储存在三个列表中
                    lesson_name.append(information[0])
                    lesson_time.append(information[2])
                    lesson_classroom.append(information[4])
                    lesson_teacher.append(information[3])
                    lesson_name.append(information[6])
                    lesson_time.append(information[8])
                    lesson_teacher.append(information[9])
                    lesson_classroom.append(information[10])
                    lesson_start.append(i+1)
                    lesson_start.append(i + 1)
                    lesson_week.append(week)
                    lesson_week.append(week)
                else:
                    lesson_name.append(information[0])
                    lesson_time.append(information[2])
                    lesson_classroom.append(information[4])
                    lesson_teacher.append(information[3])
                    lesson_start.append(i+1)
                    lesson_week.append(week)
        #返回的课程信息储存到数组
        lesson_WeekLength = []
        lesson_length = []
        lesson_Week_Odd_Even = []# Odd_Week or Even Week
        for i in lesson_time:
            print i
            if i == 'null':
                lesson_WeekLength.append([0,0])
                lesson_Week_Odd_Even.append(0)
                lesson_length.append(0)
            else:
                pattern = '第(\d+-\d+)周'
                answer = re.findall(pattern,i)
                print answer
                information = answer[0].split('-')
                lesson_WeekLength.append([information[0],information[1]])
                pattern = '\|(单|双)周'
                answer = re.search(pattern,i)
                if answer == None:
                    lesson_Week_Odd_Even.append(0)
                else:
                    if answer.group(1)=='单':
                        lesson_Week_Odd_Even.append(1)
                    elif answer.group(1) =='双':
                        lesson_Week_Odd_Even.append(2)
                pattern = '(\d*,?\d*,?\d*,?\d+)节'
                answer = re.findall(pattern,i)
                lesson_length_deal = len(answer[0].split(','))
                if lesson_length_deal > 1:
                    lesson_length.append(lesson_length_deal)
                else:
                    lesson_length.append(answer[0])
        return lesson_name,lesson_time,lesson_classroom,lesson_teacher,lesson_start,lesson_week,lesson_length,lesson_WeekLength,lesson_Week_Odd_Even
if __name__ == "__main__":
    print 'try spider'
    url = 'http://jwxt.jiangnan.edu.cn/jndx/default5.aspx'
    account = ''  # 学号
    password = ''  # 密码
    xnd = '2016-2017'  # 学年
    xqd = '2'  # 学期
    spider = Spider(url, account, password, xnd, xqd)
    name = spider.loginWeb()
    if name == 'Error':
        print 'Web Login Failed'
    else:
        print 'code right'
        spider.timeTable()
print 'run over'

