# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is a from-scratch project to build a quadruped (4-legged) spider robot controlled by a Raspberry Pi 4 (4GB/32GB SD). All robot logic is written in Python. Planned capabilities:

- **Movement/locomotion**: leg control and gait patterns, designed using OOP (object-oriented design — e.g. a `Robot` composed of leg/vision modules rather than flat procedural scripts).
- **Computer vision**: a Raspberry Pi Camera captures frames while the robot walks.
- **AI-driven object recognition**: captured images are sent to the OpenAI API (vision-capable models) to identify and name objects.

The project is in its very early stages — no hardware has been purchased yet, and the codebase currently contains only a stub `main.py` and a `.env` file for secrets.

## Development approach (important context for future work)

The user has minimal background in robotics/electronics and is learning deliberately — they want to understand and write the logic themselves rather than receive ready-made code. Until physical hardware (servos, PCA9685 driver, Pi Camera) is acquired, development proceeds in **simulated layers**:

1. **AI/vision logic** is built and tested first using static test images (instead of live camera capture).
2. **Movement logic** is designed with OOP and initially "simulated" (e.g., logging intended servo actions) rather than driving real hardware, so the control logic can be designed and validated independently of physical components.
3. Real hardware integrations (camera capture via `picamera2`, servo control via a PCA9685 driver over I2C) are meant to be swapped in later **without** restructuring the higher-level decision logic — keep hardware-facing code isolated behind clear interfaces/classes for this reason.

## Secrets

- `.env` holds `OPENAI_API_KEY` and is loaded via `python-dotenv`'s `load_dotenv()`. Never hardcode API keys in source files.
- Note: `load_dotenv()` must run **before** `OpenAI()` is instantiated, since the client reads `OPENAI_API_KEY` from the environment at construction time.

## Key dependencies

- `openai` (v2.x) — official OpenAI Python SDK; used for object-recognition/vision calls.
- `python-dotenv` — loads `.env` into environment variables.

(No build, lint, or test tooling exists yet — there is nothing to run beyond `main.py`.)
