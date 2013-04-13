import webapp2

class MainPage(webapp2.RequestHandler):
  def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.write('Hello, webapp2 World!!!')

class Stats(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Weekly stats')
        
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/stats', Stats)],
                              debug=True)
