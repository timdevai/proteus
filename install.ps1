#!/usr/bin/env pwsh
# Proteus — Windows Installer
# Run from an elevated PowerShell terminal:
#   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
#   .\install.ps1

param(
    [string]$VaultPath  = "",
    [string]$PromptsDir = "",
    [string]$UserName   = ""
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Proteus — Windows Install           " -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# ── Claude Code ───────────────────────────────────────────────────────────────
$ClaudeDir = Join-Path $env:USERPROFILE ".claude"
$SkillsDir = Join-Path $ClaudeDir "skills"
$ClaudeMd  = Join-Path $ClaudeDir "CLAUDE.md"

if (-not (Test-Path $ClaudeDir)) {
    Write-Host "[!] ~/.claude not found. Install Claude Code first:" -ForegroundColor Red
    Write-Host "    https://claude.ai/code" -ForegroundColor Yellow
    exit 1
}

# ── Python 3.8+ ───────────────────────────────────────────────────────────────
Write-Host "[check] Python 3.8+" -ForegroundColor Cyan
$pythonCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python 3\.([89]|1[0-9])") {
            $pythonCmd = $cmd
            Write-Host "    Found: $ver" -ForegroundColor Gray
            break
        }
    } catch { }
}
if (-not $pythonCmd) {
    Write-Host "[!] Python 3.8+ not found. Install from https://python.org and re-run." -ForegroundColor Red
    exit 1
}

# ── Ollama (non-blocking — warns, does not exit) ──────────────────────────────
Write-Host "[check] Ollama" -ForegroundColor Cyan
$ollamaOk = $false
try {
    $ollamaVer = & ollama --version 2>&1
    Write-Host "    Found: $ollamaVer" -ForegroundColor Gray
    $ollamaOk = $true
} catch {
    Write-Host "    [!] Ollama not found. Tier 0 filter disabled — API costs ~4x higher." -ForegroundColor Yellow
    Write-Host "    Install: https://ollama.ai  then run: ollama pull qwen2.5:1.5b" -ForegroundColor Yellow
}

# ── Resolve prompts directory ─────────────────────────────────────────────────
if (-not $PromptsDir) {
    $DefaultPromptsDir = Join-Path $env:USERPROFILE ".proteus" "_prompts"
    Write-Host ""
    Write-Host "Where should prompt templates be stored?"
    Write-Host "  Default: $DefaultPromptsDir"
    $userInput = Read-Host "  Press Enter to accept, or type a path"
    $PromptsDir = if ($userInput.Trim()) { $userInput.Trim() } else { $DefaultPromptsDir }
}

# ── Create ~/.proteus/ data dir + .env ───────────────────────────────────────
$ProteusData = Join-Path $env:USERPROFILE ".proteus"
New-Item -ItemType Directory -Force -Path $ProteusData | Out-Null
Write-Host ""
Write-Host "[1/5] Proteus data dir: $ProteusData" -ForegroundColor Green

$EnvFile = Join-Path $ProteusData ".env"
$existingEnv = if (Test-Path $EnvFile) { Get-Content $EnvFile -Raw } else { "" }
if ($existingEnv -notmatch "ANTHROPIC_API_KEY") {
    Write-Host ""
    Write-Host "  Anthropic API key required for AI agents." -ForegroundColor Cyan
    Write-Host "  Get yours at: https://console.anthropic.com/settings/keys" -ForegroundColor Cyan
    $apiKey = Read-Host "  Paste your ANTHROPIC_API_KEY (or press Enter to skip and set later)"
    if ($apiKey.Trim()) {
        Add-Content -Path $EnvFile -Value "ANTHROPIC_API_KEY=$($apiKey.Trim())" -Encoding UTF8
        Write-Host "    Saved to $EnvFile" -ForegroundColor Gray
    } else {
        Write-Host "    Skipped. Add ANTHROPIC_API_KEY=$env:USERPROFILE\.proteus\.env later." -ForegroundColor Yellow
    }
} else {
    Write-Host "    API key already configured." -ForegroundColor Gray
}

