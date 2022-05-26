from flask import render_template, g
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi

from flask_appbuilder import AppBuilder, BaseView, expose, has_access
from flask_appbuilder.api import BaseApi
from app import appbuilder, db


from .token_tools import get_guest_tokens
import requests 

SUPERSET_HOST = "https://superset.startuptrend.in"
GENERATE_TOKEN = "/generate_token"
TOKEN_LOGIN = "/token_login"

class MyView(BaseView):
    route_base = "/dashboards"
    # default_view = 'sales_dash'

    @expose('/sdk/')
    def sdk(self):
        # do something with param1
        # and render template with param
        # param1 = 'Goodbye %s' % (param1)
        
        self.update_redirect()
        return self.render_template('sdk.html')
    
    @expose('/custom_login/')
    def custom_login(self):
        # do something with param1
        # and render template with param
        # param1 = 'Goodbye %s' % (param1)
        username = g.user.username
        #params = {"username": username, "redirect": "https://superset.startuptrend.in/superset/dashboard/10/?preselect_filters=%7B%7D&standalone=true"}
        params = {"username": username, "redirect": "https://superset.startuptrend.in/superset/dashboard/11/?standalone=true"}
        resp = requests.get(SUPERSET_HOST+GENERATE_TOKEN, params=params)
        token = resp.json()['token']
        token_login_url = SUPERSET_HOST + TOKEN_LOGIN + f"?token={token}"
        print(token, token_login_url)
        self.update_redirect()
        return self.render_template('customlogin.html', url=token_login_url)

class TokenAPI(BaseApi):
    
    @expose("/fetchGuestToken")
    def fetch_guest_token(self):
        body = {
            "resources": [
                {
                    #"id": "10",
                    "id": "11",
                    "type": "dashboard"
                }
            ],
            "rls": [
                #{"clause": 'name="general"'}
            ],
            "user": {
                "first_name": g.user.first_name,
                "last_name": g.user.last_name,
                "username": g.user.username 
            }
        }
        print(f"username: {g.user.username}, {g.user.first_name}, {g.user.last_name}")
        token = get_guest_tokens(body)
        print("*"*100)
        print(token)
        return self.response(200, token = token['token'])

appbuilder.add_api(TokenAPI)

appbuilder.add_view_no_menu(MyView())

appbuilder.add_link("Custom Login", href='/dashboards/custom_login', category='Demos')
appbuilder.add_link("SDK", href='/dashboards/sdk', category='Demos')
"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


db.create_all()
