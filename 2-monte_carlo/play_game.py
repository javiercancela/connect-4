from game_engine.game import Game
from model.monte_carlo_agent import MonteCarloAgent

game = Game()
agent = MonteCarloAgent(player_id=2)

def get_humam_move():
  move = input(f"Player {game.get_turn()} (or 'quit' to exit): ")
  if move.lower() == 'quit':
    return None

  try:
    column = int(move)
    if not 0 <= int(column) <= 6:
      print("Invalid move. Please enter a column number between 0 and 6.")
      return -1
  except ValueError:
    print("Invalid input. Please enter a column number between 0 and 6.")
    return -1
  
  return column

while game.get_winner() is None:
  if game.get_turn() == 1:
    move = get_humam_move()
    if move is None:
      break
    elif move == -1:
      continue
  else:
    agent.record_state(game)
    move = agent.choose_action(game)
  game.make_move(move)
  game.print_board()

if game.get_winner() == 0:
  print("It's a tie!")
else: 
  print(f"Player {game.get_winner()} wins!")