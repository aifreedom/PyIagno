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
from ai import *



class EasyAITest(unittest.TestCase):
    def setUp(self):
        self.ai = easy_ai
        self.Broad = [[-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1,  1,  0, -1, -1, -1],
                      [-1, -1, -1,  0,  1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1]]

    def testValid1(self):
        self.assertEqual(self.ai(self.Broad, 0, 0), (2, 3))

    def testValid2(self):
        self.Broad = [[-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1,  0,  0,  0, -1, -1, -1],
                      [-1, -1, -1,  0,  1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [-1, -1, -1, -1, -1, -1, -1, -1]]
        self.assertEqual(self.ai(self.Broad, 1, 1), (2, 2))


aiSuite = unittest.TestSuite()

easySuite = unittest.makeSuite(EasyAITest, 'test')
aiSuite.addTest(easySuite)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(aiSuite)
