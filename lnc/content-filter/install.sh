#!/bin/bash

# Content Evaluation Skill Installer
# 内容评估技能安装脚本

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     Content Evaluation Skill Installer                    ║"
echo "║     内容评估技能安装程序                                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default installation path
DEFAULT_TARGET="$HOME/.claude"
TARGET_DIR="${1:-$DEFAULT_TARGET}"

echo -e "${YELLOW}Installation target / 安装目标: ${TARGET_DIR}${NC}"
echo ""

# Check if skill directory exists
if [ ! -d "$SCRIPT_DIR/skill" ]; then
    echo -e "${RED}Error: skill directory not found / 错误: 找不到 skill 目录${NC}"
    exit 1
fi

# Create target directories
echo -e "${BLUE}Creating directories / 创建目录...${NC}"
mkdir -p "$TARGET_DIR/skills/content-eval"

# Copy skill file (must be named SKILL.md in a directory)
echo -e "${BLUE}Installing skill file / 安装技能文件...${NC}"
cp "$SCRIPT_DIR/skill/content-evaluation.md" "$TARGET_DIR/skills/content-eval/SKILL.md"

# Note: settings.json is NOT needed for directory-based skills
# Claude Code automatically discovers skills from directories with SKILL.md

# Copy templates (optional)
if [ -d "$SCRIPT_DIR/templates" ]; then
    echo -e "${BLUE}Installing templates / 安装模板...${NC}"
    mkdir -p "$TARGET_DIR/data"
    cp "$SCRIPT_DIR/templates/"* "$TARGET_DIR/data/" 2>/dev/null || true
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Installation Complete! / 安装完成!                    ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Skill installed to / 技能已安装到: ${BLUE}$TARGET_DIR/skills/content-eval/SKILL.md${NC}"
echo ""
echo -e "${YELLOW}Usage / 使用方法:${NC}"
echo -e "  In Claude Code, type: ${BLUE}/content-eval${NC}"
echo ""
echo -e "${YELLOW}Example / 示例:${NC}"
echo -e "  /content-eval"
echo -e "  请评估以下内容："
echo -e "  【目标平台】小红书"
echo -e "  【品牌定位】专业护肤博主"
echo -e "  【内容草稿】..."
echo ""
