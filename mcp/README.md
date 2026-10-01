# Playwright MCP

This project uses Playwright MCP for interactive browser exploration from VS Code. The reusable browser behavior remains in the Python page objects under `job_match/browser`, and automated checks remain in pytest.

## First-time setup

1. Install Node.js 18 or newer and confirm that `node` and `npx` are available in a new VS Code terminal.PS cmd:winget install OpenJS.NodeJS.LTS
2. Open this workspace in VS Code.
3. Open the Command Palette and run `MCP: List Servers`.
4. Start the `playwright` server defined in `.vscode/mcp.json`.
5. In Copilot Chat, select an agent mode that can use MCP tools, then ask it to open a safe page such as `https://playwright.dev/`.

The first start downloads `@playwright/mcp` through `npx`. The `--yes` flag in the workspace configuration accepts that package download without an interactive prompt. The browser is launched by the MCP server, so the Python `pytest-playwright` browser setup is not reused by MCP.

## Recommended POM workflow

1. Use MCP to inspect a page and discover accessible roles, labels, and the navigation flow.
2. Translate the stable flow into a page object under `job_match/browser`.
3. Exercise that page object through a pytest test under `sanity_tests`.
4. Keep login credentials in environment variables or a local secret store. Do not put them in MCP config, page objects, or tests.

## Useful server options

The default configuration starts Chromium. To choose a browser, add an argument such as:

```json
"args": [
  "@playwright/mcp@latest",
  "--browser",
  "chromium"
]
```

Other supported values can be supplied in the same position when needed, for example `firefox` or `webkit`.

## Troubleshooting

- If the server does not start, run `node --version` and `npx --version` in a new terminal.
- If the server still fails during download, run `npx --yes @playwright/mcp@latest` once in a terminal and inspect the reported Node.js or network error.
- If the browser executable is missing, run `uv run playwright install` for the Python test suite; MCP may separately download the browser it needs.
- Stop the MCP server from `MCP: List Servers` before changing its configuration.

# FLOW
You[NLP]
 ↓
VS code Copilot Agent mode[ MCP client]
 ↓ discovers and calls
Playwright MCP tools[browser_navigate, browser_navigate_back,browser_snapshot, browser_find,browser_click]
 ↓
Playwright browser
 ↓
Website

# Role

VS Code Copilot Agent
        │
        │ MCP client
        ▼
Playwright MCP server
        │
        │ Playwright commands
        ▼
Browser


<!-- MCP client: VS Code’s Copilot Agent integration
MCP server: @playwright/mcp
Tool provider: Playwright MCP server
Browser automation engine: Playwright
Browser: Chromium, Firefox, or WebKit
The mcp.json file tells VS Code which MCP server to start and how to start it. Copilot then connects to that server, discovers its tools, and calls them when your request requires browser interaction. -->

# Subjective
VS Code starts the Playwright MCP server using mcp.json.
The MCP server exposes browser tools such as navigation, clicking, typing, screenshots, and page inspection.
Copilot Agent mode discovers those tools.
When your request needs browser interaction, Copilot chooses and calls the appropriate MCP tools.
The MCP server executes the actions through Playwright.