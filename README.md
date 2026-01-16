# bedrock-react-chat

How it works

`User Question → Agent → search_react_docs tool → Bedrock KB (Y3DV2SUPP9) → S3 React Docs → Answer`

The agent will use RAG to search React documentation in S3 and provide answers based on the retrieved content!

## Setup Instructions

### Prerequisites

- **Python 3.10 or higher** (the default macOS Python 3.9 is too old)
- **Homebrew** (for installing Python on macOS)

### 1. Install Python 3.11 (macOS)

```bash
brew install python@3.11
```

### 2. Create and activate virtual environment

```bash
# Create the virtual environment
/opt/homebrew/bin/python3.11 -m venv .venv

# Activate it
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or install strands-agents directly:

```bash
pip install strands-agents
```

### Verify Installation

```bash
python -c "import strands; print('strands-agents installed successfully!')"
```

## Usage

Each time you open a new terminal, activate the virtual environment:

```bash
source .venv/bin/activate
```

Set your AWS profile

```bash
export AWS_PROFILE=AeroAvaPowerUser
```

Your prompt will show `(.venv)` when activated.

Start the agent

```bash
python react-chat-agent.py
```

Then just type your questions! Type quit, exit, q, or press Ctrl+C to stop.

When finished with runtime deactivate

```bash
deactivate
```

**NOTE** This demo requires an AWS SSO connection to an account with a Bedrock Knowledge Base, see `.env_example` for required params.