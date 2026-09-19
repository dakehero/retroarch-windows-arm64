Unofficial native Windows ARM64 builds of RetroArch 1.22.2 and FinalBurn Neo.

- Extract `RetroArch-1.22.2-Windows-ARM64.zip` and run `retroarch.exe`.
- Optionally merge the `cores` and `info` directories from `FBNeo-Windows-ARM64.zip` into it.
- Ozone, Simplified Chinese fonts, D3D11 video and WASAPI audio defaults.
- D3D11 screenshot error handling and FBNeo MSVC macro compatibility fixes.
- Separate matching patched source archives, build scripts, and SHA-256 checksums are included.

CI checks ARM64 PE architecture, libretro ABI/init/deinit, and frontend/core
integration for 180 frames with null video, disabled audio, and an empty synthetic ZIP.
The expected FBNeo unknown-romset error is not a gameplay test. D3D11/WASAPI
graphics tests require separate real-hardware validation; see the release-specific
validation note when present. Game compatibility, performance, controllers,
netplay and HDR have not been validated. No ROMs or BIOS files are included.

RetroArch and its changes retain GPL-3.0-or-later. FBNeo retains its custom
noncommercial terms (including the donation restriction). Assets/fonts retain
their original licenses. The MIT license on build scripts does not relicense
these components. See THIRD_PARTY_NOTICES.md in the repository and packages.
