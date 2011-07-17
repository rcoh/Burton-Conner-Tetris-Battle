class Renderer(object):
  """
  renderBoard
  @param gameBoard -- dictionary of tuples of location (x,y), 0 indexed from
  the top left of the board.
  @param boardIndex -- 0 for the left board, 1 for the right board.
  """
  def renderBoard(gameBoard, boardIndex):
    raise NotImplementedError
