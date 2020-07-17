#/usr/bin/python
#coding=utf-8
import requests
import re
from lxml import etree
from multiprocessing import Pool
import gitlab

gl = gitlab.Gitlab('http://xxx', private_token='xxx')

def create_session():
    github_username = 'xxx'
    github_password = 'xxx'
    session = requests.session()
    login_page_resp = session.get('http://xxxx/users/sign_in').text
    authenticity_token = re.findall(
        'type="hidden" name="authenticity_token" value="(.*?)" />',
        login_page_resp)[0]
    post_form = {
        'user[remember_me]': '0',
        'utf8': '?',
        'authenticity_token': authenticity_token,
        'user[login]': github_username,
        'user[password]': github_password}
    session.post('xxxx', data=post_form)
    return session

urls =[]
content = create_session()

def getPorject(s):

    url="http://xxxxx/search?utf8=&snippets=&scope=&search=com.alibaba:fastjson&project_id=%s" % s
    pagecontent=content.get(url).text
    pagehtml=etree.HTML(pagecontent)
    projecttitle=pagehtml.xpath("//div[@class='content']/div[@class='row-content-block']/a/@href")
    if len(projecttitle):
        fastjsonver = re.findall("alibaba:fastjson.1.2.(\d+)",pagecontent)
        projects = gl.projects.get(s, all=True)
        if int(fastjsonver[0]) < 69:
            userlist = []
            members = projects.members.list()
            for me in members:
                userlist.append(me.username)
            print("http://xxxx"+str(projecttitle[0])," 1.2."+fastjsonver[0],projects.name,str(userlist).replace(" ", ""))
            return
    else:
        return


if __name__ == '__main__':
    pool = Pool(processes=5)
    file = open('projectid.txt')
    for i in file.readlines():
        #getPorject(i.split()[0])
        pool.apply_async(func=getPorject, args=(i.split()[0],))
    print('end')
    pool.close()
    pool.join()
