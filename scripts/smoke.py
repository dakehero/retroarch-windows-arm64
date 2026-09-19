"""Native ABI and frontend integration checks, using an empty ZIP, never game ROMs."""
from pathlib import Path
import argparse
import ctypes as c
import json
import shutil
import subprocess
import zipfile
from pipeline import ROOT, WORK, arm64


def abi(path):
    core = c.CDLL(str(path))
    class SystemInfo(c.Structure):
        _fields_ = [('library_name', c.c_char_p), ('library_version', c.c_char_p),
                    ('valid_extensions', c.c_char_p), ('need_fullpath', c.c_bool),
                    ('block_extract', c.c_bool)]
    callback = c.CFUNCTYPE(c.c_bool, c.c_uint, c.c_void_p)
    @callback
    def environment(command, data):
        return False
    core.retro_api_version.restype = c.c_uint
    if core.retro_api_version() != 1:
        raise ValueError('Unexpected libretro ABI')
    info = SystemInfo()
    core.retro_get_system_info.argtypes = [c.POINTER(SystemInfo)]
    core.retro_get_system_info.restype = None
    core.retro_get_system_info(c.byref(info))
    if info.library_name != b'FinalBurn Neo':
        raise ValueError('Unexpected core identity')
    core.retro_set_environment.argtypes = [callback]
    core.retro_set_environment.restype = None
    core.retro_set_environment(environment)
    core.retro_init.restype = core.retro_deinit.restype = None
    core.retro_init()
    core.retro_deinit()
    return {'core':info.library_name.decode(), 'version':info.library_version.decode(), 'api':1}


def main(graphics):
    for name in ('retroarch.exe','fbneo_libretro.dll'):
        arm64(WORK/'bin'/name)
    # ctypes must have the same architecture as the ARM64 DLL.
    arm64(Path(__import__('sys').executable))
    results = {'architecture':'ARM64', 'abi':abi(WORK/'bin/fbneo_libretro.dll')}
    directory = WORK / ('smoke-graphics' if graphics else 'smoke-headless')
    directory.mkdir(exist_ok=True)
    for name in ('retroarch.exe','fbneo_libretro.dll'):
        shutil.copy2(WORK/'bin'/name, directory/name)
    cfg = (ROOT/'config/retroarch.cfg').read_text()
    override = 'config_save_on_exit = "false"\npause_nonactive = "false"\nmenu_pause_libretro = "false"\nhistory_list_enable = "false"\n'
    override += f'assets_directory = "{(WORK / "assets").as_posix()}"\n'
    if not graphics:
        override += 'video_driver = "null"\naudio_enable = "false"\nmenu_driver = "rgui"\n'
    (directory/'retroarch.cfg').write_text(cfg,encoding='utf-8')
    (directory/'override.cfg').write_text(override,encoding='utf-8')
    with zipfile.ZipFile(directory/'arm64-smoke-no-rom.zip','w'):
        pass
    hidden = subprocess.STARTUPINFO()
    hidden.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    hidden.wShowWindow = 0
    version = subprocess.run([str(directory/'retroarch.exe'),'--version'],cwd=directory,capture_output=True,timeout=30,check=True,startupinfo=hidden)
    version_text = (version.stdout+version.stderr).decode('utf-8',errors='replace')
    if '1.22.2' not in version_text:
        raise ValueError('Unexpected RetroArch version')
    for name in ('menu','fbneo'):
        logfile = directory/f'{name}.log'
        screenshot = directory/f'{name}.png'
        if screenshot.exists():
            screenshot.unlink()
        args = [str(directory/'retroarch.exe'),'--config',str(directory/'retroarch.cfg'),
                '--appendconfig',str(directory/'override.cfg'),'--verbose',
                '--log-file',str(logfile),'--max-frames','180']
        if name == 'menu':
            args += ['--menu']
        else:
            args += ['-L',str(directory/'fbneo_libretro.dll'),str(directory/'arm64-smoke-no-rom.zip')]
        if graphics:
            args += ['--max-frames-ss','--max-frames-ss-path',str(screenshot)]
        process = subprocess.run(args,cwd=directory,capture_output=True,timeout=45,startupinfo=hidden)
        if process.returncode:
            raise RuntimeError(f'{name}: exit {process.returncode}; inspect {logfile}')
        log = logfile.read_text(encoding='utf-8',errors='replace')
        if not graphics and '[Video] Found display server: "null"' not in log:
            raise ValueError(f'{name}: the null display server was not initialized')
        if name == 'fbneo' and '[FBNeo]' not in log:
            raise ValueError('Frontend did not initialize FBNeo')
        if graphics and (not screenshot.is_file() or screenshot.read_bytes()[:8] != b'\x89PNG\r\n\x1a\n'):
            raise ValueError(f'Missing valid {name} GPU screenshot')
        results[name] = {'frames':180,'exit_code':0,'gpu_screenshot':graphics}
    results['mode'] = 'D3D11/WASAPI' if graphics else 'null video, audio disabled (driver selection asserted)'
    results['content'] = 'empty ZIP: expected FBNeo unknown-romset screen; no gameplay coverage'
    dest = WORK/('validation-graphics.json' if graphics else 'validation-ci.json')
    dest.write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--graphics',action='store_true',help='Require a working local D3D11 GPU and WASAPI audio device')
    main(parser.parse_args().graphics)
