from http.server import BaseHTTPRequestHandler, HTTPServer
import json

hostName = "localhost"
serverPort = 5000

def parser(query):
    splitted = query.split('&')
    ret = {}
    for pair in splitted:
        kvp = pair.split('=')
        ret[kvp[0]]=kvp[1]
    return ret

users = [
    {
    "username": "admin",
    "password": "admin"
    },
]

def authentication(userData):
    for user in users:
        if user["username"] == userData["username"] and user["password"] == userData["password"]:
            return True
    return False

routes = {
    "static": {
        "/": open("index.html").read(),
    },
    "api": {
        "get":{
            "/api/login":{
                "message": "Please Login",
                "view": open("login.html").read()
            },
            "/api/logout":{
                "message": "Please Login",
                "view": open("login.html").read()
            },
            "/api/register":{
                "message": "Please Create A New User ",
                "view": open("register.html").read()
            }
        },
        "post":{
            "/api/login":{
                
            }
        }
    }
}

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in routes["static"]:
            self.http_header(200, "text/html")
            self.wfile.write(bytes(routes["static"][self.path], "utf-8"))
        elif self.path.startswith("/api"):
            self.http_header(200, "application/json")
            obj = routes["api"]["get"][self.path]
            self.wfile.write(bytes(json.dumps(obj), "utf-8"))
        else:
            self.http_header(404, "text/html")
            self.write(bytes("404: Page not found", "utf-8"))
        return
    
    def do_POST(self):
        if self.path.startswith("/api"):
            self.http_header(200, "application/json")
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            formData = parser(post_data.decode("UTF-8"))
            if self.path == "/api/login":
                obj = self.userAuthenticate(formData)
                self.rfile.write(bytes(json.dumps(obj), "utf-8"))
            elif self.path == "/api/register":
                return
        else:
            self.http_header(200, "text/html")
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            userData = parser(post_data.decode("UTF-8"))
            if authentication(userData):
                self.wfile.write(bytes("Welcome, " + userData["username"], "UTF-8"))
            else:
                self.wfile.write(bytes("Username Or Password Are Not Correct.", "UTF-8"))
            self.wfile.write(bytes("<a href=\"/login\">login</a>", "UTF-8"))
        return
    
    def http_header(self, statuscode, contenttype):
        self.send_response(statuscode)
        self.send_header("Content-type", contenttype)
        self.end_headers()
    
    def userAuthenticate(self, formData):
        if authentication(formData):
            return {
                "status": 200,
                "message": "Welcome, " + formData["username"],
                "view": open("welcome.html").read()
            }
        else:
            return {
                "status": 400,
                "message": "Username Or Password Are Not Correct",
                "view": open("login.html").read()
            }
    def userRegister(self, formData):
        for user in users:
            if user["username"] == formData["username"]:
                return {
                    "status": 400,
                    "message": "The username has been taken. Please choose a different name.",
                    "view": open("register.partial.html").read()
                }
        if formData["password1"] != formData["password2"]:
            return {
                "status": 400,
                "message": "The Passwords Are Not The Same",
                "view": open("register.html").read()
            }
        else:
            users.append(formData)
            return {
                "status": 200,
                "message": "Welcome, " + formData["username"],
                "view": open("welcome.html").read()
            }

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server has stopped.")

