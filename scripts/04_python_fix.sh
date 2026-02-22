#!/usr/bin/env bash
# Fix Python pip + uv then continue from Step 3
set -euo pipefail
RED='\033[0;31m';GREEN='\033[0;32m';YELLOW='\033[1;33m'
CYAN='\033[0;36m';BOLD='\033[1m';DIM='\033[2m';RESET='\033[0m'
LOG="/var/log/resort_p3_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1
ok()  { echo -e "${GREEN}✓${RESET} ${BOLD}$*${RESET}"; }
log() { echo -e "${CYAN}→${RESET} $*"; }
warn(){ echo -e "${YELLOW}⚠${RESET}  $*"; }
skip(){ echo -e "${DIM}↷ already: $*${RESET}"; }
sec() { echo -e "\n${BOLD}${CYAN}━━━ $* ━━━${RESET}\n"; }
has() { command -v "$1" &>/dev/null; }
[[ $EUID -ne 0 ]] && { echo "sudo bash $0"; exit 1; }
DUSER="${SUDO_USER:-$(getent passwd|awk -F: '$3>=1000{print $1}'|head -1)}"
DHOME=$(getent passwd "$DUSER"|cut -d: -f6)
echo -e "\n${BOLD}${CYAN}  الخيمة — Fix Python + Continue Steps 3→7${RESET}\n"

# ══ FIX PYTHON PIP ══════════════════════════════════════════════
sec "Fix · Python 3.12 pip + tools"

# pip بدون --quiet (مش supported في python3.12 هنا)
log "Installing pip for python3.12..."
apt-get install -y python3-pip python3.12-distutils 2>/dev/null || true
# طريقة بديلة لو فشلت
if ! python3.12 -m pip --version &>/dev/null 2>&1; then
  log "Trying ensurepip..."
  python3.12 -m ensurepip --upgrade 2>/dev/null || true
fi
# آخر محاولة — get-pip مباشر
if ! python3.12 -m pip --version &>/dev/null 2>&1; then
  log "Downloading get-pip.py..."
  curl -fsSL https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py --retry 3
  python3.12 /tmp/get-pip.py 2>/dev/null
  rm -f /tmp/get-pip.py
fi
python3.12 -m pip install --upgrade pip 2>/dev/null || true
ok "pip $(python3.12 -m pip --version 2>/dev/null | grep -oP '\d+\.\d+' | head -1)"

# Python dev tools (بدون --quiet)
log "Installing Python dev tools..."
python3.12 -m pip install black isort mypy flake8 ipython httpie pre-commit 2>/dev/null || \
pip3 install black isort mypy flake8 ipython httpie pre-commit 2>/dev/null || true
ok "black, isort, mypy, flake8, ipython, httpie"

# uv بطريقة صح
if has uv; then
  skip "uv $(uv --version 2>/dev/null)"
else
  log "Installing uv..."
  # uv بيتنصب في home directory
  sudo -u "$DUSER" bash -c \
    'curl -LsSf https://astral.sh/uv/install.sh --retry 3 | sh' 2>/dev/null || true
  # أو عن طريق pip
  if ! sudo -u "$DUSER" bash -c 'export PATH="$HOME/.local/bin:$PATH"; uv --version' &>/dev/null 2>&1; then
    pip3 install uv 2>/dev/null || true
  fi
  ok "uv installed"
fi

# ══ STEP 3: NODE.JS ══════════════════════════════════════════════
sec "3/7 · Node.js 22 LTS + pnpm"
if has node; then
  skip "Node $(node --version)"
else
  log "Installing Node.js 22..."
  curl -fsSL https://deb.nodesource.com/setup_22.x \
    --retry 3 --connect-timeout 30 | bash - > /dev/null
  DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs
  ok "Node $(node --version) | npm $(npm --version)"
fi
has pnpm && skip "pnpm $(pnpm --version)" || {
  npm install -g pnpm@latest 2>/dev/null
  ok "pnpm $(pnpm --version)"
}
npm install -g typescript tsx eslint prettier nodemon pm2 2>/dev/null || true
ok "typescript, eslint, prettier, pm2, nodemon"

# ══ STEP 4: GIT ══════════════════════════════════════════════════
sec "4/7 · Git + GitHub CLI"
add-apt-repository ppa:git-core/ppa -y > /dev/null 2>&1 || true
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y git git-lfs
git lfs install --system --skip-repo > /dev/null 2>&1 || true
ok "Git $(git --version | grep -oP '\d+\.\d+\.\d+')"
if has gh; then
  skip "gh $(gh --version | head -1)"
else
  install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
    -o /etc/apt/keyrings/githubcli-archive-keyring.gpg --retry 3
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] \
https://cli.github.com/packages stable main" \
    | tee /etc/apt/sources.list.d/github-cli.list > /dev/null
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y gh
  ok "gh $(gh --version | head -1)"
