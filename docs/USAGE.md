# Windows ARM64 使用说明 / usage

这是社区构建，并非 RetroArch 或 FBNeo 团队的官方发行版。

解压 RetroArch 包后运行 `retroarch.exe`。安装 FBNeo 时，把 FBNeo 包内的
`cores/fbneo_libretro.dll` 和 `info/fbneo_libretro.info` 分别复制到 RetroArch
目录中的同名文件夹。然后在「加载核心」中选择 FinalBurn Neo，再加载游戏。
FBNeo 包中的许可证请一并保留。

仅支持 Windows ARM64。x64/x86 核心不能由这个 ARM64 主程序加载。
未提供完整在线核心服务器；此版本的 FBNeo 核心通过独立附件安装。

默认 Ozone 简体中文菜单、D3D11 视频和 WASAPI 音频。存档在 `saves`，即时状态
在 `states`，截图在 `screenshots`，系统文件在 `system`。不要解压到只读目录。

不附带 ROM/BIOS。请自行提供有权使用且与核心相匹配的内容。首次发布只验证了
菜单、核心 ABI/初始化和空测试 ZIP 的错误提示路径，没有验证真实游戏、手柄、
联机或性能。空测试 ZIP 出现“未知集组”是预期行为，不代表任何游戏已通过测试。

English: extract RetroArch, then merge the optional FBNeo `cores` and `info`
directories into it. Launch `retroarch.exe`, load the core and your own content.
Native ARM64 cores are required. See `THIRD_PARTY_NOTICES.md` for component licenses.
Matching source and build scripts are available alongside binaries at:
https://github.com/dakehero/retroarch-windows-arm64/releases
