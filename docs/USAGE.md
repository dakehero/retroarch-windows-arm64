# Windows ARM64 usage guide

This is a community build, not an official release from the RetroArch or FBNeo teams.

Extract the RetroArch package and run `retroarch.exe`. To install FBNeo, copy
`cores/fbneo_libretro.dll` and `info/fbneo_libretro.info` from the separate FBNeo
package into the matching directories inside RetroArch. Retain the accompanying
FBNeo license files. Select FinalBurn Neo under Load Core, then load your content.

Windows ARM64 is required. The ARM64 frontend cannot load x64 or x86 cores.
This project does not provide a complete online core server; install the supplied
FBNeo core from the separate release attachment.

Defaults are Ozone with Simplified Chinese, D3D11 video, and WASAPI audio.
Change the menu language under Settings → User → Language. Save files are stored
in `saves`, save states in `states`, screenshots in `screenshots`, and system
files in `system`. Extract into a writable directory.

No ROMs or BIOS files are included. Supply content you have the right to use and
that matches the core's expected ROM set. Initial checks cover the menu, libretro
ABI/initialization, and the error path for an empty synthetic ZIP. They do not
cover actual gameplay, controllers, netplay, save-state compatibility, or performance.
An unknown-romset message for the empty test ZIP is expected and does not establish
game compatibility.

See `THIRD_PARTY_NOTICES.md` for component licenses. Matching complete source and
build scripts are available alongside binaries on the same release page:
https://github.com/dakehero/retroarch-windows-arm64/releases
