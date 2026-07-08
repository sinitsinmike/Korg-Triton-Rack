#!/usr/bin/env python3
"""
100_generate_database.py

Collect ROM analysis into one JSON database.
"""

import json
from pathlib import Path

db = {
    "rom": {
        "name": "interleave16.bin",
        "size": 8388608
    },
    "confirmed": [
        {
            "address": "0x00000068",
            "type": "pointer_table",
            "status": "confirmed"
        },
        {
            "address": "0x003A9000",
            "type": "structured_region",
            "status": "confirmed"
        }
    ]
}

out = Path("analysis/db/database.json")

out.parent.mkdir(parents=True, exist_ok=True)

out.write_text(json.dumps(db, indent=4))

print("Database written:")
print(out)