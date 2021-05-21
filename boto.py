"""
This is the template server side for ChatBot
"""
import bottle
from bottle import route, run, template, static_file, request,response
import json
import urllib.request
import os
import re
import editdistance,random
import logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='qa.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
app = bottle.app()
class qa_node:
    def __init__(self,q,a,queue):
        self.queue=queue
        self.q=q
        self.a=a
def load_data():
    logging.debug('Loading pairs...')
    lines=open('data/qa1.txt','r').readlines()
    # print(lines[:10])
    logging.debug('Loading pairs done,length:'+str(len(lines)))
    qa_list=[]
    for i,line in enumerate(lines):
        if 'YongYiDaRecord' in line:
            continue
        arrs=line.split('$')
        # print(arrs)
        n=qa_node(arrs[0],arrs[1],i)
        qa_list.append(n)
    return qa_list
def remove_stopwords(test_input):
    pattern='的了吗啊呢吧'
    return re.sub(pattern=pattern,repl='',string=test_input)
def similarity_edit(str1,str2):
    str1=remove_stopwords(str1)
    str2 = remove_stopwords(str2)
    length=len(str1)
    if (len(str1)<len(str2)):
        length = len(str2)
    return editdistance.eval(str1,str2)/length
def get_reply(test_input):
    test_input=remove_stopwords(test_input)
    # arr = string2array(test_input)
    # index = model.predict(arr)
    # value  = index2cata[np.argmax(index[0])]
    qa_list.sort(key=lambda qa: similarity_edit(test_input, qa.q))
    min_qa=qa_list[random.randint(0,10)]
    logging.debug('question:'+test_input+' most similarity Q:'+str(min_qa.q)+' A:'+str(min_qa.a))
    return min_qa.a

qa_list=load_data()
twoWay = {"userNames":[]}
newsConvo = {"engaged":False}
def checkForQuestion(msg):
    # questions = ["what","when","where","why","how","can","may"]
    # if any(word in msg.lower().split() for word in questions):
    #     return {"animation": "no","msg":"Thats a good question!"}
    return {"animation": "no","msg":get_reply(msg)}

def checkMessage(msg):

    question = checkForQuestion(msg)
    if question:return question
    else:
        return {"animation":"inlove","msg":"I didnt understand that, im a pretty dumb boto"}

@route('/', method='GET')
def index():
    return template("index.html")



@route("/chat/<username>", method=['OPTIONS','POST'])
def chat(username):
    postValue = request.POST.decode('utf-8')
    user_message =postValue['msg']
    logging.debug('get new msg:'+user_message)
    return json.dumps(checkMessage(user_message))

@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg') #print this
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')

@route('/cors', method=['OPTIONS', 'GET'])
def lvambience():
    response.headers['Content-type'] = 'application/json'
    return '[1]'
    
@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')

def main():
    
    app.run(host='0.0.0.0', port=8890,server='paste')

if __name__ == '__main__':
    main()
