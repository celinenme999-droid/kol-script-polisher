"""
AI客户端 - 支持多种AI模型提供商
"""

import os
from typing import Optional
from abc import ABC, abstractmethod


class AIClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class OpenAIClient(AIClient):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=self.api_key)
        return self._client
    
    def generate(self, prompt: str) -> str:
        client = self._get_client()
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content


class QwenClient(AIClient):
    def __init__(self, api_key: str, model: str = "qwen-max"):
        self.api_key = api_key
        self.model = model
    
    def generate(self, prompt: str) -> str:
        import dashscope
        from dashscope import Generation
        
        dashscope.api_key = self.api_key
        response = Generation.call(
            model=self.model,
            prompt=prompt,
            temperature=0.7,
        )
        if response.status_code == 200:
            return response.output.text
        raise Exception(f"Qwen API error: {response.code} - {response.message}")


class ClaudeClient(AIClient):
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key
        self.model = model
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self.api_key)
        return self._client
    
    def generate(self, prompt: str) -> str:
        client = self._get_client()
        message = client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text


class MockClient(AIClient):
    def generate(self, prompt: str) -> str:
        return "[模拟润色结果] 实际润色需要配置API Key"


def get_ai_client(provider: str, api_key: Optional[str], model: str) -> AIClient:
    if not api_key:
        return MockClient()
    
    if provider == "OpenAI":
        return OpenAIClient(api_key, model)
    elif provider == "通义千问":
        return QwenClient(api_key, model)
    elif provider == "Claude":
        return ClaudeClient(api_key, model)
    else:
        return MockClient()
