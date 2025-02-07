class MoveSelector:

  def __init__(self):

    self.best_value = float("-inf")
    self.best_moves = []

  def process_move(self, predicted_move_value):
    """ 
    Update best move based on predicted value.
    The best move is a list in case there are multiple moves with the same value.
    """
    if predicted_move_value > self.best_value:
        self.best_value = predicted_move_value
        self.best_moves = [predicted_move_value]

    elif predicted_move_value == self.best_value:
        self.best_moves.append(predicted_move_value)

  def get_best_moves(self):

    return self.best_moves