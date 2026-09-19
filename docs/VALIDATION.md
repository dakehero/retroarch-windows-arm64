# Validation boundaries

The original local build was tested on Windows 11 ARM64 with a Qualcomm Adreno
X2-90 GPU. PE headers identify both binaries as AA64; imports used Windows system
DLLs with static MSVC CRT. The D3D11 menu, WASAPI audio driver initialization,
GPU screenshot, libretro ABI/init/deinit, and frontend/core integration with an
empty ZIP all passed. The latter renders FBNeo's expected unknown-romset message.

The public scripts repeat architecture, version, ABI and frontend/core checks.
`scripts/smoke.py` uses null video/audio for CI. `--graphics` requires the D3D11
menu and synthetic FBNeo error screen to run for 180 frames and produce PNG
screenshots, with exit code zero. JSON results are saved below `.work/`.

The CI result is attached to the specific workflow commit/run. A local test does
not certify a separately compiled CI binary. Local graphics checks and CI null
driver checks must be reported separately in release notes.

Not covered: actual ROM gameplay, gamepads, netplay, save-state compatibility,
performance, HDR, other GPUs, or other computers. No ROM is downloaded for tests.
