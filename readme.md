# Startup Idea Validator (Capstone Project)

A CLI-based agentic tool that validates startup ideas using simulated market research and "brutally honest" validation logic. It leverages LangGraph for orchestration and can optionally use OpenAI's GPT-4 for deep analysis.

## ✅ Completed Features (Progress Log)

-   **Architecture Compliance**: Verified structure, state, and subgraphs against `docs/ARCHITECTURE.md`.
-   **Automated Testing**: Ran and passed all unit tests (`test_state.py`, `test_research.py`, etc.).
-   **Functional CLI**: Implemented and tested `discover`, `validate`, and `synth` workflows.
-   **Interactive Flow**: Added a guided session mode with step-by-step confirmation.
-   **Session Management**: Implemented persistence and "continue vs. reset" logic.
-   **Real Synthesis**: Integrated OpenAI (GPT-4) for generating detailed reports.
-   **Smart Fallback**: Created a robust fallback system using sector-specific simulated data (AI, Pets, Food) when no API key is present.
-   **Quality Improvements**:
    -   Enhanced `MarketTools` to return realistic, sector-specific data.
    -   Improved `Validator` to flag common tropes ("Uber for X") and vague ideas.
    -   Refined `Synthesis` to produce educational, dynamic reports even in fallback mode.
-   **Report Refinement**: Implemented a "brutal and realistic" VC-style report format with specific sections (Executive Summary, 5 Reasons It Could Work/Fail, etc.).
-   **Documentation**: Updated README with usage instructions and feature details.

## 🚀 Features

-   **Interactive Session**: Guides you step-by-step through Research, Validation, and Synthesis.
-   **Brutal Validation**: Provides a realistic, VC-style critique of your idea, flagging common tropes and risks.
-   **Smart Fallback**: Works even without an API key by using sector-specific simulated data (AI, Pets, Food, etc.) and dynamic templates.
-   **Deep Analysis (Optional)**: Connects to OpenAI (GPT-4) for a comprehensive investment memo if an API key is provided.
-   **Session Persistence**: Saves your progress so you can resume later.

## 🛠️ Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd capstone-template-mayank220
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment (Optional)**:
    -   Create a `.env` file in the root directory.
    -   Add your OpenAI API key for real AI generation:
        ```env
        OPENAI_API_KEY=sk-your-key-here
        ```
    -   *Note: The tool works fully without a key, using smart simulated data.*

## 🏃 Usage

### Interactive Mode (Recommended)
Simply run the main script to start a guided session:
```bash
python -m graph.main
```
Follow the prompts to enter your idea, review research, and generate a report.

### Batch Mode
Run specific tasks directly via command line arguments:

-   **Discover (Research + Validate)**:
    ```bash
    python -m graph.main --idea "Uber for dog walking" --task discover
    ```

-   **Validate (Re-run validation logic)**:
    ```bash
    python -m graph.main --task validate
    ```

-   **Synth (Generate Report)**:
    ```bash
    python -m graph.main --task synth
    ```

-   **Reset Session**:
    ```bash
    python -m graph.main --reset
    ```

## 📊 Output Format

The tool generates a detailed **Validation Report** including:
-   **Executive Summary**: Viability assessment.
-   **Market Analysis**: Trends, competitors, and reality checks.
-   **Risks & Challenges**: Brutal assessment of potential failure points.
-   **Investor Snapshot**: A one-page summary for pitching.
-   **5 Reasons It Could Work / 5 Reasons It May Not Work**: Balanced, realistic critique.

## 🏗️ Architecture

-   **`graph/main.py`**: Entry point and interactive session manager.
-   **`graph/state.py`**: Manages global state and persistence (JSON).
-   **`graph/research.py`**: Simulates market research using `tools/market_tools.py`.
-   **`graph/validator.py`**: Scores ideas based on evidence and heuristics.
-   **`graph/synth.py`**: Generates the final report (LLM or Smart Template).

## 🧪 Testing

Run the test suite to verify functionality:
```bash
python -m unittest discover tests
```