#!/bin/bash

# AI Second Brain System - Copyright Check Script
# Copyright (c) 2026 Roland Wayne
# This script checks if copyright notices are intact

echo "========================================"
echo "  Copyright Check - AI Second Brain"
echo "========================================"
echo ""

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VIOLATIONS=0

# Check LICENSE file exists
echo "[1/5] Checking LICENSE file..."
if [ ! -f "$ROOT_DIR/LICENSE" ]; then
    echo "  ❌ LICENSE file missing!"
    VIOLATIONS=$((VIOLATIONS + 1))
else
    echo "  ✅ LICENSE file exists"
fi

# Check main files have copyright headers
echo ""
echo "[2/5] Checking core files for copyright headers..."

CORE_FILES=(
    "CLAUDE.md"
    "README.md"
    "任务清单.md"
    "对话历史.md"
)

for file in "${CORE_FILES[@]}"; do
    if [ -f "$ROOT_DIR/$file" ]; then
        if grep -q "Copyright (c) 2026 Roland Wayne" "$ROOT_DIR/$file"; then
            echo "  ✅ $file"
        else
            echo "  ❌ $file - Copyright header missing!"
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    fi
done

# Check rule files
echo ""
echo "[3/5] Checking rule files..."

RULE_DIR="$ROOT_DIR/.claude/rules"
if [ -d "$RULE_DIR" ]; then
    for file in "$RULE_DIR"/*.md; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            if grep -q "Copyright (c) 2026 Roland Wayne" "$file"; then
                echo "  ✅ rules/$filename"
            else
                echo "  ❌ rules/$filename - Copyright header missing!"
                VIOLATIONS=$((VIOLATIONS + 1))
            fi
        fi
    done
fi

# Check for removed attribution
echo ""
echo "[4/5] Checking for removed attribution..."

# Check if README still has original author credit
if [ -f "$ROOT_DIR/README.md" ]; then
    if grep -q "Roland Wayne" "$ROOT_DIR/README.md"; then
        echo "  ✅ Author attribution intact"
    else
        echo "  ❌ Author attribution removed!"
        VIOLATIONS=$((VIOLATIONS + 1))
    fi
fi

# Check if license is still dual license
echo ""
echo "[5/5] Checking license type..."
if [ -f "$ROOT_DIR/LICENSE" ]; then
    if grep -q "Dual License" "$ROOT_DIR/LICENSE"; then
        echo "  ✅ Dual license intact"
    else
        echo "  ⚠️  License may have been modified"
        VIOLATIONS=$((VIOLATIONS + 1))
    fi
fi

echo ""
echo "========================================"
if [ $VIOLATIONS -eq 0 ]; then
    echo "  ✅ All copyright checks passed!"
    echo "========================================"
    exit 0
else
    echo "  ❌ Found $VIOLATIONS violation(s)!"
    echo "========================================"
    echo ""
    echo "Please restore original copyright notices"
    echo "or contact Roland Wayne for licensing."
    echo ""
    echo "Copyright (c) 2026 Roland Wayne"
    echo "https://rolandwayne.com"
    exit 1
fi