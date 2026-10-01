Playwright is a node.js library built on Javascript.

Client -> WebSocket Connection -> Playwright Server
[Java/   [One time Connection gets [Commands to be executed.]
         established]
Python 
Testcodes in IDEs]

So connection never gets terminated and all the testcase steps get executed in the one established connection.

🛜 The 2 Underlying Protocols: Two distinct communication channels make this system work fluidly across different layers:Connection LayerProtocol UsedWhy It MattersClient ↔ Playwright ServerWebSocket ProtocolKeeps a single, bi-directional connection open. Commands flow instantly back-to-back without the overhead of repeating HTTP handshake cycles.Playwright Server ↔ Browser EnginesCDP / W1 ProtocolUses the native Chrome DevTools Protocol (CDP) for Chromium. For Firefox and WebKit, it uses a custom, optimized variation called W1. This provides low-level control over network interception, DOM changes, and JavaScript execution.

[ Your Test Code ] 
       │ (Code converted to JSON)
       ▼
[ Playwright Client ] 
       │
       │  ⚡ WebSocket Connection (Persistent & Fast)
       ▼
[ Playwright Server (Node.js) ] 
       │
       │  🛠️ CDP / W1 Protocol (Direct browser-level access)
       ▼
[ Browser Engine (Chromium/Firefox/WebKit) ] ──▶ (Executes action & returns results)

Difference with Selenium.
For each command execution, HTTP requests being sent.

Advantages: Fast,Less flaky.

 Key Architectural Advantages:
 1. Browser Context Isolation: Instead of spinning up an entirely separate, heavy browser instance for each test case, Playwright initializes isolated BrowserContexts. Think of them like separate "incognito tabs" within a single browser process—they share the binary file overhead but maintain entirely distinct cookies, local storage, and session footprints. This makes parallel execution incredibly fast and low on memory usage.

 2. No Flakiness via Auto-Waiting: Because the server operates on a low-level browser protocol (CDP), it remains constantly aware of the web page's state. It can tell natively when elements are attached, visible, stable, or receiving pointer events before attempting an action, completely bypassing the need for arbitrary sleep timers.


# Debugging
 $env:PWDEBUG="1"; uv run pytest .\sanity_tests\test_naukri_job_search.py -v -s
 Remove-Item Env:PWDEBUG

 uv run playwright codegen https://www.naukri.com/