import socket
import sys
import logging
#from socket import *
from thread import *
from time import sleep
import errno

#Function for handling connections. This will be used to create threads
def clientthread(conn,port):
   
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        try:
            data = conn.recv(port) #receive data from client
            string = bytes.decode(data) #decode it to string
            #determine request method  (POST and GET are supported)
            request_method = string.split(' ')[0]
            print ("Method: ", request_method)
            print ("Request body: ", string)
                
            if (request_method == 'GET') | (request_method == 'POST'):
                    #file_requested = string[4:]    
                # split on space "GET /file.html" -into-> ('GET','file.html',...)
                file_requested = string.split(' ')
                file_requested = file_requested[1] # get 2nd element
                
                #Check for URL arguments. Disregard them
                file_requested = file_requested.split('?')[0]  # disregard anything after '?'
            
                if (file_requested == '/'):  # in case no file is specified by the browser
                    file_requested = '/index.html' # load index.html by default
            
                print ("Serving web page [",file_requested,"]")
                if file_requested.split('.')[-1] in ('html','jpg','jpeg','txt','htm','gif'):
                    ## Load file content
                    try:
                        
                        file_handler = open(file_requested[1:],'rb')
                        response_content = file_handler.read() # read file content
                        file_handler.close()
                        response_headers = '\HTTP/1.1 200:Connection ok'
                
                    except Exception as e: #in case file was not found, generate 404 page
                        print ("!!!404 Error: File not found.\n", e)
                        response_headers =  '\HTTP/1.1 404:Page Not Found'   
                        response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"
                
                    server_response =  response_headers.encode() # return headers for GET and POST
                    server_response +=  response_content
                    

                    # content of the requested file will be sent to client if browser
                    for i in range(0, len(response_content)):
                        conn.send(response_content[i])
                else:
                    
                    fileFormat="Unknown file format '%s' .Supported formats are : jpg,gif,html,txt,htm" % file_requested.split('.')[-1]
                    print fileFormat
                    logging.warning("<b><p>Unknown file format '%s' .Supported formats are : jpg,gif,html,txt,htm</p></b>" % file_requested.split('.')[-1])
                    for i in range(0, len(fileFormat)):
                        conn.send(fileFormat[i])
                    conn.close()
                #conn.send(server_response)
                print ("Closing connection with client")
                conn.close()
            else:
                print("Unknown HTTP request method:", request_method)
                response_method_wrg = b"Unknown HTTP request method:%s \nPython HTTP server" % request_method
                for i in range(0, len(response_method_wrg)):
                        conn.send(response_method_wrg[i])
                conn.close()
        except socket.timeout,e:
                    #when timeout occurs
                    err=e.args[0]
                    pass                    
                    logging.info('timed out')
                    if err== 'timed out':
                        sleep(1)
                        print "Connection timed out,retry later"                      
                        continue
        except socket.error,e:
                    #when DATA not available occurs
                    err=e.args[0]
                    pass                    
                    if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                        sleep(1)                       
                        continue
                  

def run_server(serverPort):

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """to reuse te same socket port"""
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print 'Socket created'
    #prepare a server socket
    try:                                 
        serverSocket.bind(('',serverPort))
    except serverSocket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    print 'Socket bind with localhost complete'
    print 'Server port:',serverPort
    serverSocket.settimeout(10.0)
    while True:
        try:
            #establish the connection
            print 'Ready to serve...'    
            print ("Awaiting New connection")
            serverSocket.listen(1) # maximum number of queued connections            
            print 'Socket now listening'
            connectionSocket, addr = serverSocket.accept()
            # conn - socket to client
            # addr - clients address
            
            print("Got connection from:", addr)
             #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            start_new_thread(clientthread ,(connectionSocket,serverPort))
        except socket.timeout,e:
            #when timeout occurs
            err=e.args[0]
            pass                    
            logging.info('timed out')
            if err== 'timed out':
                sleep(1)
                print "Connection timed out,retry later"                      
                continue
                
           
                
    serverSocket.close() 

def usage():
    print "\nplease enter in the correct format\n"
    print "server_code_name [<port_number>]\n"
def main(argv):  
    port_no=8080                                      
    try:   
        if len(argv)==1:                             
            port_no=int(argv[0])
        else:         
            usage()                          
            sys.exit(2)
    except Exception as e: 
        print '%s',e
    run_server(port_no)
    
if __name__ == "__main__":
    main(sys.argv[1:])
