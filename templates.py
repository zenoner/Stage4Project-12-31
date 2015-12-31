#import cgi #NEED TO REMOVE THEM (THREE #)
#import urllib 
import os

#from google.appengine.api import users
from google.appengine.ext import ndb 

import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape=True)



class Handler(webapp2.RequestHandler):
    #Write small strings to the webstie
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
    #Render jija2 templates
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
    #Write the jinja template to the website
        self.write(self.render_str(template, **kw))

#Database_ndb 
class Comment(ndb.Model):
   user = ndb.StringProperty()
   comment = ndb.StringProperty()
   date = ndb.DateTimeProperty(auto_now_add=True)

#NOT WORKING 12-17 REMOVE
#c = Comment(user='Seiji',
#            comment='This is a test')
#c2 = Comment(user='Hiro',
#            comment='My name is Hiroshi')

#c2.put()
#c.put()


#import time 
#time.sleep(.1) #wait for .1 seconds


class MainPage(Handler):
    def get(self):

        query = Comment.query().order(-Comment.date) #I used a minus sign
        comment_list = query.fetch() #To fetch the data

        #user_list = query.fetch(5) REMOVE
        #print '#####'
        #print len(user_list)
        #print user_list[0]
        #print '#####'

        #print '#####'
        #for picture in query:
        #    print picture
        #print '#####'

        #table = '<table>\n<tr><th>Link</th><th>Comment</th></tr>\n'
        #for author in query:
        #    user = author.user
        #    comment = author.comment

        #    row = '<tr>\n'
        #    row += '<td>'+ user + '</td>\n'
        #    row += '<td>' + comment + '</td>\n'
        #   row += '</tr>\n'

        #    table += row
        #    table += '</table>\n'

           # render_html = "comment.html" % (table)

           # self.response.out.write(render_html)


        #user = self.request.get_all("user")
        #comment = self.request.get_all("comment")
        self.render("comment.html", comment_list=comment_list)
        #self.render("comment.html")

class Guestbook(webapp2.RequestHandler):
    def post(self):

        #user = self.request.get('user')
        #comment = Comment(parent=ndb.Key()

        #self.response.write('<body>You wrote it by HIROOOOOOO !!!:<pre>')
        #author = self.request.get_all("user")
        #author = cgi.escape(self.request.get('user'))
        
        user = self.request.get('user')
        comment = self.request.get('comment')

        if user and comment:
            author= Comment(user=user, comment=comment)
            author.put()

            import time 
            delay = 0.1
            time.sleep(delay)
            self.redirect('/')
        else:
            self.redirect('/?error=Please fill out the link and comment section!')

        #Test to see user and comment REMOVE lines 112 to 120
        print '#####'
        print user, comment
        print '#####'

        #self.render("comment.html")
        #self.response.write('<br>')
        #self.response.write(cgi.escape(self.request.get('commment')))
        #self.response.write('</pre></body>')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
], debug=True)
