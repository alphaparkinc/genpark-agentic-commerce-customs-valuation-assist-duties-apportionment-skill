# Customs Valuation Assists & Tooling Cost Apportionment Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `apportion_customs_assists_tooling`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Apportions buyer-provided engineering, molds, dies, and tooling assists across import production runs in compliance with 19 C.F.R. § 152.103 and WTO Customs Valuation Agreement.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (Customs Audit & Trade Law)`

## MCP Tool Specification
### `apportion_customs_assists_tooling`
Parameters:
- `total_tooling_assist_cost_usd` (float): Total cost incurred by buyer for molds/tooling/engineering (USD)
- `apportionment_method` (str): 'FIRST_SHIPMENT' or 'UNITS_PRODUCED' or 'LIFETIME_COMMERCIAL_VOLUME'
- `current_import_shipment_units` (float): Number of imported units in current entry manifest
- `anticipated_total_production_units` (float): Total forecasted production run units over contract lifetime
- `duty_rate_pct` (float): Ad valorem duty rate on imported finished good (e.g. 5.5%)

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-customs-valuation-assist-duties-apportionment-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-customs-valuation-assist-duties-apportionment-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
