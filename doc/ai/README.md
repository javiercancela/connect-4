# Connect-4 Engine Diagrams

The diagrams in this folder describe the core engine, agents, and CLI scripts. They are intended to give an LLM full context on how the program works.

- `architecture-overview.md`: System-level relationships across engine, agents, and CLI scripts.
- `class-diagram.md`: Class and method shape of the core engine and agents.
- `gameplay-sequence.md`: Sequence of a human vs agent game loop (`play.py`).
- `game-loop-flow.md`: Internal `Connect4.play()` flow and win/draw handling.
- `heuristic-agent-flow.md`: Decision flow for `HeuristicAgent`.
- `board-win-logic.md`: Board representation and win-checking logic.
