param(
    [string]$Url = "",
    [string]$Pat = $env:GITLAB_PAT,
    [string]$HostUrl = "https://gitlab.com",
    [string]$Executor = "shell",
    [string]$Image = "alpine:latest",
    [string]$Tags = ""
)

$ErrorActionPreference = "Stop"

Write-Host "Starting Windows GitLab Runner Setup..." -ForegroundColor Cyan

# ─── Resolve project URL ──────────────────────────────────────────────────────
if ([string]::IsNullOrWhiteSpace($Url)) {
    try {
        $remote = git remote get-url origin 2>$null
        if ($remote) {
            # Convert git@gitlab.com:user/repo.git to https://gitlab.com/user/repo
            $Url = $remote -replace "^git@([^:]+):(.+)\.git$", "https://`$1/`$2" -replace "\.git$", ""
        }
    } catch {}
}

if ([string]::IsNullOrWhiteSpace($Url)) {
    Write-Host "[ERROR] Could not determine project URL. Pass -Url <repo-url>" -ForegroundColor Red
    exit 1
}

# ─── Get PAT ──────────────────────────────────────────────────────────────────
if ([string]::IsNullOrWhiteSpace($Pat)) {
    Write-Host "A Personal Access Token (PAT) with 'api' scope is required" -ForegroundColor Yellow
    $Pat = Read-Host "Paste your GitLab PAT (Input will be hidden)" -AsSecureString
    $Pat = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Pat))
}

if ([string]::IsNullOrWhiteSpace($Pat)) {
    Write-Host "[ERROR] PAT cannot be empty." -ForegroundColor Red
    exit 1
}

# ─── Install gitlab-runner ────────────────────────────────────────────────────
$runnerDir = "C:\GitLab-Runner"
$runnerExe = "$runnerDir\gitlab-runner.exe"

if (-Not (Test-Path $runnerExe)) {
    Write-Host "[INFO] gitlab-runner not found. Downloading..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Force -Path $runnerDir | Out-Null
    $downloadUrl = "https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-windows-amd64.exe"
    Invoke-WebRequest -Uri $downloadUrl -OutFile $runnerExe
    Write-Host "[OK] gitlab-runner downloaded to $runnerExe" -ForegroundColor Green
} else {
    Write-Host "[OK] gitlab-runner already exists at $runnerExe" -ForegroundColor Green
}

# ─── Fetch project ID via GitLab API ─────────────────────────────────────────
Write-Host "[INFO] Fetching project info..." -ForegroundColor Cyan

# Extract "group/repo" from URL
$projectPath = $Url -replace "^$([regex]::Escape($HostUrl))/?", ""
# URL encode the path (replace / with %2F)
$encodedPath = [uri]::EscapeDataString($projectPath)

$headers = @{ "PRIVATE-TOKEN" = $Pat }
$projectApiUrl = "$HostUrl/api/v4/projects/$encodedPath"

try {
    $response = Invoke-RestMethod -Uri $projectApiUrl -Headers $headers -Method Get
    $projectId = $response.id
    Write-Host "[OK] Project ID: $projectId" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Could not fetch project info. Check your PAT scope and URL." -ForegroundColor Red
    exit 1
}

# ─── Create runner token via API ──────────────────────────────────────────────
Write-Host "[INFO] Creating runner token via API for project ID $projectId..." -ForegroundColor Cyan

$runnerName = ($projectPath -replace '/', '-').ToLower()
$tokenBody = @{
    runner_type = "project_type"
    project_id = $projectId
    description = $runnerName
    tag_list = $Tags
    run_untagged = $true
} | ConvertTo-Json

$tokenApiUrl = "$HostUrl/api/v4/user/runners"

try {
    $tokenResponse = Invoke-RestMethod -Uri $tokenApiUrl -Headers $headers -Method Post -Body $tokenBody -ContentType "application/json"
    $runnerToken = $tokenResponse.token
    Write-Host "[OK] Runner token obtained." -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Failed to create runner token." -ForegroundColor Red
    exit 1
}

# ─── Register the runner ──────────────────────────────────────────────────────
Write-Host "[INFO] Registering runner '$runnerName'..." -ForegroundColor Cyan

$registerArgs = @(
    "register",
    "--non-interactive",
    "--url", $HostUrl,
    "--token", $runnerToken,
    "--name", $runnerName,
    "--executor", $Executor
)

if (-Not [string]::IsNullOrWhiteSpace($Tags)) {
    $registerArgs += "--tag-list"
    $registerArgs += $Tags
}

if ($Executor -eq "docker") {
    $registerArgs += "--docker-image"
    $registerArgs += $Image
}

& $runnerExe $registerArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Runner registered." -ForegroundColor Green
} else {
    Write-Host "[ERROR] Registration failed." -ForegroundColor Red
    exit 1
}

# ─── Start the runner ───────────────────────────────────────────────────────
Write-Host "[INFO] Installing and starting runner service..." -ForegroundColor Cyan
& $runnerExe install
& $runnerExe start

Write-Host "`n[OK] Done! Runner '$runnerName' is registered and running as a Windows Service." -ForegroundColor Green
Write-Host "CI/CD settings : $Url/-/settings/ci_cd"
