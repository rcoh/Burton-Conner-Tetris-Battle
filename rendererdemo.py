"""
Draws some circles on the screen then closes.
"""
from renderer import PygameRenderer
p = PygameRenderer()

test_dict = {(0,0):"red", (5,5):"orange", (10,10):"blue"}
p.render_game(test_dict)
