# RetroArch for Windows ARM64 — community builds

Native ARM64 RetroArch and a separately packaged FinalBurn Neo arcade core.
These unofficial builds use RetroArch 1.22.2 and a pinned FBNeo revision.

[Downloads](https://github.com/dakehero/retroarch-windows-arm64/releases) ·
[Build status](https://github.com/dakehero/retroarch-windows-arm64/actions/workflows/build.yml) ·
[Licenses](THIRD_PARTY_NOTICES.md) · [Validation](docs/VALIDATION.md)

## Getting started

1. Download and extract `RetroArch-1.22.2-Windows-ARM64.zip`.
2. For FBNeo, also download `FBNeo-Windows-ARM64.zip` and merge its `cores` and
   `info` directories into the RetroArch directory.
3. Run `retroarch.exe`. Defaults are the Ozone menu, Simplified Chinese, D3D11
   video, and WASAPI audio. Change the menu language under Settings → User → Language.
4. Load your own legally obtained game content. No ROMs or BIOS files are included.

The ARM64 frontend requires ARM64 cores; it cannot load x64 or x86 cores.
This project does not host a complete core download service. Install the FBNeo
core manually as described above. See [the usage guide](docs/USAGE.md).

## Build locally

Requirements already installed: Windows ARM64, PowerShell 7, native ARM64 Python
3.12+, Git, CMake 4.0+ (4.2+ for VS 2026), Visual Studio 2022/2026 C++ ARM64 tools,
and Windows SDK 10.0.26100.0. The scripts do not install tools or modify system PATH.
VS 2026 uses v145; VS 2022 uses v143. CI uses the VS 2026 ARM64 runner image.

```powershell
pwsh -NoProfile -File scripts/Build.ps1
python scripts/pipeline.py assets
python scripts/smoke.py
python scripts/smoke.py --graphics  # Requires a local GPU and audio device
python scripts/pipeline.py package
```

Downloads and intermediate files go to `.work/`; release files go to `dist/`.
Upstream inputs are pinned in `sources.lock.json` and verified using SHA-256 or
Git blob hashes. `manifests/fbneo.json` is generated from the pinned upstream GNU
Make manifests, preserving source and include search order. Ordinary builds do
not require GNU Make. See [build maintenance](docs/BUILD.md).

Each release includes separate binary ZIPs, complete patched source archives,
build scripts, and SHA-256 checksums. Extract the source archives under
`.work/sources/` to inspect or rebuild those exact trees. Compiler revisions and
build timestamps can change binary hashes; byte-for-byte reproducibility is not claimed.

## CI and publishing

Pushes and pull requests build both ARM64 binaries and run ABI and frontend/core
integration smoke checks on a Windows ARM64 runner. These use null video with audio disabled;
they do not validate GPU drivers, audio hardware, controllers, or game compatibility.

A `v*` tag runs the same build/checks, then creates a **draft prerelease** containing
both binary packages, matching sources, build scripts, and checksums. The maintainer
reviews the draft before publishing it. Successful CI artifacts alone are not a
public release. Graphics and audio hardware checks require separate local testing.

## Scope and licensing

RetroArch already supports Windows ARM64 upstream. This repository provides
packaging, pinned build inputs, small compatibility fixes, and explicit validation.

Original scripts and documentation: MIT. RetroArch: GPL-3.0-or-later. FBNeo:
custom noncommercial terms, including restrictions on profit and donations.
Assets and fonts retain their own licenses. The script license does not relicense
these components. See [the full notices](THIRD_PARTY_NOTICES.md).
