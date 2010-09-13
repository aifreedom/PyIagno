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

import copy

class IagnoGame(object):
    """
    Implements the Reversi game.
    """
    
    # Enumerator of colors on board
    BRD_BLANK, BRD_DARK, BRD_LIGHT = range(-1, 2)

    # Directions to move
    __dir = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1),
             (1, -1), (1, 0), (1, 1))

    # =======================================================
    # Exceptions
    # =======================================================
    class NotFoundException(Exception): pass
    class InvalidPositionException(Exception): pass

    # =======================================================
    # Constructor
    # =======================================================
    def __init__(self,
                 ai = None,
                 init = [[-1, -1, -1, -1, -1, -1, -1, -1],
                         [-1, -1, -1, -1, -1, -1, -1, -1],
                         [-1, -1, -1, -1, -1, -1, -1, -1],
                         [-1, -1, -1,  1,  0, -1, -1, -1],
                         [-1, -1, -1,  0,  1, -1, -1, -1],
                         [-1, -1, -1, -1, -1, -1, -1, -1],
                         [-1, -1, -1, -1, -1, -1, -1, -1],
                         [-1, -1, -1, -1, -1, -1, -1, -1]]):
        """
        Initialize a new game.
        param init: the initial outline of the game.
        """
        self.__Board = copy.deepcopy(init) # set the initial board
        
        self.__Len = 0                 # steps been taken

        self.__Valid = []              # valid place to set
        self.__Valid.append([])
        self.__Valid.append([])
        
        self.__Player = self.BRD_DARK  # initial player: Dark
        self.__End = False

        self.__Maintain()

    # =======================================================
    # Public methods
    # =======================================================
    def Set(self, pos):
        """
        Sets a piece at pos for player.
        Returns the changed grids.
        If pos is not valid for player, raises InvalidPositionException.
        """
        player = self.__Player
        if pos in self.GetValid(player):
            x, y = pos
            self.__Board[x][y] = player
            self.__Len += 1
            self.__Player = int(not self.__Player)
            return self.__Update(pos)
        else:
            raise self.InvalidPositionException
        
    def GetValid(self, player):
        """
        Returns the valid posiitions for player.
        """
        return tuple(self.__Valid[player])

    def GetPlayer(self):
        """
        Returns the color of the current player.
        """
        return self.__Player

    def IsEnd(self):
        """
        Returns if the game is end.
        """
        return self.__End

    # =======================================================
    # Overloaded methods
    # =======================================================
    def __len__(self):
        """
        The length of a game is the current number of steps
        """
        return self.__Len

    def __getitem__(self, idx):
        """
        Access to the board by index
        """
        return self.__Board[idx][:]


    # =======================================================
    # Private methods
    # =======================================================
    def __Update(self, pos):
        """
        Update the board, after put a piece on pos.
        Returns a tuple containing the positions that was updated.
        """
        x, y = pos
        player = self[x][y]
        ret = [pos]
        for d in self.__dir:
            try:
                li = self.__Find(player, pos, d)
            except:
                pass
            else:
                for x, y in li:
                    self.__Board[x][y] = int(not self.__Board[x][y])
                ret += li
        self.__Maintain()
        return tuple(ret)

    def __Find(self, color, pos, d):
        """
        Find the consecutive grids which have different color with the color of pos in direction d.
        Returns the tuple of founded positons.
        If not found, raises NotFoundException.
        """
        x, y = pos
        dx, dy = d
        ret = []
        x += dx
        y += dy
        while self[x][y] != color:
            if (not (x in range(8) and y in range(8))
                or self[x][y] == self.BRD_BLANK):
                break
            ret.append((x, y))
            x += dx
            y += dy
        else:
            if ret != []:
                return tuple(ret)
        raise self.NotFoundException

    def __Maintain(self):
        """
        Maintains the valid positions for each player.
        """
        self.__Valid[0] = []
        self.__Valid[1] = []
        for pos in [(x, y) for x in range(8) for y in range(8)]:
            x, y = pos
            if self[x][y] == self.BRD_BLANK:
                for color in range(2):
                    for d in self.__dir:
                        try:
                            self.__Find(color, pos, d)
                        except:
                            pass
                        else:
                            self.__Valid[color].append(pos)
                            break
        if self.__Valid[0] == [] and self.__Valid[1] == []:
            self.__End = True

    # =======================================================
    # For debug only
    # =======================================================
    def Output(self, msg=''):
        """
        For debug only, print the current board.
        """
        print 'PyIagno Debug:'
        print msg
        for i in self.__Board:
            for j in i:
                print j,
            print

# end of class IagnoGame
