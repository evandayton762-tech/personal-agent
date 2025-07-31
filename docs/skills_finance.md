# Skill Specification: Finance

This document defines the minimal viable product (MVP) for finance automation. The agent operates in paper mode by default unless live trading is explicitly enabled with two confirmations.

## Paper Rebalance MVP

1. **Fetch Data (free)**: Use a free data provider (e.g., Alpha Vantage or Polygon basic) to fetch current prices and portfolio positions.
2. **Compute Target Diffs**: Determine the target allocation versus current holdings and calculate the difference for each asset.
3. **Place Paper Orders**: For each asset requiring adjustment, send paper orders via the default broker adapter (e.g., Alpaca paper) subject to per‑trade and daily caps.
4. **Verify Orders**: Poll the broker for order status and ensure that paper orders are accepted and marked as filled or completed.
5. **Capture Evidence**: Collect order JSON, fills, and a broker account snapshot showing positions before and after the rebalance.
6. **Schedule Nightly**: Schedule a nightly run using the scheduler to rebalance again or to generate a summary report.
7. **Park Conditions**: If live trading is requested without two confirmations, or if data fetch exceeds free API limits, create a ParkedItem with the reason and a free alternative (e.g., reduce universe or frequency).
