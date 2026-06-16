#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
#  Quality Engineering Statistical Analyzer — Setup & Launch Script
#  setup.sh
#
#  Created by : ENG-2518885
#  Email      : meharibrhanu233@gmail.com
#  Profession : Mechanical Engineer
#
#  Usage      : chmod +x setup.sh && ./setup.sh
#
#  What this script does:
#   1. Validates Python 3 and pip are installed
#   2. Creates an isolated virtual environment (.venv)
#   3. Upgrades pip inside the venv
#   4. Installs all dependencies from requirements.txt
#   5. Validates Flask app for syntax errors
#   6. Detects the machine's local network IP address
#   7. Launches the Flask server on 0.0.0.0:5000
# ══════════════════════════════════════════════════════════════════════════════

set -euo pipefail  # Exit on error, unset variable, or pipe failure

# ─── Color codes for terminal output ─────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# ─── Banner ───────────────────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════════════════╗${RESET}"
echo -e "${CYAN}${BOLD}║     Quality Engineering Statistical Analyzer v1.0   ║${RESET}"
echo -e "${CYAN}${BOLD}║     Created by: ENG-2518885 · Mech. Engineer        ║${RESET}"
echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════════════╝${RESET}"
echo ""

# ─── STEP 1: Check Python 3 ──────────────────────────────────────────────────
echo -e "${BOLD}[1/6]${RESET} Checking Python 3 installation…"

if ! command -v python3 &>/dev/null; then
    echo -e "${RED}✗ ERROR: python3 is not installed or not in PATH.${RESET}"
    echo -e "  Install Python 3.11+ from: ${CYAN}https://www.python.org/downloads/${RESET}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [[ "$PYTHON_MAJOR" -lt 3 ]] || { [[ "$PYTHON_MAJOR" -eq 3 ]] && [[ "$PYTHON_MINOR" -lt 9 ]]; }; then
    echo -e "${RED}✗ ERROR: Python 3.9+ is required. Found: ${PYTHON_VERSION}${RESET}"
    exit 1
fi

echo -e "${GREEN}✓ Python ${PYTHON_VERSION} detected${RESET}"

# ─── STEP 2: Check pip ────────────────────────────────────────────────────────
echo -e "${BOLD}[2/6]${RESET} Checking pip installation…"

if ! python3 -m pip --version &>/dev/null; then
    echo -e "${RED}✗ ERROR: pip is not available. Install it with:${RESET}"
    echo "  python3 -m ensurepip --upgrade"
    exit 1
fi

PIP_VERSION=$(python3 -m pip --version | awk '{print $2}')
echo -e "${GREEN}✓ pip ${PIP_VERSION} detected${RESET}"

# ─── Locate script directory ──────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"
REQUIREMENTS="${SCRIPT_DIR}/requirements.txt"
APP_FILE="${SCRIPT_DIR}/app.py"

# Validate required files exist
for required_file in "$APP_FILE" "$REQUIREMENTS"; do
    if [[ ! -f "$required_file" ]]; then
        echo -e "${RED}✗ ERROR: Required file not found: ${required_file}${RESET}"
        exit 1
    fi
done

# ─── STEP 3: Create virtual environment ───────────────────────────────────────
echo -e "${BOLD}[3/6]${RESET} Creating isolated virtual environment at .venv…"

if [[ -d "$VENV_DIR" ]]; then
    echo -e "${YELLOW}  ⚠ Existing .venv found — reusing it (delete .venv to force rebuild)${RESET}"
else
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✓ Virtual environment created${RESET}"
fi

# Activate the virtual environment
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"
echo -e "${GREEN}✓ Virtual environment activated${RESET}"

# ─── STEP 4: Upgrade pip inside venv ──────────────────────────────────────────
echo -e "${BOLD}[4/6]${RESET} Upgrading pip inside virtual environment…"
python -m pip install --upgrade pip --quiet
echo -e "${GREEN}✓ pip upgraded to $(pip --version | awk '{print $2}')${RESET}"

# ─── STEP 5: Install dependencies ─────────────────────────────────────────────
echo -e "${BOLD}[5/6]${RESET} Installing dependencies from requirements.txt…"
pip install -r "$REQUIREMENTS" --quiet

