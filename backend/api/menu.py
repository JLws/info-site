from helper.request import Request as RequestClass
from db.database import Database
from db.models.Menu import Item
from flask import jsonify

class ExecuteMenu(RequestClass):

    def load_menu(self): # GET
        menudata = []
        for item in Database.CONFIG['session'].query(Item).all():
            if len(menudata) == 0:
                if item.parent == None:
                    menudata.append({'id': item.id, 'name': item.name, 'url': item.url, 'child': [] })

                else:
                    menudata.append({'id': item.parent, 'name': '', 'url': '', 'child': [{'name': item.name, 'url': item.url}] })
                
                continue

            for item_menu in menudata:
                if item.parent == None: # add parebt
                    if item_menu['id'] == item.id:
                        item_menu['name'] = item.name
                        item_menu['url'] = item.url

                else: # add child
                    if item_menu['id'] == item.parent:
                        item_menu['child'].append({'name': item.name, 'url': item.url})
                        break

            else: # not found parent
                if item.parent == None: # add parent
                    menudata.append({'id': item.id, 'name': item.name, 'url': item.url, 'child': [] })

                else: # add child
                    menudata.append({'id': item.parent, 'name': '', 'url': '', 'child': [{'name': item.name, 'url': item.url}] })

        return jsonify({ 'payload': menudata })