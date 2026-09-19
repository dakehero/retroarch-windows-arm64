"""Pinned downloads, source preparation and release packaging; Python stdlib only."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess
import tarfile
import time
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.work'
LOCK = json.loads((ROOT / 'sources.lock.json').read_text())


def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def download(url, destination, digest, git_blob=False):
    def valid():
        if not destination.is_file():
            return False
        if git_blob:
            data = destination.read_bytes()
            actual = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
        else:
            actual = sha256(destination)
        return actual == digest
    if valid():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'retroarch-windows-arm64-build'})
            with urllib.request.urlopen(req, timeout=120) as response, destination.open('wb') as out:
                shutil.copyfileobj(response, out)
            if not valid():
                raise ValueError(f'Checksum mismatch: {destination.name}')
            return
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))


def source(component):
    return WORK / 'sources' / LOCK[component]['directory']


def patch(directory, name):
    args = ['git', '-C', str(directory), 'apply']
    filename = str(ROOT / 'patches' / name)
    result = subprocess.run(args + ['--check', filename], capture_output=True)
    if result.returncode == 0:
        subprocess.run(args + [filename], check=True)
    else:
        subprocess.run(args + ['--reverse', '--check', filename], check=True)


def cmake_fbneo():
    manifest = json.loads((ROOT / 'manifests/fbneo.json').read_text())
    fb = source('fbneo')
    for name, checksum in manifest['makefiles'].items():
        if sha256(fb / 'src/burner/libretro' / name) != checksum:
            raise ValueError(f'FBNeo manifest is stale: {name}')
    for name in manifest['sources']:
        if not (fb / name).is_file():
            raise FileNotFoundError(name)
    def items(values):
        return '\n'.join('  "' + value + '"' for value in values)
    defines = manifest['defines'] + [
        '__LIBRETRO__', 'LSB_FIRST', 'USE_SPEEDHACKS',
        'WINAPI_FAMILY=WINAPI_FAMILY_DESKTOP_APP',
        '_CRT_SECURE_NO_WARNINGS', '_CRT_NONSTDC_NO_WARNINGS']
    text = f'''cmake_minimum_required(VERSION 3.21)
project(FBNeoLibretroARM64 LANGUAGES C CXX)
if(NOT MSVC OR NOT CMAKE_GENERATOR_PLATFORM STREQUAL "ARM64")
  message(FATAL_ERROR "Use the MSVC generator with -A ARM64")
endif()
set(CMAKE_MSVC_RUNTIME_LIBRARY MultiThreaded)
add_library(fbneo_libretro SHARED
{items(manifest['sources'])}
)
target_include_directories(fbneo_libretro PRIVATE
{items(manifest['includes'])}
)
target_compile_definitions(fbneo_libretro PRIVATE
{items(defines)}
)
target_compile_options(fbneo_libretro PRIVATE /O2 /utf-8 /bigobj /MP /wd4996)
set_source_files_properties(src/burn/drv/snes/msu1_backend.cpp PROPERTIES INCLUDE_DIRECTORIES "${{CMAKE_CURRENT_SOURCE_DIR}}/src/dep/vc/include")
target_link_libraries(fbneo_libretro PRIVATE kernel32 user32 gdi32 winspool comdlg32 advapi32 shell32 ole32 uuid ws2_32 winmm)
set_target_properties(fbneo_libretro PROPERTIES PREFIX "" OUTPUT_NAME "fbneo_libretro")
'''
    (fb / 'CMakeLists.txt').write_text(text, encoding='utf-8', newline='\n')
    print(f'Prepared {len(manifest["sources"])} FBNeo sources')


def prepare():
    for component in ('retroarch', 'fbneo'):
        entry = LOCK[component]
        directory = source(component)
        if not directory.exists():
            archive = WORK / 'downloads' / entry['archive']
            download(entry['url'], archive, entry['sha256'])
            directory.parent.mkdir(parents=True, exist_ok=True)
            with tarfile.open(archive) as tar:
                tar.extractall(directory.parent, filter='data')
        if not directory.is_dir():
            raise FileNotFoundError(directory)
    patch(source('retroarch'), 'retroarch-local.patch')
    patch(source('fbneo'), 'fbneo-msvc.patch')
    for name, digest in LOCK['msvc_files'].items():
        origin = ROOT / 'vendor/msvc' / name
        if sha256(origin) != digest:
            raise ValueError(f'Vendored project changed: {name}')
        dest = source('retroarch') / 'pkg/msvc' / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, dest)
    cmake_fbneo()


def assets():
    entries = json.loads((ROOT / 'manifests/assets.json').read_text())
    def fetch(entry):
        path = entry['path']
        url = 'https://raw.githubusercontent.com/libretro/retroarch-assets/' + LOCK['assets']['ref'] + '/' + urllib.parse.quote(path)
        download(url, WORK / 'assets' / path, entry['sha'], git_blob=True)
    with ThreadPoolExecutor(max_workers=12) as pool:
        list(pool.map(fetch, entries))
    entry = LOCK['core_info']
    download(entry['url'], WORK / 'info/fbneo_libretro.info', entry['sha256'])
    print(f'Verified {len(entries)} assets and pinned FBNeo core info')


def arm64(path):
    with path.open('rb') as stream:
        header = stream.read(64)
        if header[:2] != b'MZ':
            raise ValueError(f'Not a PE image: {path.name}')
        stream.seek(struct.unpack_from('<I', header, 0x3c)[0])
        signature = stream.read(6)
    if signature[:4] != b'PE\0\0' or struct.unpack_from('<H', signature, 4)[0] != 0xAA64:
        raise ValueError(f'Not native ARM64: {path.name}')


def source_archive(component, destination):
    directory = source(component)
    def clean(info):
        # RetroArch MSBuild writes intermediates below pkg/msvc; keep source only.
        parts = Path(info.name).parts
        if any(p in {'ARM64', 'x64', 'Debug', 'Release', '__pycache__', '.git'} for p in parts):
            return None
        if info.name.endswith(('.obj', '.pdb', '.tlog', '.binlog', '.exe', '.dll')):
            return None
        info.uid = info.gid = 0
        info.uname = info.gname = ''
        return info
    with tarfile.open(destination, 'w:xz', preset=1) as tar:
        tar.add(directory, arcname=directory.name, filter=clean)


def archive_dir(directory, destination):
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED, compresslevel=7) as out:
        for path in sorted(directory.rglob('*')):
            if path.is_file():
                out.write(path, path.relative_to(directory.parent))
    with zipfile.ZipFile(destination) as check:
        if check.testzip() is not None:
            raise ValueError('Corrupt package')


def package():
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    stage = WORK / 'stage'
    if stage.exists():
        # This is generated packaging output; never delete arbitrary caller paths.
        if stage.resolve() != (ROOT.resolve() / '.work/stage'):
            raise ValueError('Unsafe staging path')
        shutil.rmtree(stage)
    ra = stage / 'RetroArch-1.22.2-Windows-ARM64'
    fb = stage / 'FBNeo-Windows-ARM64'
    ra.mkdir(parents=True)
    (fb / 'cores').mkdir(parents=True)
    (fb / 'info').mkdir()
    for src, dst in [(WORK/'bin/retroarch.exe', ra/'retroarch.exe'), (WORK/'bin/fbneo_libretro.dll', fb/'cores/fbneo_libretro.dll')]:
        arm64(src)
        shutil.copy2(src, dst)
    shutil.copytree(WORK / 'assets', ra / 'assets')
    shutil.copy2(WORK / 'info/fbneo_libretro.info', fb / 'info/fbneo_libretro.info')
    shutil.copy2(ROOT / 'config/retroarch.cfg', ra / 'retroarch.cfg')
    for directory in ['cores','info','system','saves','states','screenshots','playlists','config','cache','downloads','thumbnails']:
        (ra/directory).mkdir(exist_ok=True)
    for directory in (ra, fb):
        shutil.copytree(ROOT / 'licenses', directory / 'licenses')
        shutil.copy2(ROOT / 'THIRD_PARTY_NOTICES.md', directory / 'THIRD_PARTY_NOTICES.md')
        shutil.copy2(ROOT / 'docs/USAGE.md', directory / 'README.md')
    build_info = json.loads((WORK / 'build-info.json').read_text())
    build_info['sources'] = LOCK
    build_info['binaries'] = {name: {'sha256':sha256(WORK/'bin'/name),'architecture':'ARM64'} for name in ['retroarch.exe','fbneo_libretro.dll']}
    for directory in (ra, fb):
        (directory/'build-info.json').write_text(json.dumps(build_info,indent=2)+'\n',encoding='utf-8')
    outputs=[]
    for component, directory in [('retroarch',ra),('fbneo',fb)]:
        archive = dist / (directory.name + '.zip')
        archive_dir(directory, archive)
        outputs.append(archive)
        archive = dist / (directory.name + '-source.tar.xz')
        source_archive(component, archive)
        outputs.append(archive)
    build_archive = dist / 'build-scripts.zip'
    with zipfile.ZipFile(build_archive,'w',zipfile.ZIP_DEFLATED) as out:
        for parent, dirs, files in os.walk(ROOT):
            dirs[:] = sorted(d for d in dirs if d not in {'.git','.work','dist','__pycache__'})
            for name in sorted(files):
                path = Path(parent) / name
                out.write(path, Path('retroarch-windows-arm64') / path.relative_to(ROOT))
    outputs.append(build_archive)
    (dist/'SHA256SUMS.txt').write_text(''.join(f'{sha256(p)}  {p.name}\n' for p in outputs),encoding='utf-8')
    print('\n'.join(str(p) for p in outputs))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['prepare','assets','package'])
    args = parser.parse_args()
    globals()[args.command]()
