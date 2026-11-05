#!/bin/bash
# Auto-update dashboard data dan push ke GitHub

cd /home/aiagent/spx-dashboard

# Generate data terbaru
python3 update-data.py

# Check jika ada perubahan
if git diff --quiet data.json; then
    echo "Tidak ada perubahan data"
    exit 0
fi

# Commit dan push
git add data.json
git commit -m "Update data $(date +%Y-%m-%d\ %H:%M)"
git push origin main

echo "✓ Dashboard updated dan pushed ke GitHub"
