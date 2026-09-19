# Build inputs and maintenance

`sources.lock.json` pins source archives, original MSVC project hashes, asset
revision and FBNeo metadata. The RetroArch official source-only archive excludes
MSVC projects; `vendor/msvc/` supplies the unmodified files from the same v1.22.2
tag. The complete source release includes these projects and applied patches.

`manifests/assets.json` selects the Ozone assets and required fonts/licenses from
the pinned upstream Git tree. Each download is checked against its Git blob hash.

`manifests/fbneo.json` records the outputs of upstream `Makefile.common` and
`Makefile.all`. `scripts/refresh-fbneo-manifest.py` regenerates it using installed
GNU Make 4.x. The source makefile hashes are checked before every CMake generation.
When updating FBNeo, update the lock, regenerate the manifest and inspect the
driver/define changes. Never silently reuse a manifest from a different revision.

For offline source inspection, unpack the two release source archives under
`.work/sources/`. For an offline build, also place the original source archives
named in `sources.lock.json` under `.work/downloads/`; they are included unchanged
upstream downloads. Build.ps1 checks the cached downloads and applies patches
idempotently. Source archives already contain the generated CMake project, so
advanced users can also invoke MSBuild/CMake directly using Build.ps1 as reference.

Build scripts normalize inherited Windows environment variable key casing in
child processes to accommodate MSBuild/.NET Framework. They do not persistently
change environment variables. Visual Studio / compiler revisions may change
binary checksums; this project does not claim byte-for-byte reproducible binaries.
