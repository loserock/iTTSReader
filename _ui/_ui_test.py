#! /usr/bin/env python
# -*- coding: utf-8 -*-

from _ui import MainWindow, wx

def main():
    app = wx.App(False)
    mainWindow = MainWindow(None)
    mainWindow.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()