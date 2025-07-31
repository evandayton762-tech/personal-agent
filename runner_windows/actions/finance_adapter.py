"""Finance adapter providing paper brokerage and data access.

This module implements a simplified broker adapter for Alpaca’s paper trading
endpoint and a data adapter for retrieving stock quotes and bars. It follows
the free‑only policy by requiring API keys stored in the secrets adapter. When
secrets are missing or network access is unavailable, functions return a
parked dictionary with an appropriate reason and note.

BrokerAdapter methods:

* ``cash()`` → Returns the available cash balance.
* ``positions()`` → Returns current positions.
* ``place_order(symbol, side, qty, type, limit=None, tif='day')`` → Places a paper order.
* ``order_status(order_id)`` → Returns the current status of an order.
* ``cancel(order_id)`` → Cancels an open order.

DataAdapter methods:

* ``quote(symbol)`` → Returns the latest price for a symbol.
* ``bars(symbol, interval, lookback)`` → Returns historical bars for the symbol.

When API keys are missing, each function returns ``{'status': 'parked', 'reason': 'missing_secret', 'note': ...}``.
When API keys are present, the implementation simulates responses rather than
performing real network calls. In a real environment, one could use the
``alpaca_trade_api`` library or HTTP requests to interact with the Alpaca
paper trading API.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List

from . import secrets_adapter


# Global rate‑limit and cache for data adapter
_quote_cache: Dict[str, Dict[str, Any]] = {}
_bars_cache: Dict[str, Dict[str, Any]] = {}


def _require_api_keys() -> Dict[str, Any]:
    """Return a parked dict if API keys are missing, otherwise an empty dict.

    This helper retrieves the ``ALPACA_API_KEY`` and ``ALPACA_SECRET_KEY`` from the
    secrets adapter. If either value is a dictionary with a ``status`` field
    indicating a parked state, it returns a parked response. Otherwise it
    assumes the keys are present and returns an empty dictionary.
    """
    key = secrets_adapter.get("ALPACA_API_KEY")
    secret = secrets_adapter.get("ALPACA_SECRET_KEY")
    missing = False
    if isinstance(key, dict) and key.get("status") == "parked":
        missing = True
    if isinstance(secret, dict) and secret.get("status") == "parked":
        missing = True
    if missing:
        return {
            "status": "parked",
            "reason": "missing_secret",
            "note": "Alpaca API keys are not configured. Please create a free Alpaca paper trading account and add the keys using secrets.set().",
        }
    return {}


def cash() -> Dict[str, Any]:
    """Return the available cash balance for the paper account."""
    missing = _require_api_keys()
    if missing:
        return missing
    # Simulate a fixed cash balance; a real implementation would query Alpaca
    return {"cash": 10000.0}


def positions() -> Dict[str, Any]:
    """Return current paper positions."""
    missing = _require_api_keys()
    if missing:
        return missing
    # Simulate no open positions
    return {"positions": []}


def place_order(
    symbol: str,
    side: str,
    qty: float,
    order_type: str,
    limit: float | None = None,
    tif: str = "day",
) -> Dict[str, Any]:
    """Place a paper order and return a simulated order ID and status.

    Performs a simple validation on symbol and quantity. If the symbol is
    invalid (non‑alphabetic) or the quantity is non‑positive, returns a parked
    dictionary with reason ``invalid_order``. Also enforces a per‑trade cap of
    $1,000 based on a simulated price of $100 per share.
    """
    missing = _require_api_keys()
    if missing:
        return missing
    # Validate symbol
    if not symbol.isalpha() or qty <= 0:
        return {"status": "parked", "reason": "invalid_order", "note": "Invalid symbol or quantity."}
    # Simulate price and trade cap
    price = 100.0  # $100 per share for simulation
    if qty * price > 1000.0:
        return {"status": "parked", "reason": "trade_cap_exceeded", "note": "Trade size exceeds the $1,000 cap."}
    # Simulate an order ID and accepted status
    order_id = f"ORDER{int(time.time() * 1000)}"
    return {"order_id": order_id, "status": "accepted", "filled_qty": 0.0}


def order_status(order_id: str) -> Dict[str, Any]:
    """Return the status of a paper order. Always returns filled after a delay."""
    missing = _require_api_keys()
    if missing:
        return missing
    # Simulate an order fill
    return {"order_id": order_id, "status": "filled", "filled_qty": 1.0}


def cancel(order_id: str) -> Dict[str, Any]:
    """Cancel an order. In simulation, always succeeds."""
    missing = _require_api_keys()
    if missing:
        return missing
    return {"order_id": order_id, "status": "canceled"}


# Data adapter

def _rate_limited(key: str, cache: Dict[str, Dict[str, Any]], min_interval: float = 60.0) -> bool:
    """Return True if a new request should be blocked due to rate limiting."""
    entry = cache.get(key)
    if not entry:
        return False
    last_time = entry.get("ts")
    return last_time and (time.time() - last_time < min_interval)


def quote(symbol: str) -> Dict[str, Any]:
    """Return the latest price for a symbol using a simulated data source."""
    missing = _require_api_keys()
    if missing:
        # Data adapter uses a separate provider; still require its key
        # Reuse missing_secret reason for simplicity
        return missing
    key = symbol.upper()
    if _rate_limited(key, _quote_cache):
        # Simulate rate limit
        return {"status": "parked", "reason": "rate_limit", "note": "Data provider rate limit exceeded."}
    # Simulate price as $100 for any symbol
    _quote_cache[key] = {"price": 100.0, "ts": time.time()}
    return {"symbol": key, "price": 100.0}


def bars(symbol: str, interval: str, lookback: int) -> Dict[str, Any]:
    """Return simulated historical bars for a symbol."""
    missing = _require_api_keys()
    if missing:
        return missing
    key = f"{symbol.upper()}_{interval}_{lookback}"
    if _rate_limited(key, _bars_cache):
        return {"status": "parked", "reason": "rate_limit", "note": "Data provider rate limit exceeded."}
    # Simulate bars as a list of dicts with OHLCV
    bars = []
    for i in range(lookback):
        bars.append({"open": 100.0, "high": 101.0, "low": 99.0, "close": 100.0, "volume": 1000})
    _bars_cache[key] = {"bars": bars, "ts": time.time()}
    return {"symbol": symbol.upper(), "bars": bars}