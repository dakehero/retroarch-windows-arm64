"""Maintainer-only: regenerate the committed manifest using installed GNU Make."""
import json
import subprocess
from pipeline import ROOT, source, sha256

fb = source('fbneo')
libretro = fb / 'src/burner/libretro'
makefile = libretro / 'Makefile.arm64-manifest'
makefile.write_text('''MAIN_FBNEO_DIR := ../..
platform := windows_msvc2017_desktop_arm64
EXTERNAL_ZLIB := 0
INCLUDE_7Z_SUPPORT := 1
INCLUDE_CHD_SUPPORT := 1
CHD_LIBRETRO := 0
HAVE_UWP := 0
SUPPORT_LARGE_FILES := 1
USE_CYCLONE := 0
USE_X64_DRC := 0
HAVE_NEON := 0
AUTOGEN_DATS := 0
include Makefile.common
include Makefile.all
.PHONY: manifest
manifest:
\t$(file >arm64-sources-c.txt,$(sort $(SOURCES_C)))
\t$(file >arm64-sources-cxx.txt,$(sort $(SOURCES_CXX)))
\t$(file >arm64-includes.txt,$(INCLUDE_DIRS))
\t$(file >arm64-defines.txt,$(FBNEO_DEFINES))
''',encoding='utf-8')
subprocess.run(['make','-f',makefile.name,'GIT_VERSION=unknown','manifest'],cwd=libretro,check=True)
def paths(name):
    return [(libretro/p).resolve().relative_to(fb).as_posix() for p in (libretro/name).read_text().split()]
manifest = {
    'makefiles': {name:sha256(libretro/name) for name in ['Makefile.common','Makefile.all']},
    'sources': paths('arm64-sources-c.txt') + paths('arm64-sources-cxx.txt'),
    'includes': paths('arm64-includes.txt'),
    'defines': [d.removeprefix('-D') for d in (libretro/'arm64-defines.txt').read_text().split()],
}
(ROOT/'manifests/fbneo.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(f'Updated {len(manifest["sources"])} sources; review the manifest diff.')
