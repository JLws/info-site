from helper.request import Request as RequestClass
from db.database import Database
from db.models.Page import Page
from flask import jsonify, request
from datetime import datetime

class ExecutePage(RequestClass):

    def load_page(self): # GET
        try: # load one page
            page = Database.CONFIG['session'].query(Page).get(int(request.args.get('pid')))
            return_data = {
                'name': page.name,
                'username': page.username,
                'date': page.date,
                'content': page.content,
                'image': page.image
            }

            return jsonify({ 'payload': return_data })

        except: # load all page
            offset = request.args.get('offset') if request.args.get('offset') else 0
            limit = request.args.get('limit') if request.args.get('limit') else 10
            query = Database.CONFIG['session'].query(Page).offset(offset).limit(limit)
            result = Database.CONFIG['session'].execute(query)
            return_data = []
            for item in result.fetchall():
                return_data.append({
                'name': item.posts_name,
                'username': item.posts_username,
                'date': item.posts_date,
                'content': item.posts_content,
                'image': item.posts_image
                })

            return jsonify({ 'gallery': return_data})

    def add_page(self): # POST
        fields = {'name': '', 'image': '', 'username': '', 'content': ''}
        try:
            self.Parameters(fields, request.form) # parse parameters
            new_page = Page(name=fields['name'], image=fields['image'], username=fields['username'], content=fields['content'], date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            Database.CONFIG['session'].add(new_page)
            Database.CONFIG['session'].commit()
            return jsonify({ 'result': True })

        except Exception as e:
            return jsonify({ 'result': False, 'error': str(e) })

    def delete_page(self, page_id): # DELETE
        try:
            page = Database.CONFIG['session'].query(Page).get(int(page_id))
            Database.CONFIG['session'].delete(page)
            Database.CONFIG['session'].commit()
            return jsonify({ 'result': True })

        except Exception as e:
            return jsonify({ 'result': False, 'error': str(e) })

    def edit_page(self, page_id): # POST
        fields = { 'image': '', 'name': '', 'content': '' }
        try:
            self.Parameters(fields, request.form, miss=True) # parse parameters
            page = Database.CONFIG['session'].query(Page).get(int(page_id))
            page.image = fields['image'] if fields['image'] else page.image
            page.name = fields['name'] if fields['name'] else page.name
            page.content = fields['content'] if fields['content'] else page.content
            Database.CONFIG['session'].commit()
            return jsonify({ 'result': True })

        except Exception as e:
            return jsonify({ 'result': False, 'error': str(e) })