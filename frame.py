#!/usr/bin/python

# PyIagno - wxPython based implementation of a classial Reversi game
#
# Copyright (C) 2010 aifreedom <me@aifreedom.com>
#
# PyIagno is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PyIagno is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyIagno; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

import wx
from game import IagnoGame
from ai import *

class IagnoFrame(wx.Frame):

    # Player movement instructions
    PlayerStr = ("Dark's move", "Light's move")
    None_ID, Easy_ID, Medium_ID, Insane_ID = range(1, 5)
    
    # =======================================================
    # Constructor
    # =======================================================
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER
                                                  | wx.MINIMIZE_BOX
                                                  | wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, *args, **kwds)
        self.frame_statusbar = self.CreateStatusBar(2, 0)

        self.Game = IagnoGame(ai=None)
        self.Board = IagnoBoard(self)

        self.__set_menus()
        self.__set_properties()


    def OnExit(self, event):
        self.Close()


    def OnNewGame(self, event):
        if self.noneAI.IsChecked():
            self.Game = IagnoGame(ai=None)
        if self.easyAI.IsChecked():
            self.Game = IagnoGame(ai=easy_ai)
        if self.mediumAI.IsChecked():
            self.Game = IagnoGame(ai=medium_ai)
        if self.insaneAI.IsChecked():
            self.Game = IagnoGame(ai=insane_ai)
        self.Board.New(self.Game)

    def OnNoneAI(self, event):
        self.Game.ai = None
        
    def OnEasyAI(self, event):
        self.Game.ai = easy_ai
        
    def OnMediumAI(self, event):
        self.Game.ai = medium_ai

    def OnInsaneAI(self, event):
        self.Game.ai = insane_ai
        
    def __set_menus(self):
        menuBar = wx.MenuBar()
        menuGame = wx.Menu()
        menuBar.Append(menuGame, "Game")
        newGame = menuGame.Append(-1, "New game",
                                  "Start a new game")
        menuGame.AppendSeparator()
        
        exit = menuGame.Append(-1, "Exit",
                               "Exit the program")

        menuAI = wx.Menu()
        menuBar.Append(menuAI, "AI Level")
        self.noneAI = menuAI.AppendRadioItem(self.None_ID, "None",
                                             "Select another human player")
        self.easyAI = menuAI.AppendRadioItem(self.Easy_ID, "Easy AI",
                                             "Select Easy AI")
        self.mediumAI = menuAI.AppendRadioItem(self.Medium_ID, "Medium AI",
                                           "Select Medium AI")
        self.insaneAI = menuAI.AppendRadioItem(self.Insane_ID, "Insane AI",
                                           "Select Insane AI")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnNewGame, newGame)
        self.Bind(wx.EVT_MENU, self.OnNoneAI, self.noneAI)
        self.Bind(wx.EVT_MENU, self.OnEasyAI, self.easyAI)
        self.Bind(wx.EVT_MENU, self.OnMediumAI, self.mediumAI)
        self.Bind(wx.EVT_MENU, self.OnInsaneAI, self.insaneAI)
        self.Bind(wx.EVT_MENU, self.OnExit, exit)


    def __set_properties(self):
        self.SetTitle("PyIango")
        self.SetSize((320, 366))
        self.frame_statusbar.SetStatusWidths([-4, -3])
        self.frame_statusbar.SetStatusText(IagnoFrame.PlayerStr[self.Board.Game.Player], 0)
        self.frame_statusbar.SetStatusText("Dard: %d Light: %d" % (self.Board.Game.DarkCnt, self.Board.Game.LightCnt), 1)

# end of class IagnoFrame


class IagnoBoard(wx.Window):
    
    def __init__(self, parent):
        wx.Window.__init__(self, parent)


        self.Bitmaps = [wx.Image("image/dark.png").ConvertToBitmap(),
                        wx.Image("image/light.png").ConvertToBitmap(),
                        wx.Image("image/blank.png").ConvertToBitmap()]

        self.parent = parent
        self.Game = parent.Game
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)

    def New(self, game):
        self.Game = game
        sz = (40, 40)
        # MemDC = [wx.MemoryDC(), wx.MemoryDC(), wx.MemoryDC()]
        # map(lambda dc, bmp: dc.SelectObject(bmp), MemDC, self.Bitmaps)

        dc = wx.PaintDC(self)
        for i in range(8):
            for j in range(8):
                dc.DrawBitmap(self.Bitmaps[self.Game[i][j]], j*sz[0], i*sz[1], True)
        self.Update()
        

        
    def __Draw(self, color, pos):
        x, y = pos
        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.Bitmaps[color], x*40, y*40, True)
        
    def __AIMove(self, aiPlayer):
        while not self.Game.IsEnd and self.Game.Player == aiPlayer:
            x, y = self.Game.ai(self.Game.Board, aiPlayer, len(self.Game))
            try:
                l = self.Game.Set((x, y))
            except self.Game.InvalidPositionException:
                self.parent.frame_statusbar.SetStatusText('Invalid move.', 0)
                raise 'AI Error'
            else:
                for yy, xx in l:
                    self.__Draw(aiPlayer, (xx, yy))
                self.Update()
                
    def Update(self):
        if self.Game.IsEnd:
            if self.Game.DarkCnt > self.Game.LightCnt:
                self.parent.frame_statusbar.SetStatusText('Dark wins!', 0)
            elif self.Game.DarkCnt < self.Game.LightCnt:
                self.parent.frame_statusbar.SetStatusText('Light wins!', 0)
            else:
                self.parent.frame_statusbar.SetStatusText('Draw...', 0)
        else:
            self.parent.frame_statusbar.SetStatusText(IagnoFrame.PlayerStr[self.Game.Player], 0)
        self.parent.frame_statusbar.SetStatusText("Dard: %d Light: %d" % (self.Game.DarkCnt, self.Game.LightCnt), 1)
                

    # =======================================================
    # Event handlers
    # =======================================================
    def OnClick(self, evt):
        y, x = evt.GetPosition()

        player = self.Game.Player
        try:
            l = self.Game.Set((x/40, y/40))
        except self.Game.InvalidPositionException:
            self.parent.frame_statusbar.SetStatusText('Invalid move.', 0)
        else:
            for yy, xx in l:
                self.__Draw(player, (xx, yy))
            self.Update()

            # if is human-AI game
            if not self.Game.IsEnd and self.Game.ai:
                self.__AIMove(not player)

    def OnPaint(self, evt):
        sz = (40, 40)
        # MemDC = [wx.MemoryDC(), wx.MemoryDC(), wx.MemoryDC()]
        # map(lambda dc, bmp: dc.SelectObject(bmp), MemDC, self.Bitmaps)

        dc = wx.PaintDC(self)
        for i in range(8):
            for j in range(8):
                dc.DrawBitmap(self.Bitmaps[self.Game[i][j]], j*sz[0], i*sz[1], True)
    
