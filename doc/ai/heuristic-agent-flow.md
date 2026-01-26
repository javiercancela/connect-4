# Heuristic Agent Flow

This diagram captures the decision process of `HeuristicAgent.select_move()`.

```mermaid
flowchart TD
    HStart([HeuristicAgent.select_move])
    ValidMoves[valid_moves = game.get_valid_moves()]
    OnlyOne{len(valid_moves) == 1}
    WinMoves[Find winning moves\n_is_winning_move for current player]
    UseWinMoves{winning_moves?}
    BlockMoves[Find opponent winning moves\n_is_winning_move for opponent]
    OneBlock{len(opponent_winning_moves) == 1}
    SafeMoves[Filter moves that\nallow opponent win]
    NoSafe{safe_moves empty?}
    Central[_pick_most_central\n(min distance to center)]
    Choose([Return choice])

    HStart --> ValidMoves --> OnlyOne
    OnlyOne -- yes --> Choose
    OnlyOne -- no --> WinMoves --> UseWinMoves
    UseWinMoves -- yes --> Central --> Choose
    UseWinMoves -- no --> BlockMoves --> OneBlock
    OneBlock -- yes --> Choose
    OneBlock -- no --> SafeMoves --> NoSafe
    NoSafe -- yes --> Central --> Choose
    NoSafe -- no --> Central --> Choose
```
