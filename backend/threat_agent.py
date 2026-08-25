import json
from anthropic import Anthropic
import os

client = Anthropic()

SYSTEM_PROMPT = """You are an expert threat modeling specialist with deep knowledge of cybersecurity, application architecture, and risk assessment.

Your role is to help users perform comprehensive threat modeling on their web applications using industry-standard frameworks.

You will:
1. Ask clarifying questions about the application architecture, data flows, authentication mechanisms, and technologies used
2. Understand the user's threat modeling framework preference (STRIDE, PASTA, or hybrid)
3. Analyze the provided information (code, documentation, diagrams, or descriptions)
4. Identify potential threats, vulnerabilities, and risks
5. Provide severity ratings (Critical, High, Medium, Low)
6. Suggest mitigation strategies for each identified threat
7. Generate a comprehensive, structured threat modeling report

When the user has provided enough information, generate a structured JSON threat report with the following format:
{
  "application_name": "...",
  "framework": "STRIDE|PASTA|HYBRID",
  "summary": "Executive summary of threats identified",
  "threats": [
    {
      "id": "T001",
      "title": "Threat title",
      "description": "Detailed description",
      "category": "STRIDE/PASTA category",
      "severity": "Critical|High|Medium|Low",
      "affected_component": "...",
      "attack_vector": "How this threat could be exploited",
      "potential_impact": "What would happen if exploited",
      "mitigation": "Recommended mitigation strategy",
      "validation": "How to verify the threat is mitigated"
    }
  ],
  "data_flows": [
    {
      "source": "component A",
      "destination": "component B",
      "data_type": "type of data",
      "protocol": "protocol used",
      "risks": ["risk1", "risk2"]
    }
  ],
  "recommendations": [
    "High-priority recommendation 1",
    "High-priority recommendation 2"
  ]
}

Ask follow-up questions if needed to understand the application better. Be thorough but conversational."""

def create_threat_modeling_agent():
    """Create and return a threat modeling agent."""
    return ThreatModelingAgent()

class ThreatModelingAgent:
    def __init__(self):
        self.conversation_history = []
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment variables")

    def chat(self, user_message: str) -> str:
        """Send a message and get a response from the threat modeling agent."""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        response = client.messages.create(
            model="claude-opus-5",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=self.conversation_history
        )

        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def get_conversation_history(self) -> list:
        """Return the conversation history."""
        return self.conversation_history

    def parse_threat_report(self, content: str) -> dict:
        """Extract JSON threat report from assistant response."""
        try:
            # Try to find JSON in the response
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end > start:
                json_str = content[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        return None
