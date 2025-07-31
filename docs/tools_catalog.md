# Tools and Adapter Catalog

This catalog enumerates the tool adapters available to the runner, their functions, and the evidence they produce. Each adapter defines a set of functions that can be invoked by steps in a plan. Arguments should be passed as JSON objects where applicable.

## 6.1 Web Adapter (Playwright)

- **open(url)**: Navigate to the specified URL.
- **wait(selector, timeout_s)**: Wait until the CSS selector is present or the timeout (in seconds) is reached.
- **type(selector, text)**: Type the provided text into the element matched by the selector.
- **click(selector)**: Click on the element matched by the selector.
- **select(selector, option)**: Select an option from a dropdown or select element.
- **upload(selector, file_path)**: Upload a file from `file_path` using the file input matched by the selector.
- **get_text(selector)**: Retrieve the inner text of the element matched by the selector.
- **screenshot(region?) → image_id**: Capture a screenshot of the page or a region. Returns an image identifier.

Evidence produced: `final_url`, `dom_checks`, `screenshot_id`.

## 6.2 Desktop Adapter (pywinauto primary; pyautogui+opencv fallback)

- **focus(window_title)**: Bring the window with the given title to the foreground.
- **click(control_name|coords)**: Click on a UI control by its name or coordinates (coordinates are allowed only inside a bounded region of interest).
- **type(text)**: Type text into the active control or window.

Evidence produced: `screenshot`, `UIA control exists`.

## 6.3 Files Adapter

- **write(path, text|bytes)**: Write text or binary data to a file at the given path.
- **read(path)**: Read the contents of a file.
- **move(src, dst)**: Move a file from `src` to `dst`.
- **hash(path)**: Compute a cryptographic hash of the file contents.

## 6.4 OCR Adapter

- **read(image_id|region) → text_normalized**: Perform optical character recognition on the given image or region. Returns normalized text.

## 6.5 Secrets Adapter

- **get(alias)**: Retrieve the secret value associated with an alias.
- **set(alias, value)**: Store a secret value under an alias. Implementation should protect the secret from exposure.
- **rotate(alias)**: Rotate the secret associated with an alias; plan only. Actual rotation occurs via provider consoles.

## 6.6 Schedule Adapter (APScheduler later)

- **enqueue(step, when|cron)**: Schedule a step for future execution at a specific time or according to a cron expression.
- **list()**: List scheduled jobs.
- **cancel(id)**: Cancel a scheduled job by its identifier.

## 6.7 Budget Adapter

- **estimate(plan) → tokens_estimate, checkpoint(step_id, tokens), halt_if_exceeds()**: Estimate total tokens for a plan, record token consumption at checkpoints, and halt execution if token usage would exceed configured caps.

## 6.8 Finance Adapter

**BrokerAdapter** functions:

- **cash()**: Return current cash balance.
- **positions()**: List current positions.
- **place_order(symbol, side, qty, type, limit?, tif)**: Place an order with the broker. Parameters include symbol, buy/sell side, quantity, order type, optional limit price, and time‑in‑force.
- **order_status(id)**: Retrieve status of an existing order.
- **cancel(id)**: Cancel a pending order.

Implementations: `alpaca_paper` (default paper trading), `ibkr_live` (live trading; locked by default).

**DataAdapter** functions:

- **quote(symbol)**: Fetch the latest quote for the given symbol.
- **bars(symbol, interval, lookback)**: Retrieve historical bars for a symbol over a lookback period at a specified interval.

Providers: `alpha_vantage_free`, `polygon_basic_free`, `yfinance` (optional free data source).

## 6.9 Docs Adapter (Google Docs)

- **ensure_doc(project_name) → doc_id**: Create or retrieve a Google Doc for the project.
- **append_section(doc_id, heading, markdown_or_struct)**: Append a new section with a heading and content (markdown or structured data).
- **insert_table(doc_id, rows)**: Insert a table with the given rows.
- **insert_image(doc_id, image_path_or_drive_id)**: Insert an image into the document.
- **link_artifact(doc_id, title, href)**: Add a hyperlink to an external artifact.
- **update_toc(doc_id)**: Refresh the table of contents.

Evidence produced: document IDs and revision metadata.
