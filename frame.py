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

    # =======================================================
    # Constructor
    # =======================================================
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER
                                                  | wx.MINIMIZE_BOX
                                                  | wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, *args, **kwds)
        self.frame_statusbar = self.CreateStatusBar(2, 0)

        self.Bitmaps = [wx.Bitmap("image/dark.png", wx.BITMAP_TYPE_ANY),
                        wx.Bitmap("image/light.png", wx.BITMAP_TYPE_ANY),
                        wx.Bitmap("image/blank.png", wx.BITMAP_TYPE_ANY)]

        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_UP, self.OnClick)
        
        self.Game = IagnoGame(ai=easy_ai)
        self.__set_properties()


    def __set_properties(self):
        self.SetTitle("PyIango")
        self.SetSize((320, 346))
        self.frame_statusbar.SetStatusWidths([-4, -6])
        self.frame_statusbar.SetStatusText(IagnoFrame.PlayerStr[self.Game.Player], 0)
        self.frame_statusbar.SetStatusText("Dard: %d Light: %d" % (self.Game.DarkCnt, self.Game.LightCnt), 1)
        # frame_statusbar_fields = ["Dark's Move", "Dark: 2 Light: 2"]
        # for i in range(len(frame_statusbar_fields)):
        #     self.frame_statusbar.SetStatusText(frame_statusbar_fields[i], i)

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
                self.frame_statusbar.SetStatusText('Invalid move.', 0)
                raise 'AI Error'
            else:
                for yy, xx in l:
                    self.__Draw(aiPlayer, (xx, yy))
                    self.frame_statusbar.SetStatusText(IagnoFrame.PlayerStr[self.Game.Player], 0)
                self.frame_statusbar.SetStatusText("Dard: %d Light: %d" % (self.Game.DarkCnt, self.Game.LightCnt), 1)
                
    # =======================================================
    # Event handlers
    # =======================================================
    def OnClick(self, evt):
        y, x = evt.GetPosition()

        player = self.Game.Player
        try:
            l = self.Game.Set((x/40, y/40))
        except self.Game.InvalidPositionException:
            self.frame_statusbar.SetStatusText('Invalid move.', 0)
        else:
            for yy, xx in l:
                self.__Draw(player, (xx, yy))
            self.frame_statusbar.SetStatusText(IagnoFrame.PlayerStr[self.Game.Player], 0)
            self.frame_statusbar.SetStatusText("Dard: %d Light: %d" % (self.Game.DarkCnt, self.Game.LightCnt), 1)

            # if is human-AI game
            if not self.Game.IsEnd and self.Game.ai:
                self.__AIMove(not player)

    def OnPaint(self, evt):
        sz = (40, 40)
        MemDC = [wx.MemoryDC(), wx.MemoryDC(), wx.MemoryDC()]
        map(lambda dc, bmp: dc.SelectObject(bmp), MemDC, self.Bitmaps)

        dc = wx.PaintDC(self)
        for i in range(8):
            for j in range(8):
                dc.DrawBitmap(self.Bitmaps[self.Game[i][j]], j*sz[0], i*sz[1], True)



# end of class IagnoFrame
