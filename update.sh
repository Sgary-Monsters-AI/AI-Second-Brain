#!/bin/bash
# AI Second Brain - 用户更新脚本 v2.0
# 用于已安装用户更新到最新版本

set -e

# 获取脚本所在目录（如果在 dev-tools 中运行，需要调整路径）
if [ -f "dev-tools/lib/common.sh" ]; then
    LIB_DIR="dev-tools/lib"
elif [ -f "lib/common.sh" ]; then
    LIB_DIR="lib"
else
    # 回退到基本功能
    LIB_DIR=""
fi

# 如果找到函数库，加载它
if [ -n "$LIB_DIR" ] && [ -f "$LIB_DIR/common.sh" ]; then
    source "$LIB_DIR/common.sh"
    source "$LIB_DIR/version.sh"
    source "$LIB_DIR/git-utils.sh"
    HAS_LIB=true
else
    # 基本的颜色定义（回退方案）
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    RED='\033[0;31m'
    NC='\033[0m'
    HAS_LIB=false

    log_info() { echo -e "${BLUE}ℹ${NC} $1"; }
    log_success() { echo -e "${GREEN}✓${NC} $1"; }
    log_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
    log_error() { echo -e "${RED}✗${NC} $1" >&2; }
    print_separator() { echo -e "${BLUE}========================================${NC}"; }
    print_title() { print_separator; echo -e "${BLUE}  $1${NC}"; print_separator; echo ""; }
fi

# 显示帮助信息
show_help() {
    cat << EOF
用法: $0 [选项]

选项:
  -h, --help          显示此帮助信息
  -f, --force         强制更新（丢弃本地更改）
  --no-backup         不备份本地更改

示例:
  $0                  # 正常更新
  $0 --force          # 强制更新（危险）
EOF
}

# 解析命令行参数
FORCE_UPDATE=false
NO_BACKUP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -f|--force)
            FORCE_UPDATE=true
            shift
            ;;
        --no-backup)
            NO_BACKUP=true
            shift
            ;;
        *)
            log_error "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 主函数
main() {
    print_title "AI Second Brain - 更新工具"

    # 检查是否在 Git 仓库中
    if [ ! -d .git ]; then
        log_error "当前目录不是 Git 仓库"
        log_info "请在 AI-Second-Brain 目录下运行此脚本"
        exit 1
    fi

    # 获取当前版本
    CURRENT_VERSION=$(cat VERSION 2>/dev/null || echo "未知")
    log_info "当前版本: ${GREEN}v${CURRENT_VERSION}${NC}"
    echo ""

    # 检查是否有未提交的更改
    if [[ -n $(git status -s) ]]; then
        log_warning "检测到未提交的更改:"
        git status -s
        echo ""

        if [ "$FORCE_UPDATE" = true ]; then
            log_warning "强制更新模式：将丢弃所有本地更改"
            read -p "确认继续? [y/N]: " confirm
            if [[ ! $confirm =~ ^[Yy]$ ]]; then
                log_info "已取消"
                exit 0
            fi
            git reset --hard HEAD
            log_success "已丢弃本地更改"
        elif [ "$NO_BACKUP" = true ]; then
            log_error "存在未提交的更改，且禁用了备份"
            log_info "请先提交更改或使用 --force 强制更新"
            exit 1
        else
            # 使用 git stash 备份
            read -p "是否暂存当前更改? [Y/n]: " backup
            if [[ ! $backup =~ ^[Nn]$ ]]; then
                STASH_MESSAGE="更新前的自动备份 - $(date '+%Y-%m-%d %H:%M:%S')"
                git stash push -m "$STASH_MESSAGE"
                log_success "已暂存更改: $STASH_MESSAGE"
                STASHED=true
            else
                log_error "存在未提交的更改"
                log_info "请先提交更改或使用 --force 强制更新"
                exit 1
            fi
        fi
    fi

    # 获取远程信息
    REMOTE=$(git remote 2>/dev/null | head -1 || echo "origin")
    BRANCH=$(git branch --show-current 2>/dev/null || echo "main")

    # 拉取最新代码
    log_info "正在从 $REMOTE/$BRANCH 拉取最新版本..."
    echo ""

    if git fetch "$REMOTE" && git pull "$REMOTE" "$BRANCH"; then
        log_success "拉取成功"
    else
        log_error "拉取失败"

        # 如果有暂存的更改，尝试恢复
        if [ "$STASHED" = true ]; then
            log_info "正在恢复暂存的更改..."
            if git stash pop; then
                log_success "已恢复暂存的更改"
            else
                log_warning "恢复暂存的更改时出现冲突"
                log_info "请手动解决冲突后运行: git stash drop"
            fi
        fi

        exit 1
    fi

    # 获取新版本
    NEW_VERSION=$(cat VERSION 2>/dev/null || echo "未知")

    # 如果有暂存的更改，询问是否恢复
    if [ "$STASHED" = true ]; then
        echo ""
        read -p "是否恢复暂存的更改? [Y/n]: " restore
        if [[ ! $restore =~ ^[Nn]$ ]]; then
            if git stash pop; then
                log_success "已恢复暂存的更改"
            else
                log_warning "恢复暂存的更改时出现冲突"
                log_info "请手动解决冲突"
            fi
        else
            log_info "暂存的更改已保留，可以稍后恢复: git stash pop"
        fi
    fi

    # 显示完成信息
    echo ""
    print_separator
    echo -e "  ${GREEN}更新完成!${NC}"
    print_separator
    echo -e "  旧版本: ${YELLOW}v${CURRENT_VERSION}${NC}"
    echo -e "  新版本: ${GREEN}v${NEW_VERSION}${NC}"
    print_separator
    echo ""

    # 显示最新的更新日志 (截取 CHANGELOG 中最新的一个块)
    if [ -f "CHANGELOG.md" ]; then
        echo -e "${CYAN}📜 最新更新内容 (v${NEW_VERSION})：${NC}"
        # 打印匹配 ## [ 版本 的下一个直到下一个 ## 之间的内容
        awk '/^## \[/{if (p) exit; p=1; print; next} p' CHANGELOG.md
    else
        log_info "查看更新日志: cat CHANGELOG.md"
    fi

    echo ""
}

# 运行主函数
main
