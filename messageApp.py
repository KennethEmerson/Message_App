import wx

from messageApp_view import Main_Window, Config_Window
from messageApp_controller import Controller

if __name__ =='__main__':
    app = wx.App()
    Controller()
    app.MainLoop()