# ── User name (used by Admin + Research agent prompts) ────────────────────────
if ($existingEnv -notmatch "PROTEUS_USER_NAME") {
    if (-not $UserName) {
        Write-Host ""
        Write-Host "  What should the agents call you? (first name is fine)" -ForegroundColor Cyan
        $UserName = Read-Host "  Name (press Enter to use 'the user')"
    }
    $UserName = $UserName.Trim()
    if ($UserName) {
        Add-Content -Path $EnvFile -Value "PROTEUS_USER_NAME=$UserName" -Encoding UTF8
        Write-Host "    Agents will address you as: $UserName" -ForegroundColor Gray
    } else {
        Write-Host "    Skipped. Agents will use the default 'the user'." -ForegroundColor Yellow
    }
}

# ── Copy prompt library ───────────────────────────────────────────────────────
Write-Host ""
Write-Host "[2/5] Installing prompt library to: $PromptsDir" -ForegroundColor Green

New-Item -ItemType Directory -Force -Path $PromptsDir | Out-Null

$SourcePrompts = Join-Path $PSScriptRoot "_prompts"
if ($PSScriptRoot -and (Test-Path $SourcePrompts)) {
    Copy-Item -Path (Join-Path $SourcePrompts "*") -Destination $PromptsDir -Recurse -Force
    $count = (Get-ChildItem $PromptsDir -Filter "*.md").Count
    Write-Host "    Copied $count prompt category files." -ForegroundColor Gray
} else {
    Write-Host "    [!] _prompts/ not found next to install.ps1 — skipping." -ForegroundColor Yellow
}

# ── Install Python dependencies ───────────────────────────────────────────────
Write-Host ""
Write-Host "[3/5] Installing Python dependencies..." -ForegroundColor Green
$ReqFile = Join-Path $PSScriptRoot "requirements.txt"
if ($PSScriptRoot -and (Test-Path $ReqFile)) {
    & $pythonCmd -m pip install -r $ReqFile --quiet
    Write-Host "    Dependencies installed." -ForegroundColor Gray
} else {
    Write-Host "    [!] requirements.txt not found — skipping pip install." -ForegroundColor Yellow
}

# ── Install skill ─────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "[4/5] Installing prompt-matcher skill..." -ForegroundColor Green

$SkillDest = Join-Path $SkillsDir "prompt-matcher"
New-Item -ItemType Directory -Force -Path $SkillDest | Out-Null

