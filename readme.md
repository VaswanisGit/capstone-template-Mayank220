# Startup Idea Validator - Capstone Project

This project is a command-line interface (CLI) tool designed to validate startup concepts through simulated market research and automated analysis. It utilizes a graph-based orchestration framework (LangGraph) to manage the validation workflow, which includes research, validation, and report synthesis.

## Project Progress and Implemented Features

The following features have been implemented and verified as part of the capstone requirements:

*   **Architecture Compliance**: The project structure, state management, and subgraph components have been verified against the `docs/ARCHITECTURE.md` specification.
*   **Automated Testing**: Unit tests for state management, research logic, and main execution flow have been implemented and passed.
*   **Functional CLI**: The tool supports three distinct operational modes: `discover`, `validate`, and `synth`.
*   **Interactive Session**: A guided user interface was developed to lead the user through the validation process step-by-step.
*   **Session Persistence**: The system saves the validation state to a local JSON file, allowing users to pause and resume their sessions.
*   **Real Synthesis Integration**: The application is integrated with OpenAI's GPT-4 to generate detailed investment memos (requires an API key).
*   **Fallback Mechanism**: A robust fallback system was implemented to generate useful reports using sector-specific simulated data (e.g., for AI, Pet Care, Food Tech) when no API key is provided.
*   **Quality Enhancements**:
    *   The market research module returns sector-specific data rather than generic placeholders.
    *   The validation logic includes heuristics to flag common derivative ideas (e.g., "Uber for X") and vague descriptions.
    *   The reporting module produces educational and dynamic outputs even in fallback mode.
*   **Report Formatting**: The final output follows a structured Venture Capital style format, including an Executive Summary, Market Analysis, Competitive Landscape, and a "Brutal Reality Check" section.

## System Features

*   **Interactive Mode**: Guides the user through the entire pipeline: Research -> Validation -> Synthesis.
*   **Validation Logic**: Applies critical analysis to the startup idea, identifying potential risks and market saturation.
*   **Smart Fallback**: Ensures the tool remains functional for demonstration purposes without external dependencies.
*   **Deep Analysis**: Optional integration with Large Language Models for comprehensive report generation.
*   **State Management**: Persists data locally to `data/state.json`.

## Setup Instructions

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd capstone-template-mayank220
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration (Optional)**:
    To enable real-time AI generation, create a `.env` file in the root directory and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your-key-here
    ```
    *Note: The application functions fully without this key using the simulated data module.*

## Usage Guide

### Interactive Mode
To start a guided session, run the main module without arguments:
```bash
python -m graph.main
```

### Batch Mode
The tool can also be operated via command-line arguments for specific tasks:

*   **Discover Phase** (Runs Research and Validation):
    ```bash
    python -m graph.main --idea "Uber for dog walking" --task discover
    ```

*   **Validation Phase** (Re-runs validation logic on existing state):
    ```bash
    python -m graph.main --task validate
    ```

*   **Synthesis Phase** (Generates the final report):
    ```bash
    python -m graph.main --task synth
    ```

*   **Reset Session**:
    ```bash
    python -m graph.main --reset
    ```

## Output Structure

The generated Validation Report includes the following sections:

1.  **Executive Summary**: A high-level assessment of the idea's viability.
2.  **Market Analysis**: Data regarding market size, trends, and growth potential.
3.  **Risks & Challenges**: A critical evaluation of potential failure points.
4.  **Investor Snapshot**: A one-page summary suitable for pitch decks.
5.  **Critical Analysis**: Five reasons the idea could succeed and five reasons it might fail.

## System Architecture

The codebase is organized as follows:

*   `graph/main.py`: Entry point and session manager.
*   `graph/state.py`: Defines the global state schema and handles JSON persistence.
*   `graph/research.py`: Implements the research subgraph using `tools/market_tools.py`.
*   `graph/validator.py`: Contains the scoring logic and heuristic checks.
*   `graph/synth.py`: Handles the generation of the final report.

## Testing

To execute the unit test suite, run:
```bash
python -m unittest discover tests
```