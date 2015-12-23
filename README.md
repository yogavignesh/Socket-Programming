# Socket-Programming

## CSE5344 - Project 1
## UTA ID:1001101504
## Yoga Vignesh Surathi

   Requirements:
 Version python 2.7.9
 Windows cmd line

   Implementation:
1. Python 2.7.9 version was used to implement this project.
2. There are 2 files one for server and another for client.
3. Both the get and post method requests are handled in the server.
4. The timeout for 10 milliseconds is handled and also the client requests are run using threads.
5. Non-blocking socket error has been handled using exception.
    There are two server files:
1)To access from browser:
server_client_access_from_browser.py
2)To access from commandline:
server_client_from_cmdline.py
    One client file:
client.py
Steps to run the program in command line:
1.Run the server_client_from_cmdline.py file in command prompt using
python server_client_from_cmdline.py 8080
2.Run the client.py file in a seperate command prompt
python client.py -n 127.0.0.1 [-p 8080] [-f "index.html"] [-m "GET"]
3.The opts with [] in the syntax are optional
4.After the request is run through client.py ,
the output from the server is received.
5.formats supported are html, jpg,gif,txt.
Steps to run the program in browser:
1. Run the server_client_access_from_browser.py file in command prompt using
python server_client_access_from_browser.py 8080
2.Access the localhost server using localhost:8080 through browser
or localhost:8080/index.html
3.Try looking for localhost:8080/balls.jpg
    Known Issues:
The server for browser code doesn't work for cmd line and vice versa due to encoding.
   References:
  1. http://www.binarytides.com/python-socket-server-code-example/
  2. http://stackoverflow.com/questions/16745409/what-does-pythons-socket-recv-return-for-nonblocking-sockets-if-no-data-is-r
  3. http://stackoverflow.com/questions/5755507/creating-a-raw-http-request-with-sockets

Thank you !!!
