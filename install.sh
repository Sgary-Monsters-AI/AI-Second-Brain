#!/bin/bash
# AI Second Brain - 智能安装与更新程序
# Copyright (c) 2026 Sgary-Monsters-AI

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

REPO_URL="https://github.com/Sgary-Monsters-AI/AI-Second-Brain.git"
INSTALL_DIR="$HOME/AI-Second-Brain"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  🧠 AI Second Brain 系统助手${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 比较版本号函数 (1: v1>v2, 2: v1<v2, 0: 相等)
compare_versions() {
    if [[ $1 == $2 ]]; then return 0; fi
    local IFS=.
    local i ver1=($1) ver2=($2)
    # 填充空位
    for ((i=${#ver1[@]}; i<3; i++)); do ver1[i]=0; done
    for ((i=${#ver2[@]}; i<3; i++)); do ver2[i]=0; done
    for ((i=0; i<3; i++)); do
        if [[ 10#${ver1[i]} > 10#${ver2[i]} ]]; then return 1; fi
        if [[ 10#${ver1[i]} < 10#${ver2[i]} ]]; then return 2; fi
    done
    return 0
}

# ----------------------------------------------------------------------
# 场景 1: 未安装 -> 执行全新安装
# ----------------------------------------------------------------------
if [ ! -d "$INSTALL_DIR/.git" ]; then
    echo -e "${CYAN}▶ 检测到系统未安装，正在执行全新安装...${NC}"

    if [ -d "$INSTALL_DIR" ]; then
        echo -e "${YELLOW}警告: 目录 $INSTALL_DIR 已存在但不是 Git 仓库。${NC}"
        echo "为了避免覆盖您的文件，请手动重命名或删除该目录后重试。"
        exit 1
    fi

    # 克隆仓库
    echo "正在下载最新系统..."
    git clone "$REPO_URL" "$INSTALL_DIR"

    cd "$INSTALL_DIR"

    # 禁用 push —— 用户端只能拉取更新，不能推送到上游仓库
    git remote set-url --push origin PUSH_DISABLED_USE_UPDATE_SH_INSTEAD

    VERSION=$(cat VERSION 2>/dev/null || echo "1.0.0")

    echo ""
    echo -e "${GREEN}✓ 安装成功！当前版本: v${VERSION}${NC}"
    echo ""

    # 显示最新的更新日志 (截取 CHANGELOG 中最新的一个块)
    if [ -f "CHANGELOG.md" ]; then
        echo -e "${CYAN}📜 最新版本说明 (v${VERSION})：${NC}"
        # 打印匹配 ## [ 版本 的下一个直到下一个 ## 之间的内容
        awk '/^## \[/{if (p) exit; p=1; print; next} p' CHANGELOG.md
        echo ""
    fi

    echo -e "${YELLOW}👉 使用方法：${NC}"
    echo "1. 运行: cd ~/AI-Second-Brain"
    echo "2. 运行: claude"
    echo "3. 在 Claude Code 中输入: 启动 AI 助手"
    exit 0
fi

# ----------------------------------------------------------------------
# 场景 2: 已安装 -> 检查更新
# ----------------------------------------------------------------------
cd "$INSTALL_DIR"
echo -e "${CYAN}▶ 检查系统更新...${NC}"

# 确保 push 已禁用（用户端只能拉取，不能推送到上游仓库）
PUSH_URL=$(git remote get-url --push origin 2>/dev/null || echo "")
if [[ "$PUSH_URL" != "PUSH_DISABLED_USE_UPDATE_SH_INSTEAD" ]]; then
    git remote set-url --push origin PUSH_DISABLED_USE_UPDATE_SH_INSTEAD
fi

# 获取本地版本
LOCAL_VERSION=$(cat VERSION 2>/dev/null || echo "0.0.0")

# 获取远程最新版本信息 (静默拉取并检查)
echo "正在获取远程更新信息..."
git fetch origin main -q

# 提取远程 VERSION 文件的内容
REMOTE_VERSION=$(git show origin/main:VERSION 2>/dev/null || echo "0.0.0")

echo -e "当前本地版本: ${YELLOW}v${LOCAL_VERSION}${NC}"
echo -e "远程最新版本: ${GREEN}v${REMOTE_VERSION}${NC}"

# 比对版本
compare_versions "$LOCAL_VERSION" "$REMOTE_VERSION"
COMPARE_RESULT=$?

if [ $COMPARE_RESULT -eq 0 ] || [ $COMPARE_RESULT -eq 1 ]; then
    # 本地版本 >= 远程版本
    echo ""
    echo -e "${GREEN}🎉 恭喜！您当前已经是最新版本，无需更新！${NC}"
    exit 0
fi

# 本地版本 < 远程版本，需要更新
echo ""
echo -e "${CYAN}▶ 发现新版本 v${REMOTE_VERSION}，正在为您更新...${NC}"

# 检查是否有未提交的更改
if [[ -n $(git status -s) ]]; then
    echo -e "${YELLOW}⚠️ 检测到您在本地修改了文件。${NC}"
    STASH_MESSAGE="更新前自动备份 v${LOCAL_VERSION} - $(date '+%Y-%m-%d %H:%M:%S')"
    git stash push -m "$STASH_MESSAGE" > /dev/null
    echo "已将您的本地修改暂存至备份中。"
    STASHED=true
fi

# 执行更新
if git pull origin main -q; then
    echo -e "${GREEN}✓ 系统核心更新成功！${NC}"
else
    echo -e "${RED}✗ 更新失败，可能存在合并冲突。${NC}"
    if [ "$STASHED" = true ]; then
        git stash pop > /dev/null
    fi
    exit 1
fi

# 恢复暂存的更改
if [ "$STASHED" = true ]; then
    echo -e "${CYAN}▶ 正在恢复您的本地修改...${NC}"
    if git stash pop > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 本地修改恢复成功！${NC}"
    else
        echo -e "${YELLOW}⚠️ 恢复本地修改时出现冲突，请手动解决。${NC}"
    fi
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}  系统升级完成！ v${LOCAL_VERSION} ➔ v${REMOTE_VERSION}${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 显示最新的更新日志 (截取 CHANGELOG 中最新的一个块)
if [ -f "CHANGELOG.md" ]; then
    echo -e "${CYAN}📜 最新更新内容：${NC}"
    # 打印匹配 ## [ 版本 的下一个直到下一个 ## 之间的内容
    awk '/^## \[/{if (p) exit; p=1; print; next} p' CHANGELOG.md
fi

echo ""
echo "继续探索您的第二大脑吧！"
