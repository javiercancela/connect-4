# Game Loop Flow

This flowchart focuses on `Connect4.play()` and how wins/draws are determined.

```mermaid
flowchart TD
    Start([Connect4.play(column)])
    Valid{is_valid_move(column)?}
    Invalid[raise ValueError]
    Drop[Board.drop_piece\nfind drop row\nset grid cell]
    MoveCount[move_count += 1]
    WinCheck[WinChecker.check_win\n4 directions]
    Win{count >= WIN_LENGTH?}
    Draw{move_count == ROWS*COLS?}
    SetWinner[_winner = current_player\n_game_over = True]
    SetDraw[_game_over = True]
    Switch[_current_player = -_current_player]
    ReturnWin[return (True, winner)]
    ReturnDraw[return (True, None)]
    ReturnCont[return (True, None)]

    Start --> Valid
    Valid -- no --> Invalid
    Valid -- yes --> Drop --> MoveCount --> WinCheck --> Win
    Win -- yes --> SetWinner --> ReturnWin
    Win -- no --> Draw
    Draw -- yes --> SetDraw --> ReturnDraw
    Draw -- no --> Switch --> ReturnCont
```
