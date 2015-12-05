from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi 
# Define webserverHandler class that extends from BaseHTTPRequestHandler.
class webserverHandler(BaseHTTPRequestHandler):
	# create a do_GET function to handle GET requests.
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += ('<html><body><h1>The English Page!</h1> '
				'<form method = "POST" enctype = "multipart/form-data" action = "/hello">'
				'<h2>Enter your statement here:</h2><input name = "message" type="text">'
				'<input type = "submit" value = "Submit"> </form>'
				"<p>Yo what's up dog?</p></body></html>")
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/bonjour"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += ('<html><body><h1>The French Page!</h1> '
				'<form method = "POST" enctype = "multipart/form-data" action = "/hello">'
				'<h2>Enter your statement here:</h2><input name = "message" type="text">'
				'<input type = "submit" value = "Submit"> </form>'
				'<p>yo ce qui est le haut de chien?</p></body></html>')
				self.wfile.write(output)
				print output
				return

		except IOError:
			self.send_error(404, "File not found %s" % self.path)

    # Create a do_POST method to handle POST requests.
	def do_POST(self):
		try:
			# Send response on successful POST request.
			self.send_response(301)
			self.end_headers()

			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				messagedata = fields.get('message')

			output = ""
			output += "<html><body>"
			output += "<h3>Heads up for a message coming your way...</h3>"
			output += "<h1>%s</h1>" % messagedata [0]
			output += ('<html><body><h1>The French Page!</h1> '
				'<form method = "POST" enctype = "multipart/form-data" action = "/hello">'
				'<h2>Enter your statement here:</h2><input name = "message" type="text">'
				'<input type = "submit" value = "Submit"></form>') 
			output += '</body></html>'
			self.wfile.write(output)
			print output

		except:
			pass

# Create a main method which initiates the web server and sets
# up the port we operate on.
def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print 'Web server is up and running on port %s' % port
		server.serve_forever()

    # Main method is exited when user holds ctrl + c on the keyboard.
	except KeyboardInterrupt:
		print "Ctrl + C pressed, stopping web server..."
		server.socket.close()

# Main method runs as soon as python interprettor runs the script.
if __name__ == '__main__':
    main()
        

