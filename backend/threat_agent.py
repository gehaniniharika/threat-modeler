import json
from anthropic import Anthropic
import os
from frameworks import get_framework_prompt

INITIAL_SYSTEM_PROMPT = """You are an expert threat modeling specialist with deep knowledge of cybersecurity, application architecture, and risk assessment.

Your role is to help users perform comprehensive threat modeling on their web applications.

Start by asking clarifying questions about:
1. Application type and purpose
2. Architecture and main components
3. Data flows and external integrations
4. Authentication and authorization mechanisms
5. Technologies and frameworks used

After gathering enough information, ask the user to choose their preferred threat modeling framework:
- STRIDE: Focus on threat categories (Spoofing, Tampering, etc.)
- PASTA: Follow attack simulation process and stages
- PHANTOM-B: Analyze behavioral anomalies and monitoring

Be conversational and thorough. Gather information naturally through dialogue."""

def get_report_system_prompt(framework: str) -> str:
    """Get framework-specific system prompt for report generation"""
    base_prompt = """You are an expert threat modeling specialist. Generate a comprehensive threat report."""
    framework_prompt = get_framework_prompt(framework)

    return base_prompt + "\n\n" + framework_prompt + """

When ready to generate the report, output a JSON with this structure:
{
  "application_name": "...",
  "framework": "STRIDE|PASTA|PHANTOM-B|HYBRID",
  "summary": "Executive summary of threats identified",
  "threats": [
    {
      "id": "T001",
      "title": "Threat title",
      "description": "Detailed description",
      "category": "Framework-specific category",
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
  "recommendations": ["Recommendation 1", "Recommendation 2"]
}"""

def create_threat_modeling_agent(framework: str = None):
    """Create and return a threat modeling agent."""
    return ThreatModelingAgent(framework=framework)

class ThreatModelingAgent:
    def __init__(self, framework: str = None):
        self.conversation_history = []
        self.framework = framework
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment variables")
        self.client = Anthropic(api_key=self.api_key)

    def chat(self, user_message: str) -> str:
        """Send a message and get a response from the threat modeling agent."""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Use framework-specific prompt if framework is set, otherwise use initial prompt
        system_prompt = get_report_system_prompt(self.framework) if self.framework else INITIAL_SYSTEM_PROMPT

        response = self.client.messages.create(
            model="claude-opus-5",
            max_tokens=2000,
            system=system_prompt,
            messages=self.conversation_history
        )

        # Extract text from response, handling thinking blocks
        assistant_message = ""
        for block in response.content:
            if hasattr(block, 'text'):
                assistant_message += block.text
            elif hasattr(block, 'thinking'):
                # Skip thinking blocks, only include the final text response
                continue

        if not assistant_message:
            assistant_message = "I'm processing your request. Please continue."

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
