#!/bin/bash

# 打包 chinese-viral-writer skill

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$SCRIPT_DIR/dist"
SKILL_NAME="chinese-viral-writer"

echo "📦 Packaging $SKILL_NAME..."

# 创建 dist 目录
mkdir -p "$DIST_DIR"

# 创建临时目录
TEMP_DIR=$(mktemp -d)
mkdir -p "$TEMP_DIR/$SKILL_NAME"

# 复制文件
cp "$SCRIPT_DIR/SKILL.md" "$TEMP_DIR/$SKILL_NAME/"
cp -r "$SCRIPT_DIR/references" "$TEMP_DIR/$SKILL_NAME/"

# 打包
cd "$TEMP_DIR"
zip -r "$DIST_DIR/$SKILL_NAME.skill" "$SKILL_NAME"

# 清理
rm -rf "$TEMP_DIR"

echo "✅ Successfully packaged to: $DIST_DIR/$SKILL_NAME.skill"
