from typing import Any
from openai import OpenAI
from lib.llm_agents.base_llm_agent import BaseLLMAgent
from lib.common.constants import OPENAI_API_KEY


class OpenAILLMAgent(BaseLLMAgent):
    def __init__(self) -> None:
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    @staticmethod
    def _antropic_tools_to_openai_tools(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
        open_ai_tools = []
        for tool in tools:
            open_ai_tool = {}
            open_ai_tool['type'] = 'function'
            open_ai_tool['name'] = tool['name']
            open_ai_tool['description'] = tool['description']
            open_ai_tool['parameters'] = {}
            open_ai_tool['parameters']['type'] = tool['input_schema']['type']
            open_ai_tool['parameters']['required'] = tool['input_schema']['required']
            open_ai_tool['parameters']['properties'] = {}
            for parameter_name, parameter_properties in tool['input_schema']['properties'].items():
                open_ai_tool['parameters']['properties'][parameter_name] = {
                    "type": parameter_properties['type'],
                    "description": parameter_properties['title'],
                }

            open_ai_tools.append(open_ai_tool)

        return open_ai_tools

    def call(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]):
        open_ai_tools = self._antropic_tools_to_openai_tools(tools)
        response = self.client.responses.create(
            model='gpt-4o-mini',
            input=messages,
            tools=open_ai_tools,
        )

        return response
