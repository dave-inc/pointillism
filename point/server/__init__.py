from flask import Flask, g, session
from string import Template
from flask_simpleldap import LDAP

from .exception_handling import add_exception_handling
from .github import github_routes
from .api.v1 import v1_routes
from .paypal import paypal_routes
from .render import render_routes

from point.server.base import get_me
from ldapauth.flask.routes import auth_routes, register_config

from config import (ADMIN_USER, ADMIN_PASS, LDAP_BASE_DN, SECRET_KEY,
                    DOMAIN, HOST, ENV, STATIC_DIR, PAYPAL_CLIENT_ID, LDAP_HOST)

DOT_FORMATS = ["dot", "gv", "pu"]
IS_DEV = (ENV == "develop")

LANDING_ROUTES = [
    "/profile", "/account", "/repos", "/getting-started",
    "/about", "/contact", "/paypal/confirm", "/detail",
    "/whiteboard"
]

app = Flask(__name__)
add_exception_handling(app)
app.register_blueprint(github_routes, url_prefix='/github')
app.register_blueprint(v1_routes, url_prefix='/v1')
app.register_blueprint(auth_routes)
app.register_blueprint(render_routes)
app.register_blueprint(paypal_routes)

register_config(app,
                ldap_host=LDAP_HOST,
                ldap_base_dn=LDAP_BASE_DN,
                ldap_username=ADMIN_USER,
                ldap_password=ADMIN_PASS,
                ldap_login_view='auth.login'
                )
app.config['SECRET_KEY'] = SECRET_KEY

ldap = LDAP()


@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = get_me()
        # Create a global with the LDAP groups the user is a member of.
        # g.ldap_groups = ldap.get_user_groups(user=session['username'])


@app.route("/")
def welcome():
    me = get_me()
    username = ''
    email = ''
    if me:
        username = me.cn
        email = me.email or ''

    with open(STATIC_DIR + '/index.html', 'r') as fp:
        template = Template(fp.read())

        return template.substitute(
            host=HOST,
            domain=DOMAIN,
            paypalId=PAYPAL_CLIENT_ID,
            username=username,
            email=email
        )


for route in LANDING_ROUTES:
    app.route(route)(welcome)


def run():
    app.run(host='0.0.0.0', port=5001, debug=IS_DEV, threaded=True)
