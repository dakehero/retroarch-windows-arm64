# Licensing and attribution

This is an unofficial community build of existing upstream projects. It is not
endorsed by Libretro, RetroArch, or the FinalBurn Neo team. The root MIT license
covers only original build scripts and documentation, not third-party software.

| Material | Upstream / license |
| --- | --- |
| RetroArch 1.22.2, its patch, and vendored MSVC projects | [Libretro/RetroArch](https://github.com/libretro/RetroArch/tree/v1.22.2), GPL-3.0-or-later; `licenses/RetroArch-GPL-3.0.txt`. Individual bundled components retain their own notices in the corresponding source archive. |
| FinalBurn Neo and its patch | [libretro/FBNeo](https://github.com/libretro/FBNeo/tree/6bb3167a044e19e7106a5110d5531aa9c6afa96f), custom noncommercial license; full text and historical/third-party terms in `licenses/FBNeo.txt` and the source archive. |
| Ozone icons and other RetroArch assets | [retroarch-assets](https://github.com/libretro/retroarch-assets/tree/73106363e14e34c08a5854b4cfbc29f184e3b783), CC BY 4.0 except separately licensed material such as fonts; `licenses/Assets-CC-BY-4.0.txt`. Copied without modification from the pinned tree. |
| Ozone regular/bold fonts | Upstream merged Inter UI / XMB / M+ fonts, as described in `assets/ozone/README.md`. Inter: Copyright 2018 The Inter UI project authors, SIL OFL 1.1, full license in `licenses/Inter-OFL-1.1.txt`. M+ notice in `assets/fonts/mplus-1pLICENSE_E.txt` and Japanese counterpart. Exact embedded notices in `licenses/Font-embedded-notices.txt`. |
| Droid Sans Fallback Chinese font | Digitized data copyright Google Corporation 2006, Apache License 2.0; `licenses/Apache-2.0.txt`, `licenses/Font-embedded-notices.txt`, and `assets/pkg/chinese-fallback-font.txt`. |
| DejaVu Sans fallback font | Bitstream / Arev notices and public-domain DejaVu changes; `assets/fonts/DejaVuSans.LICENSE.txt`, `licenses/Font-embedded-notices.txt`. |
| FBNeo core metadata | [libretro-core-info](https://github.com/libretro/libretro-core-info/tree/5a74858ab2f7a50cebb5a6330895bc38899531c0), MIT, Copyright 2019 The RetroArch team; `licenses/Core-info.txt`. |

FBNeo's license permits use, modification and redistribution subject to its
terms, including no monetary profit, publication of source changes, retention of
the full license, no unauthorized ROM distribution, and no soliciting donations
to support work on projects using its source. It is not OSI open source and is
not relicensed under this repository's MIT license or RetroArch's GPL.

Release binaries are provided as separate components, with matching patched
source archives and `build-scripts.zip` on the same release. Distributors must
preserve each component's applicable terms. No game ROMs or BIOS files are included.

Changes from upstream are recorded in `patches/README.md`. Patches were prepared
on 2026-09-19. The generated FBNeo CMake build and packaging configuration are
additional build material; upstream authorship and notices remain intact.
