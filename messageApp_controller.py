
import wx
import wx.stc as stc
import select
from pubsub import pub
from threading import Thread
from socket import *

from messageApp_view import Main_Window, Config_Window
from messageApp_model import CommThread

###############################################################################################
# Controller Class 
###############################################################################################

class Controller:
    
    # initialise the bindings between UI elements and the controller
    def __init__(self):
        self.config_window = Config_Window(None)
        self.config_window.server_choice.Bind(wx.EVT_RADIOBUTTON, self.server_client_change)
        self.config_window.client_choice.Bind(wx.EVT_RADIOBUTTON, self.server_client_change)
        self.config_window.ok_button.Bind(wx.EVT_BUTTON, self.on_config_ok)

        self.message_window = Main_Window(None)
        self.message_window.close_button.Bind(wx.EVT_BUTTON, self.closeApp)
        self.message_window.input_txtbox.Bind(wx.EVT_TEXT_ENTER, self.send_message,self.message_window.input_txtbox)
        self.message_window.Bind(wx.EVT_ACTIVATE, self.at_startup)
        self.config_window.Show()

    ###############################################################################################

    # activates the corresponding UI method when the user changes the radio button setting in
    # the config window
    
    def server_client_change(self,event):
        self.config_window.server_client_change()
    
    ###############################################################################################

    # fetches the correct hostadress and activates the socket and thread to allow the communication

    def on_config_ok(self,event):
        flag, IPaddress = self.config_window.on_config_ok()
        
        if (flag != 1):
            if (flag == 2):
                hostname = gethostname()
                IPaddress = gethostbyname(hostname)
            
            self.config_window.Close()
            self.thread= CommThread(IPaddress)
            pub.subscribe(self.receive_message, "incoming_message")
            self.message_window.Show()

    ###############################################################################################

    def at_startup(self,event):
        self.message_window.at_startup()

    ###############################################################################################

    def send_message(self,event):
        text = self.message_window.own_text_read()
        self.message_window.own_text_add("<you> " + text + "\n")
        bytetext = bytes(text,'utf-8')

        try: 
            self.thread.client_conn.send(bytetext)
        except AttributeError: 
            self.message_window.received_text_add("<ERROR: No Connection>")
        self.message_window.own_text_clear_screen()

    ###############################################################################################

    def receive_message(self,message):

        self.message_window.received_text_add("<guest> " + message + "\n")
        self.message_window.own_text_clear_screen()

    ############################################################################################### 

    def closeApp(self, event):

        text = "conversation ended"
        self.message_window.own_text_add(text + "\n")
        bytetext = bytes(text, 'utf-8')
        try:
            self.thread.client_conn.send(bytetext)
            self.thread.Socket.close()
        except Exception:
            print("no connection")
        self.message_window.Destroy() 
