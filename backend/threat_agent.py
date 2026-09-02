import json
from anthropic import Anthropic
import os
from frameworks import get_framework_prompt

INITIAL_SYSTEM_PROMPT = """Help users with threat modeling. Ask about:
1. App type and purpose
2. Architecture/components
3. Data flows
4. Auth mechanisms
5. Technologies used

Then ask which framework: STRIDE, PASTA, or PHANTOM-B.
Be concise and conversational."""

def get_report_system_prompt(framework: str) -> str:
    """Get framework-specific system prompt for report generation"""
    framework_prompt = get_framework_prompt(framework)

    return framework_prompt + """

CRITICAL: Output ONLY valid JSON. Start with { and end with }. Include:
{
  "application_name": "application name",
  "framework": "STRIDE or PASTA or PHANTOM-B",
  "summary": "Brief threat summary",
  "threats": [{"id": "T001", "title": "threat", "description": "desc", "category": "cat", "severity": "High", "affected_component": "comp", "attack_vector": "attack", "potential_impact": "impact", "mitigation": "fix"}],
  "data_flows": [{"source": "A", "destination": "B", "data_type": "type", "protocol": "proto", "risks": ["risk"]}],
  "recommendations": ["rec1", "rec2"]
}

DO NOT add any text before or after JSON."""

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
            max_tokens=4000,
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

            if start == -1 or end <= start:
                return None

            json_str = content[start:end].strip()
            report = json.loads(json_str)

            # Validate structure
            if not isinstance(report, dict):
                return None

            # Ensure required fields exist
            if "threats" not in report:
                report["threats"] = []
            if "recommendations" not in report:
                report["recommendations"] = []
            if "summary" not in report:
                report["summary"] = "Threat analysis"

            return report

        except (json.JSONDecodeError, ValueError) as e:
            print(f"Failed to parse threat report: {e}")
            return None
