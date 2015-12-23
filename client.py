import socket
import sys
import getopt

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def client_request(ip_adr,port_no,file_name,method):
    # Connect the socket to the port where the server is listening
    server_address = (ip_adr, int(port_no))
    print >>sys.stderr, 'connecting to %s port %d' % server_address
    sock.connect(server_address)
    try:
    
        if file_name.split('.')[-1] in ('html','jpg','jpeg','txt','htm','gif'):            
            # Send data
            headers = """HTTP/1.1\r
            Content-Type: {content_type}\r
            Content-Length: {content_length}\r
            Host: {host}\r
            Connection: close\r
            \r\n"""        
            header_bytes = headers.format(
                content_type="application/x-www-form-urlencoded",
                content_length=len(file_name),
                host=str(ip_adr) + ":" + str(port_no)
                ).encode('iso-8859-1')
            request=header_bytes
            if method=="GET":
                file_name+='?username=test&password=pass'
            if method=="POST":
                body = 'username=test&password=pass'                                 
                body_bytes = body.encode('ascii')
                header_bytes = headers.format(
                content_type="application/x-www-form-urlencoded",
                content_length=len(body_bytes),
                host=str(ip_adr) + ":" + str(port_no)
                ).encode('iso-8859-1')
                request = header_bytes + body_bytes
                
            orig_request = method+' '+'/'+file_name+' '  
            orig_request+=request
            print >>sys.stderr, '\nSending Request:\n\n "%s"' % orig_request
            sock.sendall(orig_request)

            # Look for the response
            data = sock.recv(int(port_no))
            print >>sys.stderr, 'Received Server Reply:\n\n"%s"' % data
        else:
            print >>sys.stderr, '\n\nWrong file requested. Supported formats are : jpg,gif,html,txt,htm'

    finally:
        print >>sys.stderr, '\nClosing socket\n'
        sock.close()

def usage():
    print "\nRequired parameters missing (-n).Please use the below syntax"
    print "\nclient_code_name -n <server_IPaddress/name> [-p <port_number>] [-f <requested_file_name>]"


def main(argv):                                        
    try:                                
        opts, args = getopt.getopt(argv, "n:p:m:f:") 
    except getopt.GetoptError:          
        usage()                          
        sys.exit(2)
    ip_adr=None
    port_no=8080 
    file_name="index.html"
    method="GET"
    for opt, arg in opts:                
        if opt == "-n":      
            ip_adr= arg   
            print 'ip-address: ',ip_adr
        elif opt == '-p': 
            port_no=arg
            print 'port: ',port_no
        elif opt =="-f": 
            file_name = arg 
            print 'file: ',file_name
        elif opt =="-m": 
            method = arg 
            print 'method: ',method
    if not ip_adr:
        usage()
        sys.exit(2)
    else:
        client_request(ip_adr,port_no,file_name,method)
if __name__ == "__main__":
    main(sys.argv[1:])