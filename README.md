# DAX LLM Backend

A FastAPI-based backend service that provides LLM-powered DAX query assistance using Anthropic's API.

## Prerequisites

- Python 3.12+
- Environment variables setup (see Configuration section)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the root directory with the following variables:

```env
ANTHROPIC_API_KEY=your_api_key_here
# Add any other required environment variables
```

## Running the Application

### Local Development
```bash
uvicorn src.main:app --reload --host 127.0.0.1
```

### Production Deployment (Azure)
Configure the app service with `startup.sh` as the startup command.

## Project Structure

### Data
Various scripts utilized to pull DAX function docs, overview of the dax language, etc - all stored in the src/data folder.

### LLM
- anthropic_helpers.py: Making API calls and basic data input/output formatting.
- embeddings.py: Simple rag lookup model to add function information to context.
- schemas.py: Expected API input schema.
- system_prompt.py: Building up the system prompt, combination of defined text and appended dynamic values.

### Evaluation
All stored in src/evaluate folder - allows for running a test suite where a given question and expected answer can be tested against an LLM DAX query result.

### Fast API Sepcifics
Mostly in startup folder - setting up app, routes, throttling, etc.