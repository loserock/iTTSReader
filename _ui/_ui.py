# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Sep 12 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext

###########################################################################
## Class MainWindow
###########################################################################

class MainWindow ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"iTTS Reader - a simple text to speech app", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_richText1 = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer1.Add( self.m_richText1, 1, wx.EXPAND, 2 )

		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel1.SetMinSize( wx.Size( -1,30 ) )
		self.m_panel1.SetMaxSize( wx.Size( -1,30 ) )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		m_choice1Choices = []
		self.m_choice1 = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0 )
		self.m_choice1.SetSelection( 0 )
		bSizer2.Add( self.m_choice1, 0, wx.ALL|wx.EXPAND, 3 )


		bSizer2.Add( ( 20, 0), 0, 0, 0 )

		self.m_button1 = wx.Button( self.m_panel1, wx.ID_ANY, u"Speak", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button1, 0, wx.ALL, 3 )


		self.m_panel1.SetSizer( bSizer2 )
		self.m_panel1.Layout()
		bSizer2.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 0, wx.ALL|wx.EXPAND, 0 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_choice1.Bind( wx.EVT_CHOICE, self.setVoice )
		self.m_choice1.Bind( wx.EVT_SET_FOCUS, self.updateVoiceList )
		self.m_button1.Bind( wx.EVT_BUTTON, self.speak )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def setVoice( self, event ):
		event.Skip()

	def updateVoiceList( self, event ):
		event.Skip()

	def speak( self, event ):
		event.Skip()


