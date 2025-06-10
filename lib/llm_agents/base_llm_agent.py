from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass


@dataclass
class LLMAgentResponse:
    resp_type: str
    text: str|None = None
    function_name: str|None = None
    arguments: str|None = None
    output: Any = None



class BaseLLMAgent(ABC):

    @abstractmethod
    def call(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> LLMAgentResponse:
        pass

    @abstractmethod
    def get_tool_call_message(self, llm_response: LLMAgentResponse) -> dict[str, str]:
        pass

    @abstractmethod
    def get_function_call_result_message(self, function_output: str) -> dict[str, str]:
        pass
