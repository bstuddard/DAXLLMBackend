### Running the backend
Local (first install requirements.txt and creating .env file with ANTHROPIC_API_KEY entry):
uvicorn src.main:app --reload --host 127.0.0.1

Azure/hosted:
Put 'startup.sh' in the startup command under app service configuration.

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