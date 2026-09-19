# RetroArch for Windows ARM64 — community builds

Native ARM64 RetroArch and a separately packaged FinalBurn Neo libretro core.
Unofficial; based on upstream RetroArch 1.22.2 and pinned FBNeo sources.

[Downloads](https://github.com/dakehero/retroarch-windows-arm64/releases) ·
[Build workflow](https://github.com/dakehero/retroarch-windows-arm64/actions/workflows/build.yml) ·
[Licenses](THIRD_PARTY_NOTICES.md) · [Validation](docs/VALIDATION.md)

## 使用

1. 下载并解压 `RetroArch-1.22.2-Windows-ARM64.zip`。
2. 如需 FBNeo，再下载 `FBNeo-Windows-ARM64.zip`，把其中的 `cores`、`info` 合并到 RetroArch 目录。
3. 运行 `retroarch.exe`。默认使用 Ozone 简体中文菜单、D3D11 和 WASAPI。
4. 使用自己有权使用的游戏内容。包内没有 ROM 或 BIOS。

Windows ARM64 主程序必须使用 ARM64 核心，不能加载 x64/x86 核心。
本项目不提供完整核心下载服务器；FBNeo 按上述方式手动安装。
参见 [使用说明](docs/USAGE.md)。

## Build locally

Requirements already installed: Windows ARM64, PowerShell 7, native ARM64 Python
3.12+, Git, CMake 4.0+ (4.2+ for VS 2026), Visual Studio 2022/2026 C++ ARM64 tools,
and Windows SDK 10.0.26100.0. The scripts do not install tools or modify system PATH.
VS 2026 uses v145; VS 2022 uses v143. The workflow uses the VS 2026 ARM64 image.

```powershell
pwsh -NoProfile -File scripts/Build.ps1
python scripts/pipeline.py assets
python scripts/smoke.py
python scripts/smoke.py --graphics  # local GPU and sound device required
python scripts/pipeline.py package
```

Downloads and work files go to `.work/`; release files go to `dist/`.
All upstream inputs are pinned in `sources.lock.json` and verified using SHA-256
or Git blob hashes. `manifests/fbneo.json` is generated from the pinned upstream
GNU Make manifests, with source/include order preserved. Ordinary builds need
no GNU Make installation. See [manifest maintenance](docs/BUILD.md).

Each release includes separate binary ZIPs, complete patched source archives,
the build scripts, and SHA-256 checksums. Extract the source archives under
`.work/sources/` to inspect or rebuild those exact patched trees. Exact binary
hashes may vary with compiler revisions and build timestamps.

## CI and publishing

Pushes and pull requests build both ARM64 binaries and run ABI/integration smoke
checks on a Windows ARM64 runner. These use null video/audio; they do not validate
GPU drivers, audio hardware, gamepads, or actual game compatibility.

A `v*` tag runs the same build/checks, then creates a **draft prerelease** containing
both binary packages, matching sources, build scripts and checksums. The maintainer
reviews the draft and publishes it. Successful CI artifacts alone are not a public
release. Graphics checks must be run on real hardware before advertising them.

## Scope and licensing

RetroArch already has upstream Windows ARM64 support. This repository provides
packaging, pinned build inputs, small compatibility fixes and explicit validation;
it does not claim to introduce the ARM64 port.

Original scripts/docs: MIT. RetroArch: GPL-3.0-or-later. FBNeo: custom noncommercial
terms, including restrictions on profit and donations. Assets/fonts have their
own licenses. See [the full notices](THIRD_PARTY_NOTICES.md).
