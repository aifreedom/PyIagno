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

import unittest
import sys
sys.path.append('..')
from game import IagnoGame



class InitGameTest(unittest.TestCase):
    def setUp(self):
        self.Game = IagnoGame()

    def testLength1(self):
        assert len(self.Game) == 0, 'Initial length not zero'

    def testInitOutline(self):
        assert self.Game[3][3] == IagnoGame.BRD_LIGHT, '(3, 3) not light'
        assert self.Game[4][4] == IagnoGame.BRD_LIGHT, '(4, 4) not light'
        assert self.Game[3][4] == IagnoGame.BRD_DARK, '(3, 4) not dark'
        assert self.Game[4][3] == IagnoGame.BRD_DARK, '(4, 3) not dark'

    def testInitPlayerColor(self):
        """Test if the first player is Dark."""
        assert self.Game.Player == IagnoGame.BRD_DARK

    def testValidSet1(self):
        """Set a dark piece at pos (2, 3)."""
        self.Game.Set((2, 3))
        spj = ((2, 3), (3, 3), (3, 4), (4, 3), (4, 4))
        for i in range(8):
            for j in range(8):
                if not (i, j) in spj:
                    assert self.Game[i][j] == IagnoGame.BRD_BLANK, \
                           '(%d, %d) is not blank' % (i, j)
        assert self.Game[2][3] == IagnoGame.BRD_DARK
        assert self.Game[3][3] == IagnoGame.BRD_DARK
        assert self.Game[4][4] == IagnoGame.BRD_LIGHT
        assert self.Game[3][4] == IagnoGame.BRD_DARK
        assert self.Game[4][3] == IagnoGame.BRD_DARK

    def testValidSet2(self):
        """Set a dark piece at pos (3, 2)."""
        self.Game.Set((3, 2))
        spj = ((3, 2), (3, 3), (3, 4), (4, 3), (4, 4))
        for i in range(8):
            for j in range(8):
                if not (i, j) in spj:
                    assert self.Game[i][j] == IagnoGame.BRD_BLANK, \
                           '(%d, %d) is not blank' % (i, j)
        assert self.Game[3][2] == IagnoGame.BRD_DARK
        assert self.Game[3][3] == IagnoGame.BRD_DARK
        assert self.Game[4][4] == IagnoGame.BRD_LIGHT
        assert self.Game[3][4] == IagnoGame.BRD_DARK
        assert self.Game[4][3] == IagnoGame.BRD_DARK

    def testValidSet3(self):
        """Set a dark piece at pos (4, 5)."""
        self.Game.Set((4, 5))
        spj = ((3, 3), (3, 4), (4, 3), (4, 4), (4, 5))
        for i in range(8):
            for j in range(8):
                if not (i, j) in spj:
                    assert self.Game[i][j] == IagnoGame.BRD_BLANK, \
                           '(%d, %d) is not blank' % (i, j)
        assert self.Game[4][5] == IagnoGame.BRD_DARK
        assert self.Game[3][3] == IagnoGame.BRD_LIGHT
        assert self.Game[4][4] == IagnoGame.BRD_DARK
        assert self.Game[3][4] == IagnoGame.BRD_DARK
        assert self.Game[4][3] == IagnoGame.BRD_DARK

    def testValidSet4(self):
        """Set a dark piece at pos (5, 4)."""
        self.Game.Set((5, 4))
        spj = ((3, 3), (3, 4), (4, 3), (4, 4), (5, 4))
        for i in range(8):
            for j in range(8):
                if not (i, j) in spj:
                    assert self.Game[i][j] == IagnoGame.BRD_BLANK, \
                           '(%d, %d) is not blank' % (i, j)
        assert self.Game[5][4] == IagnoGame.BRD_DARK
        assert self.Game[3][3] == IagnoGame.BRD_LIGHT
        assert self.Game[4][4] == IagnoGame.BRD_DARK
        assert self.Game[3][4] == IagnoGame.BRD_DARK
        assert self.Game[4][3] == IagnoGame.BRD_DARK


    def testInvalidSet1(self):
        """Set a dark piece at pos (0, 0)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (0, 0))
        
    def testInvalidSet2(self):
        """Set a dark piece at pos (7, 7)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (7, 7))
        
    def testInvalidSet3(self):
        """Set a dark piece at pos (0, 7)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (0, 7))
        
    def testInvalidSet4(self):
        """Set a dark piece at pos (7, 0)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (7, 0))
        
    def testInvalidSet5(self):
        """Set a dark piece at pos (2, 2)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (2, 2))

    def testInvalidSet6(self):
        """Set a dark piece at pos (5, 5)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (5, 5))

    def testInvalidSet7(self):
        """Set a dark piece at pos (4, 2)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (4, 2))

    def testInvalidSet8(self):
        """Set a dark piece at pos (3, 5)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (3, 5))

    def testInvalidSet9(self):
        """Set a dark piece at pos (2, 4)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (2, 4))

    def testInvalidSet10(self):
        """Set a dark piece at pos (5, 3)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (5, 3))

    def testInvalidSet11(self):
        """Set a dark piece at pos (2, 4)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (1, 3))

    def testInvalidSet12(self):
        """Set a dark piece at pos (0, 2)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (0, 2))

    def testInvalidSet13(self):
        """Set a dark piece at pos (2, 0)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (2, 0))

    def testInvalidSet14(self):
        """Set a dark piece at pos (3, 7)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (3, 7))

    def testInvalidSet15(self):
        """Set a dark piece at pos (7, 4)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (7, 4))

    def testInvalidSet16(self):
        """Set a dark piece at pos (2, 4)."""
        self.assertRaises(IagnoGame.InvalidPositionException,
                          self.Game.Set, (2, 4))

        
gameSuite = unittest.TestSuite()

# Test initial outline
initSuite = unittest.makeSuite(InitGameTest, 'test')
gameSuite.addTest(initSuite)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(gameSuite)
