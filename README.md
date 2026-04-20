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

   - **Flood Fill Algorithm:** To prevent the AI from trapping itself, it uses a simplified flood_count to "look ahead" and calculate how much empty space is available in a given direction.

   - **Evaluation Function:** The AI scores potential moves based on a weighted formula: <br>
<p align="center">
  <i>Score = Area + AttackBias + WallBias + StraightBonus + Randomness</i>
</p>

   - **Survival Instinct:** It prioritizes moves that maximize reachable space while maintaining a slight bias toward staying near the player to force a "cut-off" maneuver.

---

## Features
  - **Dual Game Modes:** Supports 1 Player vs System (AI-driven) and 2 Player Duel (local multiplayer).

  - **Dynamic AI:** Features a predictive AI that uses flood-fill pathfinding to avoid obstacles and trap the player.

  - **In-Game Instructions:** Includes a "How to Play" screen detailing controls (WASD for P1, Arrows for P2) and game rules.

  - **Visual Polish:** Cinematic neon aesthetics with grid backgrounds, glowing light cycle heads, and particle-based crash effects.

  - **Persistence:** A round-based scoring system that tracks wins across multiple matches until the user returns to the main menu.

---

## Project Structure
The project is organized as a modular script utilizing the Pyxel package for hardware-accelerated 2D graphics and input handling.

➤ **Imports:** Utilizes pyxel for the engine, math and random for physics/AI, and dataclasses for clean data modeling.

➤ **Data Models (@dataclass):** Defines the Bike object, which encapsulates state data like position, direction, color, and player-specific key mappings.

➤ **Game Engine (TronGame):** <br>

   - **Initialization:** Sets up the 240x180 resolution and the 30 FPS update frequency.

   - **Update Loop:** Handles input polling, AI calculations, and collision logic.

   - **Draw Loop:** Manages the rendering of the neon grid, trails, UI overlays, and particle effects.

➤ **Constants:** Centralized configuration for the color palette, grid dimensions, and directional vectors.

---


## Output

**Main Menu**
<img width="1366" height="718" alt="Screenshot (7825)" src="https://github.com/user-attachments/assets/0ab04698-f748-4f36-821e-9e98380ce1d0" />
<br><br>

**Instructions on how to play the game**
<img width="1366" height="718" alt="Screenshot (7826)" src="https://github.com/user-attachments/assets/1e919a3b-9c4e-4461-a96a-e395e5180ad2" />
<br><br>

**Player vs System**
<img width="1366" height="718" alt="Screenshot (7827)" src="https://github.com/user-attachments/assets/d16a0440-daa1-4c57-9581-f3922ef7d8c5" />

<img width="1366" height="718" alt="Screenshot (7828)" src="https://github.com/user-attachments/assets/5e087e77-c9f4-4348-af41-35aa0971cf03" />

<img width="1366" height="718" alt="Screenshot (7835)" src="https://github.com/user-attachments/assets/540429c6-a85b-4281-9237-f55cf2c798d7" />
<br><br>

**Player vs Player**
<img width="1366" height="720" alt="Screenshot (7830)" src="https://github.com/user-attachments/assets/9bf89b65-caf4-48bb-ab8d-8401294c5f36" />

<img width="1366" height="718" alt="Screenshot (7831)" src="https://github.com/user-attachments/assets/0014d569-a260-4aee-8af6-660ee1179015" />

<img width="1366" height="718" alt="Screenshot (7832)" src="https://github.com/user-attachments/assets/486760d5-bffc-4355-898d-6dca89719db3" />

<img width="1366" height="718" alt="Screenshot (7834)" src="https://github.com/user-attachments/assets/ae4b58c5-864a-460f-9613-692d22653f22" />

---

## Demonstration - How the Game Works 
<img width="800" height="421" alt="Tron GIF-refer this" src="https://github.com/user-attachments/assets/581f3da7-6c21-40a6-870b-d52c07ed1ef9" />





