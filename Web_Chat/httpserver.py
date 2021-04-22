from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from socketserver import ThreadingMixIn
from bs4 import BeautifulSoup

HOST = '0.0.0.0'
PORT = 35780

users = dict()

class RequestHandler(BaseHTTPRequestHandler):

    #files path
    index = 'index.html'
    register = 'register.html'
    chat_room = 'chat_room.html'
    not_found = 'not_found.html'
    curentfile = None

    def do_GET(self):
        self.log_message('Incomming GET request....')
        if self.path == '/':
            self.curent_path(self.index)

        elif self.register in self.path:
            if f'{self.register}?name=' in self.path:
                self.do_POST()    
            else:
                self.curent_path(self.register)

        elif self.chat_room in self.path:
            if self.client_address[0] in users:
                self.chatroom(self.chat_room)
            else:
                pass

    def curent_path(self, data):
        #open current path
        with open(data) as fh:
                html = BeautifulSoup(fh,'html.parser')        
        try:
            self.send_response_to_client(200, html)
        except FileNotFoundError:
            self.send_response_to_client(404, html)

    def do_POST(self):
        self.log_message('Incomming POST request....') 
        data = parse_qs(self.path[15:])

        #save the user in a dictionary
        try:
            users[self.client_address[0]] = data['name'][0]
            self.log_message(str(users))
        except KeyError:
            self.log_message('incorect parameters')

        with open(self.register) as fh:
                html = BeautifulSoup(fh,'html.parser')

        #registration
        if self.client_address[0] in users.keys():
            tag = html.new_tag('a', href=f'/{self.chat_room}')
            tag.string = 'Enter Room'
            html.form.insert_after(tag)
            self.send_response_to_client(200, html)    
        #unregistered    
        else:
            tag = html.new_tag('h2')
            tag.string = 'You must enter your name first'
            html.form.insert_after(tag)
            self.send_response_to_client(404, html)
    #chatroom path

    def chatroom(self, path):
        js_code = f'''const user = '{users[self.client_address[0]]}'
        var ws = new WebSocket("ws://laurentiuweb.asuscomm.com:8080"),
                messages = document.createElement('ul');
            ws.onmessage = function (event) {{
                var messages = document.getElementsByTagName('ul')[0],
                    message = document.createElement('li'),
                    content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
            }};
            
        document.querySelector('.msg').appendChild(messages);

        ws.onopen = function (){{
                const x = document.getElementById("message").value;
                ws.send(`${{user}} : ${{x}}`);
            }};

        var reset = document.querySelector('#message');
        reset.addEventListener('click', function () {{
            reset.value ='';
        }},false);'''

        with open(path) as chat:
            html = BeautifulSoup(chat, 'html.parser')
        tag = html.new_tag('script')
        tag.string = js_code
        html.body.insert_after(tag)
        self.send_response_to_client(200, html)

    def send_response_to_client(self, status_code, data):
        # Send OK status
        self.send_response(status_code)
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send the response
        self.wfile.write(str(data).encode())

#opens one thread for each client
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):   
    pass

if __name__=='__main__':
    print('Starting httpd on port {}'.format(PORT))
    server = ThreadedHTTPServer((HOST,PORT), RequestHandler)
    server.serve_forever()