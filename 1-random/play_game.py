from ..game_engine.game import Game


game = Game()

while True:
  move = input(f"Player {game.get_turn()} (or 'quit' to exit): ")
  if move.lower() == 'quit':
    break
  try:
    column = int(move)
    if not 0 <= int(column) <= 6:
      print("Invalid move. Please enter a column number between 0 and 6.")
      continue
    game.make_move(column)
    game.print_board()
    if game.get_winner() is not None:
      if game.get_winner() == 'Tie':
        print("It's a tie!")
      else: 
        print(f"Player {game.get_winner()} wins!")
      break
  except ValueError:
    print("Invalid input. Please enter a column number between 0 and 6.")