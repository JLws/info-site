# info-site

Start server:

```
cd backend
pip install requirements.txt
gunicorn -w 1 -b localhost:3000 server:app --worker-class gevent
```
Deploy the database **dump.sql** and configure *backend/config.py* DATABASE_URI.
# Requests

Load items of menu:
```
GET: /api/menu
```

Load question:
```
GET: /api/question?qid=1
```
> **qid** - question id

Load questions:
```
GET: /api/question?offset=0&limit=10
```
> **offset** - start loading
> **limit** - number of questions

Delete question:
```
DELETE: /api/question/<question_id>
```

Add question:
```
POST: /api/question
```
> **name** - username
> **email** - user email
> **question** - question text

Add answer:
```  
POST: /api/answer
```
> **question_id** - question id
> **name** - username
> **answer** - answer the question

Delete answer:
```
DELETE: /api/answer/<answer_id>
```