$SkillMd = Join-Path $PSScriptRoot "SKILL.md"
if ($PSScriptRoot -and (Test-Path $SkillMd)) {
    $content = Get-Content $SkillMd -Raw
    $content = $content -replace '\[path to your _prompts folder\]', $PromptsDir
    $content = $content -replace '~/.claude-powerkit/_prompts/', $PromptsDir.Replace('\','/')
    $content = $content -replace '\{PROMPTS_DIR\}', $PromptsDir
    Set-Content -Path (Join-Path $SkillDest "SKILL.md") -Value $content -Encoding UTF8
    Write-Host "    Skill installed at: $SkillDest" -ForegroundColor Gray
} else {
    Write-Host "    [!] SKILL.md not found." -ForegroundColor Yellow
}

# ── Update CLAUDE.md ──────────────────────────────────────────────────────────
Write-Host ""
Write-Host "[5/5] Updating CLAUDE.md..." -ForegroundColor Green

# Behavioral spine — discipline rules + two-tier memory. The highest-leverage layer.
$SpineSrc = Join-Path $PSScriptRoot "claude-md\spine.md"
if ($PSScriptRoot -and (Test-Path $SpineSrc)) {
    $spineHas = (Test-Path $ClaudeMd) -and ((Get-Content $ClaudeMd -Raw) -match "# Response Rules")
    if ($spineHas) {
        Write-Host "    CLAUDE.md already has the behavioral spine — skipping." -ForegroundColor Gray
    } else {
        Add-Content -Path $ClaudeMd -Value ("`r`n" + (Get-Content $SpineSrc -Raw)) -Encoding UTF8
        Write-Host "    Added behavioral spine (Response Rules / Tool Efficiency / Execution Quality / Memory)." -ForegroundColor Gray
    }
}

$pmBlock = @"

# Prompt Matcher (always-on)
- Prompt library: ``$($PromptsDir.Replace('\','\\'))``
- On EVERY task message (research, build, analyze, write, design, debug, audit), before executing: silently score the message against the prompt library. If any template scores 6+/10 relevance, use it — fill known variables from context, ask the user only for unknowns that can't be inferred. Show the matched prompt name in one line, then proceed.
- If all variables are inferable from context: fill the template silently and execute without asking.
- If nothing matches above 4/10: execute directly without the skill.
- Do NOT activate for: casual chat, vault saves, quick lookups, yes/no questions.
- Add new prompts to the library whenever a reusable pattern emerges from conversation.
"@

if (Test-Path $ClaudeMd) {
    $existing = Get-Content $ClaudeMd -Raw
    if ($existing -match "Prompt Matcher") {
        Write-Host "    CLAUDE.md already has Prompt Matcher section — skipping." -ForegroundColor Gray
    } else {
        Add-Content -Path $ClaudeMd -Value $pmBlock -Encoding UTF8
        Write-Host "    Added Prompt Matcher section to CLAUDE.md." -ForegroundColor Gray
    }
} else {
    Set-Content -Path $ClaudeMd -Value $pmBlock.TrimStart() -Encoding UTF8
    Write-Host "    Created CLAUDE.md." -ForegroundColor Gray
}

# ── Optional: Obsidian vault junction ─────────────────────────────────────────
if (-not $VaultPath) {
    $vaultInput = Read-Host "    Obsidian vault path for Brain memory (Enter to skip)"
    $VaultPath = $vaultInput.Trim()
}

if ($VaultPath -and (Test-Path $VaultPath)) {
    $BrainDest = Join-Path $ClaudeDir "projects\brain"
    if (Test-Path $BrainDest) {
        Write-Host "    Brain junction already exists — skipping." -ForegroundColor Gray
    } else {
        New-Item -ItemType Directory -Force -Path (Split-Path $BrainDest) | Out-Null
        cmd /c "mklink /J `"$BrainDest`" `"$VaultPath`"" 2>&1 | Out-Null
        Write-Host "    Junction: $BrainDest -> $VaultPath" -ForegroundColor Gray
    }
    $brainBlock = @"

# Brain (always-on)
- Vault: ``$($BrainDest.Replace('\','\\'))``
- At the START of every session, read Brain\CRITICAL_FACTS.md if it exists.
- Treat the brain as authoritative for identity, active projects, and durable preferences.
- When conversation produces something durable (decision, task, lesson, finding), save it to the vault.
"@
    $existing = Get-Content $ClaudeMd -Raw
    if ($existing -notmatch "Brain \(always-on\)") {
        Add-Content -Path $ClaudeMd -Value $brainBlock -Encoding UTF8
        Write-Host "    Added Brain section to CLAUDE.md." -ForegroundColor Gray
    }
} elseif ($VaultPath) {
    Write-Host "    [!] Vault path not found: $VaultPath — skipping." -ForegroundColor Yellow
}

# ── Done ──────────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Proteus installed!" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Restart Claude Code for changes to take effect." -ForegroundColor White
Write-Host ""
Write-Host "Prompt library : $PromptsDir" -ForegroundColor Gray
Write-Host "Skill          : $SkillDest"  -ForegroundColor Gray
Write-Host "CLAUDE.md      : $ClaudeMd"   -ForegroundColor Gray
Write-Host "Data dir       : $ProteusData" -ForegroundColor Gray
if ($ollamaOk) {
    Write-Host "Ollama         : ready (run 'ollama pull qwen2.5:1.5b' if not yet pulled)" -ForegroundColor Gray
} else {
    Write-Host "Ollama         : NOT installed (see warning above)" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "To launch Proteus: python proteus.py" -ForegroundColor White
Write-Host ""
