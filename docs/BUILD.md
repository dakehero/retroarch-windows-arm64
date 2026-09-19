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

For an offline build, verify the release checksums and unpack both release source
archives under `.work/sources/` inside the extracted build-scripts directory.
Build.ps1 reuses those trees and applies patches idempotently; no original source
download is needed. If a source tree is absent, it downloads the original pinned
archive (or verifies a cached copy in `.work/downloads/`) and extracts it first.
Existing source trees are trusted local input, so use a clean directory when
checking an upstream version change. Source archives already contain the generated
CMake project; MSBuild/CMake can also be invoked directly as in Build.ps1.

Build scripts normalize inherited Windows environment variable key casing in
child processes to accommodate MSBuild/.NET Framework. They do not persistently
change environment variables. Visual Studio / compiler revisions may change
binary checksums; this project does not claim byte-for-byte reproducible binaries.
