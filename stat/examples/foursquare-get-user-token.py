import webbrowser
import httplib
import bottle
import clients
import simplejson as json
from bottle import route, post, run, request

bottle.debug(True)

CONFIG = {
    'client_id'    : clients.clients[0][0],
    'client_secret': clients.clients[0][1],
    'redirect_uri' : 'http://localhost:8515/oauth_callback'
}

@route('/')
def home():
    try:
        url = "https://foursquare.com/oauth2/authenticate?client_id=%s&response_type=code&redirect_uri=%s" % (CONFIG['client_id'],CONFIG['redirect_uri'])
        return '<a href="%s">Connect with foursquare</a>' % url
    except Exception, e:
        print e

@route('/oauth_callback')
def on_callback():
    code = request.GET.get("code")
    if not code:
        return 'Missing code'
    else:
        print code
        conn = httplib.HTTPSConnection("foursquare.com");
        conn.request("GET", 
            "/oauth2/access_token"
            "?client_id=%s"
            "&client_secret=%s"
            "&grant_type=authorization_code"
            "&redirect_uri=%s"
            "&code=%s" 
            % (CONFIG['client_id'], CONFIG['client_secret'], CONFIG['redirect_uri'], code))
        resp = conn.getresponse()
        print resp.status, resp.reason
        d = json.loads(resp.read())
        token = d['access_token']
        f = open("token.py", "w")
        f.write("token = \""+token+"\"\n")
        f.close()

        return "token \""+token+"\" was written to token.py"
        
webbrowser.open("http://localhost:8515")
run(host='localhost', port=8515, reloader=True)