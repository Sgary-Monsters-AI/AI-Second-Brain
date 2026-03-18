#!/bin/bash

# AI 第二大脑系统 - 安装脚本
# 用法: ./install.sh [目录名]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 默认目录名
DEFAULT_NAME="AI-Second-Brain"
TARGET_DIR="${1:-$DEFAULT_NAME}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  AI 第二大脑系统 - 安装向导${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查是否提供了自定义名称
if [ -z "$1" ]; then
    echo -e "${YELLOW}提示: 你可以自定义目录名${NC}"
    echo -e "用法: ./install.sh AI-MyName"
    echo ""
    echo "将使用默认名称: $DEFAULT_NAME"
    echo ""
fi

# 获取当前目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 检查目标目录是否已存在
if [ -d "$HOME/$TARGET_DIR" ]; then
    echo -e "${RED}错误: 目录 $HOME/$TARGET_DIR 已存在${NC}"
    echo "请删除或选择其他名称"
    exit 1
fi

# 复制模板到目标目录
echo "正在安装到: $HOME/$TARGET_DIR"
cp -r "$SCRIPT_DIR" "$HOME/$TARGET_DIR"

# 删除安装脚本本身（不需要复制到用户目录）
rm "$HOME/$TARGET_DIR/install.sh"

# 如果用户提供了自定义名称，更新 CLAUDE.md
if [ "$TARGET_DIR" != "$DEFAULT_NAME" ]; then
    # 提取名称（去掉 AI- 前缀）
    USER_NAME="${TARGET_DIR#AI-}"
    if [ "$USER_NAME" = "$TARGET_DIR" ]; then
        USER_NAME="$TARGET_DIR"
    fi

    # 更新 CLAUDE.md
    sed -i.bak "s/AI 助手/AI_$USER_NAME/g" "$HOME/$TARGET_DIR/CLAUDE.md"
    sed -i.bak "s/用户的 AI 数字分身/$USER_NAME 的 AI 数字分身/g" "$HOME/$TARGET_DIR/CLAUDE.md"
    sed -i.bak "s/启动 AI 助手/启动 AI $USER_NAME/g" "$HOME/$TARGET_DIR/CLAUDE.md"
    rm "$HOME/$TARGET_DIR/CLAUDE.md.bak"

    echo -e "${GREEN}已更新系统名称为: AI_$USER_NAME${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  安装成功！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "安装位置: $HOME/$TARGET_DIR"
echo ""
echo "下一步:"
echo ""
echo "1. 进入目录:"
echo "   cd ~/$TARGET_DIR"
echo ""
echo "2. 启动 Claude Code:"
echo "   claude"
echo ""
echo "3. 启动 AI 助手:"
echo "   启动 AI 助手"
echo ""
echo "详细使用说明请查看 README.md"
echo ""
