#!/usr/bin/env bash
# Claude Power Kit — macOS / Linux Installer
# Usage:
#   chmod +x install.sh
#   ./install.sh
#   ./install.sh --vault ~/path/to/obsidian --prompts ~/my-prompts

set -euo pipefail

VAULT_PATH=""
PROMPTS_DIR=""

# ── Parse args ────────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --vault)   VAULT_PATH="$2"; shift 2;;
        --prompts) PROMPTS_DIR="$2"; shift 2;;
        *) echo "Unknown arg: $1"; exit 1;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
SKILLS_DIR="$CLAUDE_DIR/skills"
CLAUDE_MD="$CLAUDE_DIR/CLAUDE.md"

echo ""
echo "======================================"
echo "  Claude Power Kit — macOS/Linux      "
echo "======================================"
echo ""

# ── Check Claude Code installed ───────────────────────────────────────────────
if [[ ! -d "$CLAUDE_DIR" ]]; then
    echo "[!] ~/.claude not found. Is Claude Code installed?"
    echo "    Install: https://claude.ai/claude-code"
    exit 1
fi

# ── Resolve prompts dir ───────────────────────────────────────────────────────
if [[ -z "$PROMPTS_DIR" ]]; then
    DEFAULT_PROMPTS="$HOME/.claude-powerkit/_prompts"
    echo "Where should prompt templates be stored?"
    echo "  Default: $DEFAULT_PROMPTS"
    read -r -p "  Press Enter to accept, or type a path: " input
    PROMPTS_DIR="${input:-$DEFAULT_PROMPTS}"
fi

# ── Copy prompt library ───────────────────────────────────────────────────────
echo ""
echo "[1/4] Installing prompt library to: $PROMPTS_DIR"

mkdir -p "$PROMPTS_DIR"

SOURCE_PROMPTS="$SCRIPT_DIR/_prompts"
if [[ -d "$SOURCE_PROMPTS" ]]; then
    cp -r "$SOURCE_PROMPTS/"* "$PROMPTS_DIR/"
    count=$(find "$PROMPTS_DIR" -name "*.md" | wc -l | tr -d ' ')
    echo "    Copied $count prompt category files."
else
    echo "[!] _prompts/ directory not found next to install.sh"
fi

# ── Install skill ─────────────────────────────────────────────────────────────
echo ""
echo "[2/4] Installing prompt-matcher skill..."

SKILL_DEST="$SKILLS_DIR/prompt-matcher"
mkdir -p "$SKILL_DEST"

SKILL_MD="$SCRIPT_DIR/SKILL.md"
if [[ -f "$SKILL_MD" ]]; then
    # Inject resolved prompts dir
    sed \
        -e "s|\[path to your _prompts folder\]|$PROMPTS_DIR|g" \
        -e "s|~/.claude-powerkit/_prompts/|$PROMPTS_DIR/|g" \
        "$SKILL_MD" > "$SKILL_DEST/SKILL.md"
    echo "    Skill installed at: $SKILL_DEST"
else
    echo "[!] SKILL.md not found"
fi

# ── Update CLAUDE.md ──────────────────────────────────────────────────────────
echo ""
echo "[3/4] Updating CLAUDE.md..."

PM_BLOCK="
# Prompt Matcher (always-on)
- Prompt library: \`$PROMPTS_DIR\`
- On EVERY task message (research, build, analyze, write, design, debug, audit), before executing: silently score the message against the prompt library. If any template scores 6+/10 relevance, use it — fill known variables from context, ask the user only for unknowns that can't be inferred. Show the matched prompt name in one line, then proceed.
- If all variables are inferable from context: fill the template silently and execute without asking.
- If nothing matches above 4/10: execute directly without the skill.
- Do NOT activate for: casual chat, vault saves, quick lookups, yes/no questions.
- Add new prompts to the library whenever a reusable pattern emerges from conversation.
"

if [[ -f "$CLAUDE_MD" ]]; then
    if grep -q "Prompt Matcher" "$CLAUDE_MD"; then
        echo "    CLAUDE.md already has Prompt Matcher section — skipping."
    else
        printf '%s\n' "$PM_BLOCK" >> "$CLAUDE_MD"
        echo "    Added Prompt Matcher section to CLAUDE.md."
    fi
else
    printf '%s\n' "$PM_BLOCK" > "$CLAUDE_MD"
    echo "    Created CLAUDE.md with Prompt Matcher section."
fi

# ── Optional: Obsidian vault symlink ─────────────────────────────────────────
echo ""
echo "[4/4] Obsidian Brain (optional)"
echo "    This step creates a memory vault Claude reads at session start."

if [[ -z "$VAULT_PATH" ]]; then
    read -r -p "    Enter your Obsidian vault path (or press Enter to skip): " vault_input
    VAULT_PATH="${vault_input:-}"
fi

if [[ -n "$VAULT_PATH" && -d "$VAULT_PATH" ]]; then
    BRAIN_DEST="$CLAUDE_DIR/projects/brain"
    if [[ -L "$BRAIN_DEST" || -d "$BRAIN_DEST" ]]; then
        echo "    Brain symlink already exists at $BRAIN_DEST — skipping."
    else
        mkdir -p "$(dirname "$BRAIN_DEST")"
        ln -s "$VAULT_PATH" "$BRAIN_DEST"
        echo "    Symlink created: $BRAIN_DEST -> $VAULT_PATH"
    fi

    BRAIN_BLOCK="
# Brain (always-on)
- Vault: \`$BRAIN_DEST\`
- At the START of every session, read Brain/CRITICAL_FACTS.md if it exists.
- Treat the brain as authoritative for identity, active projects, and durable preferences.
- When conversation produces something durable (decision, task, lesson, finding), save it to the vault.
"
    if ! grep -q "Brain (always-on)" "$CLAUDE_MD"; then
        printf '%s\n' "$BRAIN_BLOCK" >> "$CLAUDE_MD"
        echo "    Added Brain section to CLAUDE.md."
    fi
elif [[ -n "$VAULT_PATH" ]]; then
    echo "    [!] Path not found: $VAULT_PATH — skipping vault setup."
else
    echo "    Skipped. Re-run with --vault ~/path/to/vault later."
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "======================================"
echo "  Installation complete!"
echo "======================================"
echo ""
echo "Restart Claude Code for changes to take effect."
echo ""
echo "Prompt library: $PROMPTS_DIR"
echo "Skill:          $SKILL_DEST"
echo "CLAUDE.md:      $CLAUDE_MD"
echo ""
echo "Test it: Open Claude Code and type any task — Claude will auto-match a prompt."
echo ""
