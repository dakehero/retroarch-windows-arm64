# RetroArch Windows ARM64 社区构建

原生 ARM64 版 RetroArch，以及单独打包的 FinalBurn Neo 街机核心。
这是非官方构建，基于 RetroArch 1.22.2 和固定版本的 FBNeo 源码。

[下载](https://github.com/dakehero/retroarch-windows-arm64/releases) ·
[构建状态](https://github.com/dakehero/retroarch-windows-arm64/actions/workflows/build.yml) ·
[许可证](THIRD_PARTY_NOTICES.md) · [验证范围](docs/VALIDATION.md)

## 使用

1. 下载并解压 `RetroArch-1.22.2-Windows-ARM64.zip`。
2. 如需 FBNeo，再下载 `FBNeo-Windows-ARM64.zip`，把其中的 `cores`、`info` 合并到 RetroArch 目录。
3. 运行 `retroarch.exe`。默认使用 Ozone 简体中文菜单、D3D11 和 WASAPI。
4. 使用自己有权使用的游戏内容。包内没有 ROM 或 BIOS。

Windows ARM64 主程序必须使用 ARM64 核心，不能加载 x64/x86 核心。
本项目不提供完整核心下载服务器；FBNeo 按上述方式手动安装。
参见 [使用说明](docs/USAGE.md)。

## 本机编译

需要 Windows ARM64，以及已安装的 PowerShell 7、原生 ARM64 Python 3.12+、Git、
CMake 4.0+（使用 VS 2026 时需要 4.2+）、Visual Studio 2022/2026 C++ ARM64 工具链
和 Windows SDK 10.0.26100.0。脚本不会安装工具，也不会修改系统 PATH。
VS 2026 使用 v145 工具集，VS 2022 使用 v143；CI 使用 VS 2026 ARM64 镜像。

```powershell
pwsh -NoProfile -File scripts/Build.ps1
python scripts/pipeline.py assets
python scripts/smoke.py
python scripts/smoke.py --graphics  # 需要本机 GPU 和音频设备
python scripts/pipeline.py package
```

下载文件和编译中间文件保存在 `.work/`，发布附件保存在 `dist/`。
上游输入版本固定在 `sources.lock.json`，通过 SHA-256 或 Git 对象哈希校验。
`manifests/fbneo.json` 由对应版本的上游 GNU Make 清单生成，保留源码和头文件
搜索顺序；日常编译无需安装 GNU Make。更新方法见[构建清单维护说明](docs/BUILD.md)。

每个发行版都提供独立的程序与核心 ZIP、打好补丁的完整源码包、构建脚本和
SHA-256 校验值。把源码包解压到 `.work/sources/` 后，即可查看或重新编译对应源码。
编译器修订和构建时间不同，生成的二进制哈希也可能不同。

## 自动构建与发布

推送代码和提交 PR 后，CI 会在 Windows ARM64 环境编译两个组件，并检查核心 ABI
和主程序加载核心的基本运行路径。这些检查使用空视频、空音频驱动，不验证 GPU
驱动、音频硬件、手柄或真实游戏兼容性。

推送 `v*` 标签后，流水线完成同样的构建和检查，再生成包含程序、核心、对应源码、
脚本和校验值的**预发布草稿**，由维护者检查后公开。CI 产物上传成功不代表已经
公开发行；图形和音频硬件相关的验证需要在真实设备上单独完成。

## 项目范围与许可证

RetroArch 上游已经支持 Windows ARM64。本仓库在此基础上提供完整打包、固定
版本的构建流程、小范围兼容性修复，以及明确的验证记录。

本仓库原创脚本和文档采用 MIT 许可；RetroArch 采用 GPL-3.0-or-later；FBNeo
采用自定义非商业许可，包含盈利和募捐限制；资源和字体保留各自许可证。
脚本的 MIT 许可不适用于这些第三方组件，详情见[许可说明](THIRD_PARTY_NOTICES.md)。
