"""Handle streaming responses from Claude API"""

import json
from anthropic import Anthropic
import os

def stream_threat_analysis(user_message: str, conversation_history: list, system_prompt: str, framework: str = None):
    """
    Stream threat analysis from Claude with tool calls and reasoning.
    Yields JSON events for the frontend.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")

    client = Anthropic(api_key=api_key)

    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # Yield starting event
    yield json.dumps({
        "type": "start",
        "message": "Analyzing threat model...",
        "framework": framework or "general"
    })

    try:
        # Stream the response
        with client.messages.stream(
            model="claude-opus-5",
            max_tokens=4000,
            system=system_prompt,
            messages=conversation_history
        ) as stream:
            full_response = ""
            tool_use_active = False

            for event in stream:
                # Handle content block start
                if event.type == "content_block_start":
                    if hasattr(event.content_block, 'type'):
                        if event.content_block.type == "tool_use":
                            tool_use_active = True
                            yield json.dumps({
                                "type": "tool_start",
                                "tool_name": getattr(event.content_block, 'name', 'unknown'),
                                "tool_id": getattr(event.content_block, 'id', '')
                            })
                        elif event.content_block.type == "text":
                            yield json.dumps({
                                "type": "text_start",
                                "message": "Generating analysis..."
                            })

                # Handle content block delta (streaming text)
                elif event.type == "content_block_delta":
                    if hasattr(event.delta, 'type'):
                        if event.delta.type == "text_delta":
                            text = getattr(event.delta, 'text', '')
                            full_response += text
                            yield json.dumps({
                                "type": "text_chunk",
                                "content": text
                            })
                        elif event.delta.type == "input_json_delta":
                            # Tool input being constructed
                            yield json.dumps({
                                "type": "tool_input",
                                "content": getattr(event.delta, 'input_json', '')
                            })

                # Handle content block stop
                elif event.type == "content_block_stop":
                    if tool_use_active:
                        yield json.dumps({
                            "type": "tool_end",
                            "message": "Tool execution complete"
                        })
                        tool_use_active = False

                # Handle message start (metadata)
                elif event.type == "message_start":
                    if hasattr(event.message, 'usage'):
                        usage = event.message.usage
                        yield json.dumps({
                            "type": "usage_start",
                            "input_tokens": getattr(usage, 'input_tokens', 0)
                        })

                # Handle message delta (final tokens)
                elif event.type == "message_delta":
                    if hasattr(event, 'delta') and hasattr(event.delta, 'usage'):
                        usage = event.delta.usage
                        yield json.dumps({
                            "type": "usage_delta",
                            "output_tokens": getattr(usage, 'output_tokens', 0)
                        })

        # Final response
        yield json.dumps({
            "type": "complete",
            "content": full_response,
            "message": "Analysis complete"
        })

    except Exception as e:
        yield json.dumps({
            "type": "error",
            "error": str(e),
            "message": f"Error during analysis: {str(e)}"
        })


def format_stream_event(event_type: str, **kwargs) -> str:
    """Format an event for streaming"""
    event = {"type": event_type}
    event.update(kwargs)
    return json.dumps(event) + "\n"
