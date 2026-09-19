# Local changes (2026-09-19)

`retroarch-local.patch` applies to RetroArch v1.22.2:

- Clear incompatible miscellaneous flags when creating a D3D11 screenshot staging
  texture; check creation, resource availability and Map before dereferencing;
  initialize pointers/results and release resources safely on error. An unpatched
  build crashed in the screenshot path on a Qualcomm Adreno Windows ARM64 device.
- Initialize the CPU-capability log buffer when the feature mask is empty. The
  latest upstream master already initializes this in the capability function;
  this part is a stable-version backport workaround, not a new upstream fix.

`fbneo-msvc.patch` applies to FBNeo commit
`6bb3167a044e19e7106a5110d5531aa9c6afa96f`:

- Only alias `strcasecmp` if it is not already defined, avoiding a macro cycle in
  the Windows libretro/MSVC build.

The FBNeo source manifest uses upstream's default driver selection with 7z/CHD
support. No additional x86-only assembly or JIT is enabled. The generated CMake
project uses static CRT and adds FBNeo's own MSVC dirent include for MSU-1 only.

RetroArch patches retain GPL-3.0-or-later terms. FBNeo patches retain the original
FBNeo license. Before an upstream PR, rebase on current master and verify the
relevant behavior there; do not submit the already-fixed CPU buffer workaround.
