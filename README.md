# Tron Light Cycle Battle Game

## Description
A Python-based arcade game developed using the Pyxel retro game engine. It simulates the high-stakes "Light Cycle" battles from the 1982 film TRON, utilizing grid-based movement, collision detection, and a custom AI algorithm to create a fast-paced, neon-drenched competitive experience.

---

## How the Code Works

The TRON Light Cycle Battle is built on a frame-based update loop. The game translates a 2D grid logic into a visual arena where players leave lethal trails behind them.

➤ **Core Architecture and Logic** <br>
The application is structured around a central game class that manages the state machine (menu, play, and game over) and the rendering pipeline.

   - **Grid System:** The arena is represented by a 2D list (grid). Each cell stores the color of the trail occupying it. This allows for _**O(1)**_(i.e. Constant Time) collision lookups—the game simply checks if the next coordinate in the grid is already occupied.

   - **Collision Engine:** In every frame, the system calculates the "next position" for all active bikes. A collision is triggered if a bike hits the boundary, an existing trail, or if two bikes move into the same cell simultaneously.

   - **Particle System:** Upon a collision, a "sparkle" system generates an explosion of pixels. Each particle has its own velocity, gravity-free trajectory, and lifespan, providing a cinematic "de-resolution" effect.
     

➤ **AI and Decision Making** <br>
For the "System" opponent, the code implements a heuristic-based AI:

**Flood Fill Algorithm:** To prevent the AI from trapping itself, it uses a simplified flood_count to "look ahead" and calculate how much empty space is available in a given direction.

**Evaluation Function:** The AI scores potential moves based on a weighted formula:
               _**Score = Area + AttackBias + WallBias + StraightBonus + Randomness**_

Survival Instinct: It prioritizes moves that maximize reachable space while maintaining a slight bias toward staying near the player to force a "cut-off" maneuver.