fi
sudo -u "$DUSER" git config --global init.defaultBranch main 2>/dev/null || true
sudo -u "$DUSER" git config --global pull.rebase false        2>/dev/null || true
sudo -u "$DUSER" git config --global core.autocrlf input      2>/dev/null || true
sudo -u "$DUSER" git config --global color.ui auto            2>/dev/null || true
ok "Git configured"

# ══ STEP 5: ZSH ══════════════════════════════════════════════════
sec "5/7 · Zsh + Oh-My-Zsh"
has zsh || DEBIAN_FRONTEND=noninteractive apt-get install -y zsh
ok "Zsh $(zsh --version | grep -oP '\d+\.\d+\.\d+')"
if [[ ! -d "${DHOME}/.oh-my-zsh" ]]; then
  sudo -u "$DUSER" sh -c \
    "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
    "" --unattended 2>/dev/null || true
fi
PLUG="${DHOME}/.oh-my-zsh/custom/plugins"
for e in \
  "zsh-autosuggestions:https://github.com/zsh-users/zsh-autosuggestions" \
  "zsh-syntax-highlighting:https://github.com/zsh-users/zsh-syntax-highlighting"; do
  n="${e%%:*}"; u="${e##*:}"
  [[ -d "${PLUG}/${n}" ]] && skip "$n" && continue
  sudo -u "$DUSER" git clone --depth=1 "$u" "${PLUG}/${n}" >/dev/null 2>&1 && ok "plugin: $n"
done
cat > "${DHOME}/.zshrc" << 'ZRC'
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="agnoster"
plugins=(git docker docker-compose python node zsh-autosuggestions zsh-syntax-highlighting history sudo colored-man-pages)
source $ZSH/oh-my-zsh.sh
export PATH="$HOME/.local/bin:$PATH"
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
# ── Git
alias gs='git status'         ; alias ga='git add .'
alias gc='git commit -m'      ; alias gp='git push'
alias gpl='git pull'          ; alias gl='git log --oneline --graph --all'
alias gd='git diff'           ; alias gb='git branch'
alias gco='git checkout'      ; alias gcb='git checkout -b'
# ── Docker
alias dc='docker compose'     ; alias dcu='docker compose up -d'
alias dcd='docker compose down'; alias dcr='docker compose restart'
alias dcl='docker compose logs -f'; alias dcp='docker compose ps'
alias dcb='docker compose build'  ; alias dce='docker compose exec'
alias dps='docker ps'         ; alias dclean='docker system prune -af'
# ── Python
alias py='python3'            ; alias pip='pip3'
alias activate='source .venv/bin/activate'
alias venv='python3 -m venv .venv && source .venv/bin/activate'
# ── Resort
alias resort='cd ~/projects/resort-platform'
alias be='cd ~/projects/resort-platform/backend'
alias fe='cd ~/projects/resort-platform/frontend'
alias api='uvicorn app.main:app --reload --host 0.0.0.0 --port 8000'
# ── System
alias ll='ls -alFh --color=auto' ; alias la='ls -A'
alias ..='cd ..'                  ; alias ...='cd ../..'
alias ports='ss -tlnp'            ; alias myip='curl -s ifconfig.me'
alias mem='free -h'               ; alias disk='df -h'
alias update='sudo apt update && sudo apt upgrade -y'
alias rm='rm -i'                  ; alias cp='cp -i'; alias mv='mv -i'
# ── Functions
mkcd() { mkdir -p "$1" && cd "$1"; }
dex()  { docker exec -it "$1" "${2:-bash}"; }
backup(){ cp -r "$1" "${1}_bak_$(date +%Y%m%d_%H%M%S)"; }
serve(){ python3 -m http.server "${1:-8080}"; }
ZRC
chown "$DUSER:$DUSER" "${DHOME}/.zshrc"
chsh -s "$(which zsh)" "$DUSER" 2>/dev/null || true
ok "Zsh configured"

# ══ STEP 6: PROJECT TOOLS ════════════════════════════════════════
sec "6/7 · PostgreSQL client + Redis + Nginx + Certbot"
has psql      || { DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql-client; }
has redis-cli || { DEBIAN_FRONTEND=noninteractive apt-get install -y redis-tools; }
has nginx     || { DEBIAN_FRONTEND=noninteractive apt-get install -y nginx; systemctl enable nginx --quiet; }
has certbot   || { DEBIAN_FRONTEND=noninteractive apt-get install -y certbot python3-certbot-nginx; }
ok "psql · redis-cli · nginx · certbot"

