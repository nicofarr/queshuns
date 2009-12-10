import time

import cherrypy
import jinja2
from filter_daemon import *

from simplejson import JSONEncoder
encoder = JSONEncoder()

def jsonify_tool_callback(*args, **kwargs):
    response = cherrypy.response
    response.headers['Content-Type'] = 'application/json'
    response.body = encoder.iterencode(response.body)

cherrypy.tools.jsonify = cherrypy.Tool('before_finalize', jsonify_tool_callback, priority=30) 

# jinja2 template renderer
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
def render_template(template,**context):
  global env
  template = env.get_template(template+'.jinja')
  return template.render(context)


# QUESHUNS
class Questions(object):

    fr = FilterRedis()

    @cherrypy.expose()
    def index(self):
        tweets =  self.fr.tweets()

        return render_template('index', tweets=tweets)

    @cherrypy.expose()
    def latest(self, since):
        if not since:
            return
        tweets = self.fr.tweets(limit=5, since=float(since))

        return render_template('tweets', tweets=tweets)


cherrypy.quickstart(Questions())
