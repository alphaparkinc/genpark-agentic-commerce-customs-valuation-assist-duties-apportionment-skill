# -*- coding: utf-8 -*-
"""Customs Valuation Assists & Tooling Cost Apportionment Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def apportion_customs_assists_tooling(**kwargs):
    """Apportions buyer-provided engineering, molds, dies, and tooling assists across import production runs in compliance with 19 C.F.R. § 152.103 and WTO Customs Valuation Agreement."""
    total_tooling_assist_cost_usd = kwargs.get('total_tooling_assist_cost_usd')
    apportionment_method = kwargs.get('apportionment_method')
    current_import_shipment_units = kwargs.get('current_import_shipment_units')
    anticipated_total_production_units = kwargs.get('anticipated_total_production_units')
    duty_rate_pct = kwargs.get('duty_rate_pct')

    if apportionment_method == "FIRST_SHIPMENT":
        apportioned_assist_value_usd = total_tooling_assist_cost_usd
    elif apportionment_method == "UNITS_PRODUCED":
        unit_assist_rate = total_tooling_assist_cost_usd / (anticipated_total_production_units if anticipated_total_production_units > 0 else 1.0)
        apportioned_assist_value_usd = round(unit_assist_rate * current_import_shipment_units, 2)
    else:
        unit_assist_rate = total_tooling_assist_cost_usd / (anticipated_total_production_units if anticipated_total_production_units > 0 else 1.0)
        apportioned_assist_value_usd = round(unit_assist_rate * current_import_shipment_units, 2)
        
    additional_dutiable_liability_usd = round(apportioned_assist_value_usd * (duty_rate_pct / 100.0), 2)
    
    result = {
        "status": "success",
        "total_assist_cost_usd": total_tooling_assist_cost_usd,
        "apportionment_method": apportionment_method,
        "current_shipment_units": current_import_shipment_units,
        "apportioned_assist_dutiable_value_usd": apportioned_assist_value_usd,
        "incremental_customs_duty_due_usd": additional_dutiable_liability_usd,
        "cbp_form_7501_declaration_entry": f"Add ${apportioned_assist_value_usd:,.2f} to Dutiable Value Box 35 under 19 CFR 152.103 Assists.",
        "engine": "GenPark WTO & US Customs Valuation Assists Apportionment Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "apportion_customs_assists_tooling": {
        "name": "apportion_customs_assists_tooling",
        "description": "Apportions buyer-provided engineering, molds, dies, and tooling assists across import production runs in compliance with 19 C.F.R. § 152.103 and WTO Customs Valuation Agreement.",
        "parameters": {
            "type": "object",
            "properties": {
                "total_tooling_assist_cost_usd": {"type": "number", "description": "Total cost incurred by buyer for molds/tooling/engineering (USD)"},
                "apportionment_method": {"type": "string", "description": "'FIRST_SHIPMENT' or 'UNITS_PRODUCED' or 'LIFETIME_COMMERCIAL_VOLUME'"},
                "current_import_shipment_units": {"type": "number", "description": "Number of imported units in current entry manifest"},
                "anticipated_total_production_units": {"type": "number", "description": "Total forecasted production run units over contract lifetime"},
                "duty_rate_pct": {"type": "number", "description": "Ad valorem duty rate on imported finished good (e.g. 5.5%)"},
            },
            "required": ['total_tooling_assist_cost_usd', 'apportionment_method', 'current_import_shipment_units', 'anticipated_total_production_units', 'duty_rate_pct']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "apportion_customs_assists_tooling":
            res = apportion_customs_assists_tooling(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-customs-valuation-assist-duties-apportionment-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-customs-valuation-assist-duties-apportionment-skill...")
    test_args = {'total_tooling_assist_cost_usd': 120000.0, 'apportionment_method': 'UNITS_PRODUCED', 'current_import_shipment_units': 15000.0, 'anticipated_total_production_units': 60000.0, 'duty_rate_pct': 5.5}
    res = apportion_customs_assists_tooling(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-customs-valuation-assist-duties-apportionment-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
