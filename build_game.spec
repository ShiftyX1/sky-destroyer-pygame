import os
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis

block_cipher = None

assets = [
    ('assets/sounds/*.wav', 'assets/sounds'),  # Только звуковые файлы, так как они есть
]

# На будущее, если еще добавятся ассеты
# if os.path.exists('assets/fonts') and os.listdir('assets/fonts'):
#     assets.append(('assets/fonts/*', 'assets/fonts'))
# if os.path.exists('assets/images') and os.listdir('assets/images'):
#     assets.append(('assets/images/*', 'assets/images'))
# if os.path.exists('assets/levels') and os.listdir('assets/levels'):
#     assets.append(('assets/levels/*', 'assets/levels'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=assets,
    hiddenimports=[
        'const.colors',
        'const.game_consts',
        'const.system_consts',
        'game_objects.bullet',
        'game_objects.camera',
        'game_objects.cloud',
        'game_objects.enemy',
        'game_objects.player',
        'utils.glow',
        'utils.sound'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SkyDestroyer3D',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)