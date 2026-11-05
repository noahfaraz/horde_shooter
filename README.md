# Horde Shooter

A small top-down arcade shooter built with Python and Pygame. Dots come at you, you shoot the dots, and the dots keep coming. How long can you last?

It's a simple game, but it has a menu, sound, controller support and a few enemy types.

## How to Play

Stay alive, shoot as many enemies as you can, and grab green health pickups when they appear.

| Thing | What it does |
|-------|--------------|
| 🔴 Red enemy | Dies in 1 hit, worth 1 point. Touching one costs you a life. |
| 🔵 Blue enemy | Bigger and slower, takes 3 hits, worth 5 points. **Touching one is instant game over.** |
| 🟢 Green pickup | Restores 1 life (max 5). Appears every few seconds. |

You start with 3 lives. Enemies spawn in groups of 2-4 every couple of seconds, and a big blue one shows up every 10 seconds. Your bullets only fire upward, so line up your shots.

## Controls

**Keyboard**

| Key | Action |
|-----|--------|
| `W` `A` `S` `D` | Move |
| `Space` | Shoot (right side of ship) |
| `O` | Shoot (left side of ship) |
| `Enter` | Select in menu / restart after game over |
| `Space` (on game over) | Back to main menu |

**Controller**

| Input | Action |
|-------|--------|
| Left stick | Move |
| `A` / `B` buttons | Shoot |
| D-pad | Navigate menu |
| `X` (on game over) | Restart |

## Running It

You'll need Python 3 and Pygame.

```bash
pip install pygame
python game.py
```

Run it from the project's root folder so the game can find the `assets/` folder.

## Project Structure

```
horde_shooter/
├── game.py          # the whole game
├── assets/          # images, fonts and sound
├── best_model/      # saved trained model
└── best_model.zip   # same model, zipped
```

## Notes

- The window is 500x500.
- A random soundtrack plays each time you launch the game.
- Plugging in a controller makes the player and enemies a bit faster.
- The "Settings" menu option is a placeholder for now.

## Ideas for Later

- Working settings menu
- Different weapons or power-ups
- High score saving
- More enemy types
