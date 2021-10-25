# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['__init__.py'],
             pathex=['./'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['matplotlib', 'pyside2', 'tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='GCrypter',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , uac_admin=True,
          icon='img/gcrypter-256x256.ico')
