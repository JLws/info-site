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

Change answer:
```
POST: /api/answer/<answer_id>
```
> **answer** - answer the question

Add page:
```
POST: /api/page
```
> **name** - header the page
> **content** - text the page

Load page:
```
GET: /api/page?pid=1
```
> **qid** - page id

Load pages:
```
GET: /api/page?offset=0&limit=10
```
> **offset** - start loading
> **limit** - number of questions

Change page:
```
POST: /api/page/<page_id>
```
> **name** - header the page
> **content** - text the page

Delete page:
```
DELETE: /api/page/<page_id>
```
