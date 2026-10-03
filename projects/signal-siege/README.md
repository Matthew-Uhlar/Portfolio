# Signal Siege

[![Signal Siege demo](https://raw.githubusercontent.com/Matthew-Uhlar/Portfolio/main/demos/signal-siege-demo.gif)](https://matthew-uhlar.github.io/Portfolio/demos/signal-siege-demo.mp4)

**[Watch the full demo video (MP4)](https://matthew-uhlar.github.io/Portfolio/demos/signal-siege-demo.mp4)** | Gameplay recorded from the real game loop: waves of three enemy types, the upgrade screen between waves, particles and screen shake.

Signal Siege is a wave survival game I built with Python and Pygame as a portfolio project. I wanted something that showed more than just basic movement and collision detection so I focused on writing clean code and organizing everything into reusable classes.

Instead of relying on downloaded assets I generated the visuals directly in code. That keeps the project easy to run while still demonstrating game architecture and programming fundamentals.

## Features

- WASD movement
- Mouse aiming and shooting
- Three enemy types with different behaviors
- Progressive wave system
- Upgrade selection between waves
- Health and shield mechanics
- Core defense objective
- Particle effects
- Screen shake
- Local high score saving
- Object oriented design
- Simple project structure

## Controls

- WASD to move
- Mouse to aim
- Left click to shoot
- Escape to pause
- 1 through 3 to choose upgrades
- R to restart after a game over

## Run

```bash
python -m pip install -r requirements.txt
python main.py
```

## Tech Used

- Python
- Pygame
- JSON
- Object Oriented Programming

If I kept working on this project I would add bosses, animations, sound effects, controller support, more weapons and online leaderboards.