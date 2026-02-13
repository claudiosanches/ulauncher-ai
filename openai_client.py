import requests


class OpenAIClient:

    API_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, api_key, model="gpt-4o-mini"):
        self.api_key = api_key
        self.model = model

    def ask(self, question):
        """Ask a general question and return the response text."""
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Give concise, direct answers. "
                    "Use plain text only, no markdown formatting. "
                    "Keep responses short (2-3 sentences max)."
                ),
            },
            {"role": "user", "content": question},
        ]
        return self._call_api(messages, max_tokens=300)

    def synonyms(self, word):
        """Return a list of synonyms for the given word."""
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a synonym finder. Given a word, return only a "
                    "comma-separated list of synonyms. No explanations, no "
                    "numbering, no extra text. Just the synonyms separated by commas."
                ),
            },
            {"role": "user", "content": word},
        ]
        response = self._call_api(messages, max_tokens=100)
        return [s.strip() for s in response.split(",") if s.strip()]

    def _call_api(self, messages, max_tokens):
        headers = {
            "Authorization": "Bearer %s" % self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }
        response = requests.post(
            self.API_URL, headers=headers, json=payload, timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
