# Minimax Agent Flow

This diagram captures `MinimaxAgent.select_move()` with alpha-beta pruning.

```mermaid
flowchart TD
    Start([MinimaxAgent.select_move])
    Valid[valid_moves = game.get_valid_moves()]
    OneMove{len(valid_moves) == 1}
    Root[root_player = game.current_player]
    InitBest[best_score = -inf\nbest_move = first valid]
    OrderedRoot[for move in _ordered_moves(valid_moves)]
    Sim[game_copy = game.copy()\ngame_copy.play(move)]
    Recurse[_minimax(game_copy, depth-1,\nalpha=-inf, beta=+inf,\nmaximizing=False, root_player)]
    Better{score > best_score?}
    Update[best_score = score\nbest_move = move]
    End([return best_move])

    Start --> Valid --> OneMove
    OneMove -- yes --> End
    OneMove -- no --> Root --> InitBest --> OrderedRoot --> Sim --> Recurse --> Better
    Better -- yes --> Update --> OrderedRoot
    Better -- no --> OrderedRoot
    OrderedRoot --> End

    subgraph Recursion["_minimax(...)"]
        Term{game.is_game_over?}
        TermScore[_terminal_score]
        DepthZero{depth == 0?}
        Eval[_evaluate_position]
        MaxNode{maximizing?}
        LoopMax[iterate ordered moves\nvalue=max(value, child)\nalpha=max(alpha,value)]
        LoopMin[iterate ordered moves\nvalue=min(value, child)\nbeta=min(beta,value)]
        Prune{alpha >= beta?}
        RetVal([return value])

        Term -- yes --> TermScore --> RetVal
        Term -- no --> DepthZero
        DepthZero -- yes --> Eval --> RetVal
        DepthZero -- no --> MaxNode
        MaxNode -- yes --> LoopMax --> Prune
        MaxNode -- no --> LoopMin --> Prune
        Prune -- yes --> RetVal
        Prune -- no --> RetVal
    end
```
