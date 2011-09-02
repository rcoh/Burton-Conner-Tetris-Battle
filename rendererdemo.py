# rendererdemo.py
# Copyright (C) 2011  Russell Cohen <rcoh@mit.edu>
#
# This file is part of Burton-Conner Tetris Battle.
#
# Burton-Conner Tetris Battle is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Burton-Conner Tetris Battle is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Burton-Conner Tetris Battle.  If not, see
# <http://www.gnu.org/licenses/>.

"""
Draws some circles on the screen then closes.
"""
from renderer import PygameRenderer
p = PygameRenderer()

test_dict = {(0,0):"red", (5,5):"orange", (10,10):"blue"}
p.render_game(test_dict)
