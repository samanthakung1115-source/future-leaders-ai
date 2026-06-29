
# Future Leaders AI v1.0 RC1 Architecture

## Purpose

RC1 refactors the prototype into a maintainable product structure.

## Single App Entry

- `app.py`

## Main Modules

- `src/core`: shared data models and settings
- `src/discovery`: candidate loading and ranking
- `src/portfolio`: STS portfolio loading and warnings
- `src/decision`: action plan generation
- `src/services`: Samantha Daily Brief orchestration
- `src/ui`: Streamlit dashboard
- `src/utils`: shared helpers

## Data Flow

Future Leaders CSV
+
STS Portfolio CSV
->
BriefService
->
Samantha Daily Brief
->
Streamlit Dashboard
