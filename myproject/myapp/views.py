from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
# from . import models
# import random



nextId = 4
topics = [ # 리스트로 묶음
    {'id':1, 'title':'Upload Data', 'body':'분석하고자 하는 데이터를 넣어주세요'},
    {'id':2, 'title':'Result analysis', 'body':'View is ..'},
    {'id':3, 'title':'Accuracy', 'body':'Model is ..'},
]


# Create your views here.
# def index(request):
#     return HttpResponse('<h1>Random</h1>'+str(random.random()))

# 삭제할때 페이지를 한개 더 만들어서 할거면 get 해도되지만 버튼을 눌렀을때 바로 삭제되게 만들때는 
# POST방식을 써야한다. POST 쓸때는 form 을 사용해야한다. delete를 form으로 감싸줘야한다. 
def HTMLTemplate(articleTag, id=None): # 2. 그 인자를 HTMLTemplate 의 첫번째 파라미터(articleTag)가 받는다 # id의 값이 없는 경우에는 None을 해줘야 에러가 안난다.
    global topics
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li>
                <form action ="/delete/" method="post">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li>
            <li><a href="/update/{id}">update</a></li>
            <li><a href = "/create/">create</a></li>
        '''
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
    <html>
    <body>
        <h1><a href = "/">High-risk pregnant woman Classification App</a></h1>
        <ul>
            {ol}
        </ul>
        {articleTag}
        <ul>
            
            {contextUI}
        </ul>
    </body>
    </html>
    '''

def index(request):
    article = '''
    <h2>고위험 임신부 예측을 위한 App입니다</h2>
    test - 설명 추가 예정
    '''
    return HttpResponse(HTMLTemplate(article)) # 1. article을 HTMLTemplate 의 인자로 전달하면     

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article, id)) # 뒤에 id 를 붙여서 처리가능

# input type 에다가 엑셀 데이터 넣을수 있도록 name="title" 해주면 title이라는 이름으로 전송됨
# textarea 는 본문
# 서버로 전송하기 위해 button 필요함 원하는 서버로 전송하기 위해 <form>으로 감싸야한다 보내고 싶은 주소를 action에
# csrf 보안기능 면제하고 싶으면 이렇게 써야함
@csrf_exempt
def create(request):
    global nextId
    # {% csrf_token %} <form method="POST" action="URL" enctype="multipart/form-data">
    if request.method == 'GET':
        article = '''
        <form action="/create/" method="post">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea name="body" placeholder="body"></textarea></p>
            <input type="file" name="file" id="file">
            <button type="submit">결과확인</button>
        </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        newTopic = {"id":nextId, "title":title, "body":body}
        topics.append(newTopic)
        url = '/read/'+str(nextId) # 갱신되기 이전의 값
        nextId = nextId + 1
        return redirect(url)

@csrf_exempt
def update(request, id):
    global topics
    if request.method == 'GET':
        for topic in topics:
            if topic['id'] == int(id):
                selectedTopic = {
                    "title":topic['title'],
                    "body":topic['body']
                }
        article = f'''
        <form action="/update/{id}" method="post">
            <p><input type="text" name="title" placeholder="title" value={selectedTopic["title"]}></p>
            <p><textarea name="body" placeholder="body">{selectedTopic["body"]}</textarea></p>
            <p><input type="submit"></p>
        </form>
        '''
        return HttpResponse(HTMLTemplate(article, id))
    elif request.method == 'POST':
        title = request.POST['title'] # title 간단한 변수로 뽑아냄
        body = request.POST['body']
        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body
        return redirect(f'/read/{id}')

@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id = request.POST['id']
        newTopics = []
        for topic in topics:
            if topic['id'] != int(id):
                newTopics.append(topic)
        topics = newTopics
        return redirect('/') # home 으로 사용자를 보내는것
