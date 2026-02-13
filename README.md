# Ulauncher AI Assistant

A [Ulauncher](https://ulauncher.io/) extension that integrates directly with the OpenAI API to answer questions and find synonyms — all inline, without leaving Ulauncher.

## Features

- **AI Question mode** (`ai`) — Ask any question and get a concise answer displayed directly in Ulauncher
- **Synonym mode** (`syn`) — Find synonyms for any word, each displayed as a selectable item
- **Copy to clipboard** — Press Enter on any result to copy it
- **Configurable** — Choose your model, API key, and max results from Ulauncher preferences

## Installation

1. Open Ulauncher Preferences
2. Go to **Extensions** > **Add extension**
3. Paste the repository URL:
   ```
   https://github.com/laercioskt/ulauncher-ai
   ```

### Manual Installation

Clone the repository into the Ulauncher extensions directory:

```bash
git clone https://github.com/laercioskt/ulauncher-ai.git \
  ~/.local/share/ulauncher/extensions/com.github.laercioskt.ulauncher-ai
```

## Setup

1. Get an API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Open Ulauncher Preferences > **Extensions** > **AI Assistant**
3. Paste your API key in the **OpenAI API Key** field
4. (Optional) Change the model or max results

## Usage

### Ask a question

Type `ai` followed by your question:

```
ai What is the capital of France?
ai Explain recursion in one sentence
ai How do I list files in Linux?
```

The response is split into readable chunks. Press **Enter** on any item to copy the full answer to your clipboard.

### Find synonyms

Type `syn` followed by a word:

```
syn happy
syn fast
syn beautiful
```

Each synonym appears as a separate item. Press **Enter** to copy that synonym to your clipboard.

## Preferences

| Preference | Default | Description |
|---|---|---|
| **OpenAI API Key** | *(empty)* | Your OpenAI API key (required) |
| **OpenAI Model** | `gpt-4o-mini` | Model to use (e.g. `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo`) |
| **Max Results** | `5` | Maximum number of items displayed in the results list |

## Error Messages

| Message | Cause |
|---|---|
| OpenAI API key not configured | API key is empty in preferences |
| Invalid OpenAI API key | The API key was rejected (HTTP 401) |
| Rate limit or quota exceeded | Too many requests or billing quota reached (HTTP 429) |
| Model not found | The configured model name is invalid (HTTP 404) |
| Request timed out | The API did not respond within 10 seconds |
| Network error | No internet connection or DNS failure |

## Requirements

- Ulauncher 5 (API v2)
- Python 3
- `requests` library (included with Ulauncher)
- An OpenAI API key with available credits

## License

MIT
