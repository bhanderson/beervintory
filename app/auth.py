from functools import wraps
from flask import make_response, redirect, request, session
from app import app
import ldap


USERNAME_KEY = "username"

admin = ['bhanderson','wchristie','jwisman']

def has_voted():
    return session[USERNAME_KEY]['voted']

def vote():
    session[USERNAME_KEY]['voted'] = True

def is_logged_in():
    return USERNAME_KEY in session

def get_username():
    if is_logged_in():
        return session[USERNAME_KEY]['username']
    return 'Anonymous'

def is_admin(username = None):
    if not username:
        if not is_logged_in():
            return False
        username = session[USERNAME_KEY]['username']
    return username in admin

def login(username):
    if is_logged_in():
        logout()
    session[USERNAME_KEY] = {'username': username,
            'voted': False,
            'admin': is_admin(username)}

def logout():
    session.pop(USERNAME_KEY, None)

def check_builtin(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    builtins = {"test":"a"}
    for key, val in builtins.iteritems():
        if key == username and val == password:
            return True
    return False

def check_ldap(username, password):
    """
    Calls out to LDAP to verify a given username and password.
    Returns a dictionary that describes a User on success, raises an exception
    otherwise.
    """
    try:
        # Connect to LDAP server with our query credentials.
        # TODO: Retry a few times.
        ldap_server = "ldap://seadc03.desktop.isilon.com"
        ldap_object = ldap.initialize(ldap_server)

        ldap_bind_dn = "CN=genericid,CN=Users,DC=desktop,DC=isilon,DC=com"
        ldap_bind_pass = "Auth_LDAP."
        ldap_object.set_option(ldap.OPT_REFERRALS, 0)
        r = ldap_object.simple_bind_s(who=ldap_bind_dn, cred=ldap_bind_pass)
        if r[0] != 97:
            raise Exception("Cannot bind to LDAP server.")

        # Try searching for this user
        ldap_base_dn = "DC=desktop,DC=isilon,DC=com"
        ldap_filter = "(&(objectclass=user)(sAMAccountName=%s))" % username
        ldap_attr = ["Department", "MemberOf"]
        user_from_ldap = ldap_object.search_s(ldap_base_dn, ldap.SCOPE_SUBTREE,
                                              ldap_filter, ldap_attr)
        dn = user_from_ldap[0][0]
        if dn is None:
            #raise Exception("Invalid username/password")
            return False

        r = ldap_object.unbind()

        # Now bind (authenticate) the DN with their password
        ldap_object = ldap.initialize(ldap_server)
        ldap_object.set_option(ldap.OPT_REFERRALS, 0)
        r = ldap_object.simple_bind_s(who=dn, cred=password)
        r = ldap_object.unbind()

    except ldap.INVALID_CREDENTIALS, e:
        #raise Exception("Invalid username/password")
        return False
    except ldap.LDAPError, e:
        #raise Exception("LDAP Error %s" % str(e))
        return False

    return True

def authenticate(username, password):
    """
    Given a username and password try to authenticate the user against
    the configured user stores.  If authentication is successful a
    session is created for the user.
    """
    # support multiple user stores
    methods = (check_builtin, check_ldap)
    for method in methods:
        if method(username, password):
            # create a session for the user
            login(username)
            return True
    return False

def send_401_response():
    """Sends a 401 response that enables basic auth"""
    resp = make_response("Login Required")
    resp.status_code = 401
    resp.headers["WWW-Authenticate"] = "Basic realm=\"Login Required\""
    return resp

def requires_auth(f):
    """decerator for requiring auth to a function"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if is_logged_in():
            return f(*args, **kwargs)
        return redirect("/login?return={ret}".format( \
                ret=request.path), code=302)
    return decorated

def requires_admin(f):
    """decerator for requiring auth to a function"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if is_admin():
            return f(*args, **kwargs)
        return redirect("/", 302)
    return decorated

def requires_basic_auth(f):
    """decerator for requiring http basic auth to a function"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # otherwise we need to check for http basic auth
        auth = request.authorization
        if auth:
            # support multiple user stores
            methods = (check_builtin, check_ldap)
            for method in methods:
                if method(auth.username, auth.password):
                    # create a session for the user
                    login(auth.username)
                    return f(*args, **kwargs)
        # otherwise send 401
        return send_401_response()
    return decorated

@app.context_processor
def inject_admin():
    return dict(admin=is_admin(), logged_in=is_logged_in(),
            username=get_username())