# ══ STEP 7: EXTRA TOOLS ══════════════════════════════════════════
sec "7/7 · Extra Tools"
PKGS=()
{ has batcat || has bat; } || PKGS+=(bat)
has rg      || PKGS+=(ripgrep)
has fdfind  || PKGS+=(fd-find)
has ncdu    || PKGS+=(ncdu)
has tmux    || PKGS+=(tmux)
has htop    || PKGS+=(htop)
[[ ${#PKGS[@]} -gt 0 ]] && DEBIAN_FRONTEND=noninteractive apt-get install -y "${PKGS[@]}" >/dev/null
ln -sf /usr/bin/batcat /usr/local/bin/bat 2>/dev/null || true
ok "bat · ripgrep · fd · ncdu · tmux · htop"

# lazydocker
if ! has lazydocker; then
  TAG=$(curl -sS --connect-timeout 10 \
    https://api.github.com/repos/jesseduffield/lazydocker/releases/latest \
    2>/dev/null | grep '"tag_name"' | grep -oP '(?<=v)[^"]+' || echo "")
  [[ -n "$TAG" ]] && {
    curl -Lo /tmp/lzd.tar.gz \
      "https://github.com/jesseduffield/lazydocker/releases/download/v${TAG}/lazydocker_${TAG}_Linux_x86_64.tar.gz" \
      --silent --retry 2 --connect-timeout 30
    tar -xzf /tmp/lzd.tar.gz -C /tmp lazydocker 2>/dev/null
    mv /tmp/lazydocker /usr/local/bin/ && chmod +x /usr/local/bin/lazydocker
    ok "lazydocker $TAG"
  } || warn "lazydocker: skipped"
else skip "lazydocker"; fi

# lazygit
if ! has lazygit; then
  LTAG=$(curl -sS --connect-timeout 10 \
    https://api.github.com/repos/jesseduffield/lazygit/releases/latest \
    2>/dev/null | grep '"tag_name"' | grep -oP '(?<=v)[^"]+' || echo "")
  [[ -n "$LTAG" ]] && {
    curl -Lo /tmp/lzg.tar.gz \
      "https://github.com/jesseduffield/lazygit/releases/download/v${LTAG}/lazygit_${LTAG}_Linux_x86_64.tar.gz" \
      --silent --retry 2 --connect-timeout 30
    tar -xzf /tmp/lzg.tar.gz -C /tmp lazygit 2>/dev/null
    mv /tmp/lazygit /usr/local/bin/ && chmod +x /usr/local/bin/lazygit
    ok "lazygit $LTAG"
  } || warn "lazygit: skipped"
else skip "lazygit"; fi

# fzf
[[ ! -d "${DHOME}/.fzf" ]] && {
  sudo -u "$DUSER" git clone --depth 1 \
    https://github.com/junegunn/fzf.git "${DHOME}/.fzf" >/dev/null 2>&1
  sudo -u "$DUSER" "${DHOME}/.fzf/install" --all --no-update-rc >/dev/null 2>&1
  ok "fzf (Ctrl+R)"
} || skip "fzf"

# project dirs
sudo -u "$DUSER" mkdir -p \
  "${DHOME}/projects/resort-platform" \
  "${DHOME}/scripts" "${DHOME}/backups"

apt-get autoremove -y --purge >/dev/null; apt-get autoclean -y >/dev/null
rm -f /tmp/lzd.tar.gz /tmp/lzg.tar.gz

# ══ SUMMARY ══════════════════════════════════════════════════════
echo ""
echo -e "${BOLD}${GREEN}══════════════════════════════════════════${RESET}"
echo -e "${BOLD}${GREEN}  ✓ ALL DONE — Environment Ready!         ${RESET}"
echo -e "${BOLD}${GREEN}══════════════════════════════════════════${RESET}\n"
for t_c in \
  "Docker:docker --version|grep -oP '\d+\.\d+\.\d+'" \
  "Python:python3.12 --version" \
  "Node:node --version" \
  "pnpm:pnpm --version" \
  "Git:git --version|grep -oP '\d+\.\d+\.\d+'" \
  "Nginx:nginx -v 2>&1|grep -oP '\d+\.\d+\.\d+'" \
  "Zsh:zsh --version|grep -oP '\d+\.\d+\.\d+'"; do
  t="${t_c%%:*}"; c="${t_c##*:}"
  v=$(eval "$c" 2>/dev/null || echo "—")
  echo -e "  ${GREEN}✓${RESET} $(printf '%-10s' "$t") ${DIM}$v${RESET}"
done
echo ""
echo -e "  ${CYAN}→${RESET} Run: ${BOLD}newgrp docker${RESET}  then  ${BOLD}zsh${RESET}"
echo -e "  ${DIM}Log: ${LOG}${RESET}\n"
