import bottle
from bottle import route, run, template, static_file, request,response
import json
import logging
import llm
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='qa.log', level=logging.WARNING, format=LOG_FORMAT, datefmt=DATE_FORMAT)
app = bottle.app()

def get_reply(querys):
    prompts=[]
    if len(querys)>=5*2:
        querys=querys[-5*2:]
    for query in querys:
        if query["role"] == "bot":
            query["role"]="system"
        prompts.append(llm.build_prompt(query["role"],query["content"]))
    text = llm.tokenizer.apply_chat_template(
        prompts,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = llm.tokenizer(text, return_tensors="pt",padding=True).to('cuda')

    from transformers import TextIteratorStreamer
    from threading import Thread

    streamer = TextIteratorStreamer(llm.tokenizer,skip_prompt=True)
    # Run the generation in a separate thread, so that we can fetch the generated text in a non-blocking way.
    generation_kwargs = dict(inputs, streamer=streamer, max_new_tokens=4000,temperature=0.6)
    thread = Thread(target=llm.model.generate, kwargs=generation_kwargs)
    thread.start()
    generated_text = ""
    for new_text in streamer:
        generated_text += new_text
    logging.warning(generated_text)
    return "**以下为思考过程**\n"+generated_text.replace("</think>","**以下为回答内容**\n").replace("<｜end▁of▁sentence｜>","")


def checkForQuestion(msgs):
    return {"code":100,"animation": "no","msg":get_reply(msgs)}

def checkMessage(msgs):
    question = checkForQuestion(msgs)
    if question:return question
    else:
        return {"code":101,"animation":"inlove","msg":"I didnt understand that, im a pretty dumb boto"}

@route('/', method='GET')
def index():
    return template("index.html")



@route("/chat/<username>", method=['OPTIONS','POST'])
def chat(username):
    user_messages =request.json['msg']["messages"] #postValue['msg']
    logging.warning('get new msg:')
    logging.warning(user_messages)
    return json.dumps(checkMessage(user_messages))

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
    
    app.run(host='0.0.0.0', port=8181,server='paste')

if __name__ == '__main__':
    main()
