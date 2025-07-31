"""Minimum Viable Input (MVI) definitions per domain.

This module lists the required fields for each supported domain. The intake
manager uses these definitions to determine completeness and to generate
appropriate questions.
"""

from typing import Dict, List


# Required parameters per domain
MVI_DEFINITIONS: Dict[str, List[str]] = {
    "finance": [
        "mode",
        "universe",
        "per_trade_cap",
        "daily_cap",
        "data_provider",
        "broker",
    ],
    "leadgen": [
        "output_type",
        "platform",
        "asset_source",
        "cadence",
    ],
    "ecommerce": [
        "platform",
        "items_count",
        "asset_source",
        "pricing_rule",
    ],
    "social": [
        "platform",
        "asset_source",
        "cadence",
    ],
    "outreach": [
        "source_csv",
        "profile_data",
        "throttle_rules",
    ],
}


# Multiple-choice options for fields. These reflect the prompts defined in
# `/docs/prompts_intake_templates.md`. Free-form answers are allowed when
# a field has no listed options.
MVI_OPTIONS: Dict[str, List[str]] = {
    "mode": ["paper", "live"],
    "data_provider": ["alpha_vantage_free", "polygon_basic_free"],
    "broker": ["alpaca_paper", "ibkr_live"],
    "output_type": ["Static HTML page", "PDF document", "Social media post"],
    "platform": ["GitHub Pages", "Netlify", "LinkedIn", "Other"],
    "asset_source": ["user_provided", "auto_generate"],
    "cadence": ["one-time", "weekly", "monthly"],
    "pricing_rule": ["cost_plus_markup", "fixed_price"],
}