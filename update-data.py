#!/usr/bin/env python3
"""Convert spx-absen.log to data.json untuk dashboard"""

import json
import os
from datetime import datetime

LOG_FILE = os.path.expanduser("~/spx-absen.log")
OUTPUT_FILE = "data.json"
WAGE_PER_DAY = 245000

MONTH_NAMES = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

def load_log():
    entries = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split("|")
                    if len(parts) >= 3:
                        entries.append({
                            "tanggal": parts[0],
                            "shift": parts[1],
                            "status": parts[2],
                            "catatan": parts[3] if len(parts) > 3 else ""
                        })
    return entries

def get_pay_date(d: datetime):
    if d.day <= 15:
        return datetime(d.year, d.month, 25)
    else:
        if d.month == 12:
            return datetime(d.year + 1, 1, 10)
        else:
            return datetime(d.year, d.month + 1, 10)

def generate_data():
    entries = load_log()
    hadir = [e for e in entries if e["status"] == "hadir"]
    
    # Group by pay date
    grouped = {}
    for e in hadir:
        d = datetime.strptime(e["tanggal"], "%Y-%m-%d")
        pay_d = get_pay_date(d)
        pay_key = pay_d.strftime("%Y-%m-%d")
        grouped.setdefault(pay_key, []).append({
            "tanggal": e["tanggal"],
            "shift": e["shift"],
            "date_obj": d
        })
    
    # Build periods
    periods = []
    for pay_key in sorted(grouped.keys()):
        items = grouped[pay_key]
        dates = sorted([x["date_obj"] for x in items])
        total_hari = len(dates)
        total_upah = total_hari * WAGE_PER_DAY
        
        pay_d = datetime.strptime(pay_key, "%Y-%m-%d")
        first_d = dates[0]
        last_d = dates[-1]
        
        if first_d == last_d:
            periode = f"{first_d.day} {MONTH_NAMES[first_d.month]} {first_d.year}"
        elif first_d.month == last_d.month:
            periode = f"{first_d.day}–{last_d.day} {MONTH_NAMES[last_d.month]} {last_d.year}"
        else:
            periode = f"{first_d.day} {MONTH_NAMES[first_d.month]} – {last_d.day} {MONTH_NAMES[last_d.month]} {last_d.year}"
        
        gajian_str = f"{pay_d.day} {MONTH_NAMES[pay_d.month]} {pay_d.year}"
        
        periods.append({
            "gajian": gajian_str,
            "gajian_date": pay_key,
            "hari_kerja": total_hari,
            "periode": periode,
            "upah": total_upah,
            "detail": [{"tanggal": x["tanggal"], "shift": x["shift"]} for x in items]
        })
    
    total_semua = len(hadir) * WAGE_PER_DAY
    
    data = {
        "updated": datetime.now().isoformat(),
        "total_hari_kerja": len(hadir),
        "total_upah": total_semua,
        "wage_per_day": WAGE_PER_DAY,
        "periods": periods,
        "all_entries": entries
    }
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Data updated: {len(hadir)} hari kerja, Rp{total_semua:,}".replace(",", "."))
    print(f"✓ Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_data()
