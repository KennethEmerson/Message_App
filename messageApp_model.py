from pubsub import pub
from threading import Thread
from socket import *

###############################################################################################
# class CommThread inherites from Thread and additional socket logic is added
###############################################################################################

class CommThread(Thread):

    def __init__(self,IP_adress):
        Thread.__init__(self)
        Thread.daemon = True                        # stop thread after window closes
        self.host = IP_adress                       # hostadress (own IP if server)
        self.port = 13000                
        self.start()                                #start thread and applies method "run"

###############################################################################################

    #override the standard run method of the thread
    def run(self):  
        self.buf = 1024
        self.addr = (self.host, self.port)
        self.Socket = socket()
        print("Server IP-adress: " + self.host)
        self.Socket.bind(self.addr)
        self.Socket.listen(5)
        print("Socket listening")
        print("ready to accept")
        self.client_conn, self.client_addr = self.Socket.accept()
        print('Connected with ' + self.client_addr[0] + ':' + str(self.client_addr[1]))
        while 1:
            ready = select.select([self.client_conn, ], [], [], 2)
            if ready[0]:
                data = self.client_conn.recv(self.buf)
                datastr = data.decode('utf-8')
                if datastr == "":
                    break
                wx.CallAfter(pub.sendMessage, "incoming_message", message=  datastr)

        wx.CallAfter(pub.sendMessage, "incoming_message", message="conversation ended by" + self.client_addr[0])
        self.Socket.close()
        print("thread stopped")