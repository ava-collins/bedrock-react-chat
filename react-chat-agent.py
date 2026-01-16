import os
import boto3
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models import BedrockModel

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Create Bedrock Agent Runtime client for knowledge base retrieval
bedrock_agent_client = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)


@tool
def search_react_docs(query: str) -> str:
    """Search the React documentation knowledge base for relevant information.
    
    Args:
        query: The search query to find relevant React documentation.
    
    Returns:
        Relevant documentation excerpts from the knowledge base.
    """
    try:
        response = bedrock_agent_client.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={"text": query},
            retrievalConfiguration={
                "vectorSearchConfiguration": {
                    "numberOfResults": 5
                }
            }
        )
        
        # Extract and format the results
        results = []
        for item in response.get("retrievalResults", []):
            content = item.get("content", {}).get("text", "")
            source = item.get("location", {}).get("s3Location", {}).get("uri", "unknown")
            score = item.get("score", 0)
            results.append(f"Source: {source}\nRelevance: {score:.2f}\n\n{content}\n")
        
        if results:
            return "\n---\n".join(results)
        else:
            return "No relevant documentation found."
            
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"


# Use Amazon Nova Lite for RAG
model = BedrockModel(
    model_id="amazon.nova-lite-v1:0",
    region_name=AWS_REGION,
)

react_chat_agent = Agent(
    model=model,
    system_prompt="""You are a helpful assistant that answers questions about the React framework.

When answering React questions, ALWAYS use the search_react_docs tool first to find relevant information from the official documentation.
Base your answers on the retrieved documentation and cite the sources when possible.""",
    tools=[search_react_docs],
)

if __name__ == "__main__":
    print("React Documentation Assistant")
    print("Ask questions about React (type 'quit' or 'exit' to stop)")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ("quit", "exit", "q"):
                print("Goodbye!")
                break
            
            print("\nAssistant: ", end="")
            react_chat_agent(user_input)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
