param(
    [string]$Toolset = '',
    [string]$WindowsSdk = '10.0.26100.0',
    [ValidateRange(1,64)][int]$Jobs = 4
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot
$work = Join-Path $repo '.work'
$null = New-Item -ItemType Directory -Force -Path "$work/bin","$work/logs"
$clean = Join-Path $PSScriptRoot 'run-clean-env.py'
function Run-Checked([string[]]$Command) {
    & python $clean @Command
    if ($LASTEXITCODE) { throw "Command failed ($LASTEXITCODE): $($Command[0])" }
}
Run-Checked @('python', (Join-Path $PSScriptRoot 'pipeline.py'), 'prepare')
$lock = Get-Content -LiteralPath (Join-Path $repo 'sources.lock.json') -Raw | ConvertFrom-Json
$ra = Join-Path "$work/sources" $lock.retroarch.directory
$fb = Join-Path "$work/sources" $lock.fbneo.directory
$vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio/Installer/vswhere.exe'
if (!(Test-Path -LiteralPath $vswhere)) { throw 'Install Visual Studio C++ tools with ARM64 support before building.' }
$vs = (& $vswhere -latest -products '*' -format json | ConvertFrom-Json)[0]
if (!$vs) { throw 'Visual Studio was not found.' }
$major = [int]($vs.installationVersion.Split('.')[0])
if ($major -ge 18) { $generator = 'Visual Studio 18 2026'; $defaultToolset = 'v145' }
elseif ($major -eq 17) { $generator = 'Visual Studio 17 2022'; $defaultToolset = 'v143' }
else { throw 'Visual Studio 2022 or 2026 is required.' }
if (!$Toolset) { $Toolset = $defaultToolset }
$msbuild = Join-Path $vs.installationPath 'MSBuild/Current/Bin/arm64/MSBuild.exe'
if (!(Test-Path -LiteralPath $msbuild)) { $msbuild = Join-Path $vs.installationPath 'MSBuild/Current/Bin/MSBuild.exe' }
Run-Checked @($msbuild, "$ra/pkg/msvc/RetroArch-msvc2022.sln", "/m:$Jobs", '/nologo', '/v:minimal', '/p:Configuration=Release', '/p:Platform=ARM64', "/p:PlatformToolset=$Toolset", '/p:PreferredToolArchitecture=arm64', "/p:WindowsTargetPlatformVersion=$WindowsSdk", '/fl', "/flp:logfile=$work/logs/retroarch-build.log;verbosity=normal")
Run-Checked @('cmake', '-S', $fb, '-B', "$work/fbneo-build", '-G', $generator, '-A', 'ARM64', '-T', $Toolset, "-DCMAKE_GENERATOR_INSTANCE=$($vs.installationPath)", "-DCMAKE_SYSTEM_VERSION=$WindowsSdk")
Run-Checked @('cmake', '--build', "$work/fbneo-build", '--config', 'Release', '--parallel', "$Jobs", '--', '/nologo', '/v:minimal', '/p:PreferredToolArchitecture=arm64')
Copy-Item -LiteralPath "$ra/pkg/msvc/ARM64/Release/RetroArch-msvc2022.exe" -Destination "$work/bin/retroarch.exe"
Copy-Item -LiteralPath "$work/fbneo-build/Release/fbneo_libretro.dll" -Destination "$work/bin/fbneo_libretro.dll"
$revision = & git -C $repo rev-parse HEAD 2>$null
if ($LASTEXITCODE) { $revision = 'uncommitted' }
@{
    built_at_utc = [DateTime]::UtcNow.ToString('o')
    visual_studio = $vs.installationVersion
    toolset = $Toolset
    windows_sdk = $WindowsSdk
    architecture = 'ARM64'
    crt = 'static'
    build_repository_revision = $revision
    verification = 'See the workflow run and docs/VALIDATION.md; no gameplay claim.'
} | ConvertTo-Json | Set-Content -LiteralPath "$work/build-info.json" -Encoding utf8
Write-Output "Built ARM64 binaries in $work/bin"