# Verify critical packages
echo -e "${BOLD}     Verifying installed packages:${RESET}"
PACKAGES=("flask" "numpy" "pandas" "scipy")
ALL_OK=true
for pkg in "${PACKAGES[@]}"; do
    if python -c "import ${pkg}" 2>/dev/null; then
        VERSION=$(python -c "import ${pkg}; print(${pkg}.__version__)" 2>/dev/null || echo "unknown")
        echo -e "     ${GREEN}✓${RESET} ${pkg} (${VERSION})"
    else
        echo -e "     ${RED}✗ FAILED to import: ${pkg}${RESET}"
        ALL_OK=false
    fi
done

if [[ "$ALL_OK" == "false" ]]; then
    echo -e "${RED}✗ One or more packages failed to install. Check the output above.${RESET}"
    exit 1
fi

# ─── STEP 6: Syntax validation ────────────────────────────────────────────────
echo -e "${BOLD}[6/6]${RESET} Validating Flask application for syntax errors…"

if python -m py_compile "$APP_FILE" 2>/dev/null; then
    echo -e "${GREEN}✓ app.py syntax is valid${RESET}"
else
    echo -e "${RED}✗ ERROR: app.py has syntax errors:${RESET}"
    python -m py_compile "$APP_FILE"
    exit 1
fi

# Quick Flask import test
if python -c "
import sys
sys.path.insert(0, '${SCRIPT_DIR}')
from flask import Flask
app = Flask(__name__)
print('Flask import OK')
" 2>/dev/null | grep -q "Flask import OK"; then
    echo -e "${GREEN}✓ Flask initializes correctly${RESET}"
else
    echo -e "${RED}✗ Flask initialization check failed${RESET}"
    exit 1
fi

# ─── Detect local network IP ──────────────────────────────────────────────────
echo ""
echo -e "${BOLD}Detecting local network IP address…${RESET}"

LOCAL_IP=""

# Try multiple methods across Linux/macOS
if command -v hostname &>/dev/null; then
    LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || true)
fi

if [[ -z "$LOCAL_IP" ]] || [[ "$LOCAL_IP" == "127.0.0.1" ]]; then
    # macOS fallback
    if command -v ipconfig &>/dev/null; then
        LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || true)
    fi
fi

if [[ -z "$LOCAL_IP" ]] || [[ "$LOCAL_IP" == "127.0.0.1" ]]; then
    # Linux fallback: use ip route
    if command -v ip &>/dev/null; then
        LOCAL_IP=$(ip route get 1.1.1.1 2>/dev/null | awk '/src/{print $7}' | head -1 || true)
    fi
fi

if [[ -z "$LOCAL_IP" ]]; then
    LOCAL_IP="<YOUR_LOCAL_IP>"
fi

# ─── Launch summary ───────────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}${BOLD}══════════════════════════════════════════════════════${RESET}"
echo -e "${BOLD}  🚀 Launching Quality Engineering Analyzer…${RESET}"
echo -e "${CYAN}${BOLD}══════════════════════════════════════════════════════${RESET}"
echo ""
echo -e "  ${BOLD}Local Machine URL:${RESET}  ${GREEN}http://127.0.0.1:5000${RESET}"
echo -e "  ${BOLD}Mobile Device URL:${RESET}  ${YELLOW}${BOLD}http://${LOCAL_IP}:5000${RESET}"
echo ""
echo -e "  ${BOLD}📱 On your smartphone, open:${RESET}"
echo -e "     ${YELLOW}${BOLD}http://${LOCAL_IP}:5000${RESET}"
echo -e "  ${BOLD}(Ensure your phone is on the same Wi-Fi network)${RESET}"
echo ""
echo -e "  Press ${BOLD}Ctrl+C${RESET} to stop the server."
echo -e "${CYAN}${BOLD}══════════════════════════════════════════════════════${RESET}"
echo ""

# ─── Set Flask environment variables ──────────────────────────────────────────
export FLASK_APP=app.py
export FLASK_ENV=production
export FLASK_DEBUG=0

# ─── Launch server ────────────────────────────────────────────────────────────
cd "$SCRIPT_DIR"
python -m flask run \
    --host=0.0.0.0 \
    --port=5000 \
    --no-debugger \
    --no-reload

# Trap clean exit
trap 'echo -e "\n${YELLOW}Server stopped. Deactivating virtual environment.${RESET}"; deactivate' EXIT
