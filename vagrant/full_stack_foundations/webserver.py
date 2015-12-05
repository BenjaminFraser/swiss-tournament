from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from restaurant_queries import *
# Within this Python file I've created a basic web-server, which provides
# the functionality to search, create, edit and delete restaurants that
# are stored within the database. For this we handle simple GET and POST
# requests, and make use of a query function file, restaurant_queries. The
# restaurant queries file performs various functions that connect to the
# database using SQL Alchemy. The original setup file for this database is 
# within database_setup.py, where the classes and table data is setup.
# 
# Define webserverHandler class that extends from BaseHTTPRequestHandler.
class webserverHandler(BaseHTTPRequestHandler):
    # create a do_GET function to handle GET requests.
    def do_GET(self):
        restaurant_string = list_restaurants()
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += '<html><body><h1>Our restaurants!!</h1>'
                for i in restaurant_string:
                    output += '<h3>%s</h3>' % i[0]
                    output += '<ul><li><a href="/restaurants/%s/edit">Edit</a>' % i[1]
                    output += '<li><a href="/restaurants/%s/delete">Delete</a></li></ul><br>' % i[1]
                output += '<p>Cant find your restaurant? Add one <a href ="/restaurants/new">here.</a>'
                output += '</body></html>'
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += '<html><body><h1>Create a new restaurant</h1>'
                output += '<form method = "POST" enctype = "multipart/form-data" action = "/restaurants/new">'
                output += '<h2>New restaurant name:</h2>'
                output += '<input type = "text" name = "newRestaurantEntry"><br>'
                output += '<input type = "submit" value = "Create">'
                output += '</body></html>'
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                # We need to obtain the id number of the restaurant to edit.
                # The id is in the path, as defined at the edit button.
                restaurantIDnumber = self.path.split("/") [2]
                # Using this id we can then query the database and find the name.
                edit_name = fetch_name_from_id(restaurantIDnumber)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # Generate HTML for editing specific restaurant.
                output = ""
                output += '<html><body><h1>%s</h1>' % edit_name
                output += '<form method="POST" enctype="multipart/form-data" action="/restaurants/%s/edit"' % restaurantIDnumber
                output += '<h3>Enter a new name below:</h3><br>'
                output += '<input type="text" name="changeName"><br>'
                output += '<input type="submit" value="Change" placeholder="New Name"></form>'
                output += '</body></html>'
                self.wfile.write(output)
                return

            if self.path.endswith("/delete"):
                # We need to obtain the id number of the restaurant to edit.
                # The id is in the path, as defined at the edit button.
                restaurantIDnumber = self.path.split("/") [2]
                # Using this id we can then query the database and find the name.
                delete_name = fetch_name_from_id(restaurantIDnumber)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # Generate HTML for delete warning/confirmation.
                output = ""
                output += '<html><body><h1>%s</h1>' % delete_name
                output += '<form method="POST" enctype="multipart/form-data" action="/restaurants/%s/delete"' % restaurantIDnumber
                output += '<p>Are you sure you want to delete? '
                output += 'Enter the restaurant name below to confirm.</p>'
                output += '<input type="text" name="deleteName" placeholder="Restaurant name"><br>'
                output += '<input type="submit" value="Delete" placeholder="Delete"></form><br><br>'
                output += '<h5>Changed your mind? Click <a href="/restaurants">here</a> to return.</h5>'
                output += '</body></html>'
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, "File not found %s" % self.path)

    # Create a do_POST method to handle POST requests.
    def do_POST(self):
        try:
            # Handle new restaurant requests.
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagedata = fields.get('newRestaurantEntry')
                    add_restaurant(messagedata[0])

                    print 'added %s to the database' % messagedata[0]
                    #output = ""
                    #output += '<html><body><h1>Create a new restaurant</h1>'
                    #output += '<form method = "POST" enctype = "multipart/form-data">'
                    #output += '<h2>New restaurant name:</h2>'
                    #output += '<input type = "text" name = "message"><br>'
                    #output += '<input type = "submit" value = "submit"><br><br>'
                    #output += '<h3>Your restaurant %s has been added to the database.</h3><br>' % messagedata
                    #output += '<h4> Click <a href = "/restaurants">here</a> to view all restaurants.</h4>'
                    #output += '</body></html>'
                    #self.wfile.write(output)

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return
            # Handle edit requests.
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagedata = fields.get('changeName')
                    # We need to obtain the id number of the restaurant to edit.
                    restaurantIDnumber = self.path.split("/") [2]
                    # Using this id we can then query the database and find the name.
                    edit_name = fetch_name_from_id(restaurantIDnumber)
                    # Change the name using the change function in restaurant_queries.
                    # Validate the change was successful beforehand.
                    if change_restaurant_name(restaurantIDnumber, messagedata[0]) == True:
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        # Set location back to the restaurants list.
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                        return
                    # Flag up a warning alert if the change was unsuccessful.
                    else: 
                        print "The change didnt work."
                        output += '<html><body><h3>Oops, there was an error.</h3>'
                        output += '<p>Click <a href="/restaurants">here</a> to return home.</p>'
                        output += '</body></html>'
                        self.wfile.write(output)
                        return
            # Handle delete requests.
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagedata = fields.get('deleteName')
                    # We need to obtain the id number of the restaurant to edit.
                    # The id is in the path, as defined at the edit button.
                    restaurantIDnumber = self.path.split("/") [2]
                    # Using this id we can then query the database and find the name.
                    delete_name = fetch_name_from_id(restaurantIDnumber)
                    # Delete the restaurant entry using the delete function from the queries.
                    # Validate the delete was successful before carrying on.
                    if delete_restaurant(restaurantIDnumber, messagedata[0]) == True:
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                        return
                    # Create an error alert to notify the unsuccessful delete.
                    else:
                        print "The delete did not work."
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        output = ""
                        output += '<html><body><h3>Oops, there was an error.</h3>'
                        output += '<p>Click <a href="/restaurants">here</a> to return home.</p>'
                        output += '</body></html>'
                        self.wfile.write(output)
                        return
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
        

