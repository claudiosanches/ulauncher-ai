import logging

import requests
from openai_client import OpenAIClient
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction

ICON = "images/icon.svg"
logger = logging.getLogger(__name__)


class AiExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument()
        keyword = event.get_keyword()
        ai_kw = extension.preferences["ai_kw"]
        syn_kw = extension.preferences["syn_kw"]

        if keyword == ai_kw:
            return self._handle_ai(query, extension)
        elif keyword == syn_kw:
            return self._handle_synonyms(query, extension)

    def _handle_ai(self, query, extension):
        if not query:
            return self._render([self._info_item("Type your question...", "ai <question>")])

        client = self._get_client(extension)
        if not client:
            return self._render([self._error_item("OpenAI API key not configured")])

        try:
            response = client.ask(query)
        except Exception as e:
            return self._render([self._make_error_item(e)])

        max_results = self._get_max_results(extension)
        items = self._split_response(response, max_results)
        return self._render(items)

    def _handle_synonyms(self, query, extension):
        if not query:
            return self._render([self._info_item("Type a word...", "syn <word>")])

        client = self._get_client(extension)
        if not client:
            return self._render([self._error_item("OpenAI API key not configured")])

        try:
            synonyms = client.synonyms(query)
        except Exception as e:
            return self._render([self._make_error_item(e)])

        if not synonyms:
            return self._render([self._info_item("No synonyms found", query)])

        max_results = self._get_max_results(extension)
        items = []
        for syn in synonyms[:max_results]:
            items.append(
                ExtensionResultItem(
                    icon=ICON,
                    name=syn,
                    description="Press Enter to copy",
                    on_enter=CopyToClipboardAction(syn),
                )
            )
        return self._render(items)

    def _get_client(self, extension):
        api_key = extension.preferences.get("openai_api_key", "").strip()
        if not api_key:
            return None
        model = extension.preferences.get("openai_model", "gpt-4o-mini").strip()
        return OpenAIClient(api_key, model)

    def _get_max_results(self, extension):
        try:
            return int(extension.preferences.get("max_results", "5"))
        except ValueError:
            return 5

    def _split_response(self, response, max_results):
        """Split a response into chunks for display as multiple result items."""
        full_response = response
        chunks = []
        while response:
            if len(response) <= 100:
                chunks.append(response)
                break
            split_at = response.rfind(" ", 0, 100)
            if split_at <= 0:
                split_at = 100
            chunks.append(response[:split_at])
            response = response[split_at:].lstrip()

        items = []
        for chunk in chunks[:max_results]:
            items.append(
                ExtensionResultItem(
                    icon=ICON,
                    name=chunk,
                    description="Press Enter to copy full response",
                    on_enter=CopyToClipboardAction(full_response),
                )
            )
        return items

    def _make_error_item(self, exception):
        """Create an error item based on the exception type."""
        if isinstance(exception, requests.exceptions.Timeout):
            return self._error_item("Request timed out")
        if isinstance(exception, requests.exceptions.ConnectionError):
            return self._error_item("Network error")
        if isinstance(exception, requests.exceptions.HTTPError):
            status = exception.response.status_code
            if status == 401:
                return self._error_item("Invalid OpenAI API key")
            if status == 429:
                return self._error_item("Rate limit or quota exceeded")
            if status == 404:
                return self._error_item("Model not found")
            return self._error_item("API error (HTTP %d)" % status)
        logger.error("Unexpected error: %s", exception)
        return self._error_item("Unexpected error: %s" % str(exception))

    @staticmethod
    def _error_item(message):
        return ExtensionResultItem(
            icon=ICON,
            name=message,
            description="Check extension preferences",
            on_enter=DoNothingAction(),
        )

    @staticmethod
    def _info_item(name, description):
        return ExtensionResultItem(
            icon=ICON,
            name=name,
            description=description,
            on_enter=DoNothingAction(),
        )

    @staticmethod
    def _render(items):
        return RenderResultListAction(items)


if __name__ == "__main__":
    AiExtension().run()
