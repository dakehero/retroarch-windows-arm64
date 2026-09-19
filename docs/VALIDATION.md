# Validation boundaries

The original local build was tested on Windows 11 ARM64 with a Qualcomm Adreno
X2-90 GPU. PE headers identify both binaries as AA64; imports used Windows system
DLLs with static MSVC CRT. The D3D11 menu, WASAPI audio driver initialization,
GPU screenshot, libretro ABI/init/deinit, and frontend/core integration with an
empty ZIP all passed. The latter renders FBNeo's expected unknown-romset message.

The public scripts repeat architecture, version, ABI and frontend/core checks.
`scripts/smoke.py` uses null video with audio disabled for CI. `--graphics` requires the D3D11
menu and synthetic FBNeo error screen to run for 180 frames and produce PNG
screenshots, with exit code zero. JSON results are saved below `.work/`.

The CI result is attached to the specific workflow commit/run. A local test does
not certify a separately compiled CI binary. Local graphics checks and CI null
driver checks must be reported separately in release notes.

The original v1.22.2-arm64.1 CI run appended duplicate configuration keys, which
did not override the default drivers. Its successful integration runs therefore
did not establish null-driver coverage. Commit dc0aa29 fixes this with a separate
`--appendconfig` file and asserts the selected null display server in the log.
The released binaries were subsequently retested locally with the corrected
script in both null-video and D3D11/WASAPI modes. Release `VALIDATION.json` records
that distinction and the unchanged binary hashes.

Not covered: actual ROM gameplay, gamepads, netplay, save-state compatibility,
performance, HDR, other GPUs, or other computers. No ROM is downloaded for tests.
