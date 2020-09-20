###############################################################################################
# Contains all UI related classes and methods
###############################################################################################

import wx
import wx.stc as stc
import re 

###############################################################################################
# Config Window
###############################################################################################

#Defines the layout of teh configuaration window
class Config_Window(wx.Frame):
    def __init__(self,parent, style= wx.CLOSE_BOX):
        wx.Frame.__init__(self,parent,-1,"Small message App: config",size=(250,200))
        panel = wx.Panel(self)

        #vertical box thats holds all elements in window
        vert_boxsizer = wx.BoxSizer(wx.VERTICAL)

        #add a empty line
        vert_boxsizer.Add(wx.StaticText(panel, label=''), flag=wx.CENTER, border=5)

        #add two radiobuttons to config if user is host or client
        self.server_choice = wx.RadioButton(panel, 11, label="Server",pos = (40,60), style = wx.RB_GROUP)
        self.client_choice = wx.RadioButton(panel, 22, label="Client", pos = (40,100))
        self.server_choice.SetValue(True)
        vert_boxsizer.Add(self.server_choice, border=2)
        vert_boxsizer.Add(self.client_choice, border=2)

        #add a empty line
        vert_boxsizer.Add(wx.StaticText(panel, label=''), flag=wx.CENTER, border=5)

        #add the IP textbox
        self.IP_txtbox = wx.TextCtrl(panel,size=(200, 20),style = wx.TE_PROCESS_ENTER)
        self.IP_txtbox.SetMaxLength(15)
        self.IP_txtbox.SetEditable(False)
        vert_boxsizer.Add(self.IP_txtbox, flag = wx.CENTER, border=5)

        #add the OK button
        self.ok_button = wx.Button(panel, size=(120, 50), label="OK")
        vert_boxsizer.Add(self.ok_button, flag=wx.CENTER, border=2)

        panel.SetSizer(vert_boxsizer)
    
    ###############################################################################################

    def server_client_change(self): 
        if self.server_choice.GetValue():
            self.IP_txtbox.SetValue("")
            self.IP_txtbox.SetEditable(False)
        if self.client_choice.GetValue():
            self.IP_txtbox.SetEditable(True)

    def on_config_ok(self):
        if self.client_choice.GetValue():
            hostAddress = self.IP_txtbox.GetValue()
            if re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', hostAddress, flags=0):
                flag = 0
                print("ip ok")
            else: 
                flag = 1
                self.IP_txtbox.SetValue("")
                print("ip NOK")
        else:
            hostAddress = ""
            flag = 2
        return (flag,hostAddress)

###############################################################################################
# Main Window
###############################################################################################

class Main_Window(wx.Frame):
    def __init__(self,parent, style= wx.CLOSE_BOX):
        wx.Frame.__init__(self,parent,-1,"Small message App",size=(500,400))
        panel = wx.Panel(self)

        #vertical box thats holds all elements in window
        vert_boxsizer = wx.BoxSizer(wx.VERTICAL)

        #add empty line at top
        vert_boxsizer.Add(wx.StaticText(panel, label=''), flag=wx.CENTER, border=5)

        #text box for messages overview
        self.message_txtbox = wx.TextCtrl(panel, size=(470, 200),style= wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.TE_RICH)
        self.message_txtbox.SetMaxLength(400)
        self.message_txtbox.SetBackgroundColour("Grey")
        self.message_txtbox.SetEditable(False)
        vert_boxsizer.Add(self.message_txtbox, flag=wx.CENTER, border=5)
        

        #add empty line between messages overview and input textbox
        vert_boxsizer.Add(wx.StaticText(panel, label=''), flag=wx.CENTER, border=5)

        #input textbox
        self.input_txtbox = wx.TextCtrl(panel,size=(470, 50),style = wx.TE_PROCESS_ENTER)
        self.input_txtbox.SetMaxLength(400)
        vert_boxsizer.Add(self.input_txtbox, flag = wx.CENTER, border=5)

        #add empty line between input textbox and button
        vert_boxsizer.Add(wx.StaticText(panel, label=''), flag=wx.CENTER, border=5)

        #button to end app
        self.close_button = wx.Button(panel, size=(120, 50), label="End")
        vert_boxsizer.Add(self.close_button, flag=wx.CENTER, border=2)

        panel.SetSizer(vert_boxsizer)


##############################################################################################

    #gives focus to input textbox
    def at_startup(self):
        self.input_txtbox.SetFocus()

    #change color and add send text to messages overview
    def own_text_add(self,text):
        self.message_txtbox.SetDefaultStyle(wx.TextAttr(wx.GREEN))
        self.message_txtbox.AppendText(text)

    def own_text_clear_screen(self):
        self.input_txtbox.SetValue("")

    #change color and add received text to messages overview
    def received_text_add(self,text):
        self.message_txtbox.SetDefaultStyle(wx.TextAttr(wx.BLUE))
        self.message_txtbox.AppendText(text)

    #reads input text from input box
    def own_text_read(self):
        return self.input_txtbox.GetValue()

