from helper.request import Request as RequestClass
from db.database import Database
import sqlalchemy as db
from flask import jsonify

class ExecuteMenu(RequestClass):

    def load_menu(self): # GET
        menu = db.Table('menu', db.MetaData(), autoload=True, autoload_with=Database.CONFIG['engine'])
        query = db.select([menu])
        result = Database.CONFIG['connect'].execute(query)
        menudata = []
        for item in result.fetchall():
            item_id, item_name, item_parent, item_url = item
            if len(menudata) == 0:
                if item_parent == None:
                    menudata.append({'id': item_id, 'name': item_name, 'url': item_url, 'child': [] })

                else:
                    menudata.append({'id': item_parent, 'name': '', 'url': '', 'child': [{'name': item_name, 'url': item_url}] })
                
                continue

            for item_menu in menudata:
                if item_parent == None: # add parebt
                    if item_menu['id'] == item_id:
                        item_menu['name'] = item_name
                        item_menu['url'] = item_url

                else: # add child
                    if item_menu['id'] == item_parent:
                        item_menu['child'].append({'name': item_name, 'url': item_url})
                        break

            else: # not found parent
                if item_parent == None: # add parent
                    menudata.append({'id': item_id, 'name': item_name, 'url': item_url, 'child': [] })

                else: # add child
                    menudata.append({'id': item_parent, 'name': '', 'url': '', 'child': [{'name': item_name, 'url': item_url}] })

        return jsonify({ 'payload': menudata })