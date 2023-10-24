from PyInstaller.utils.hooks import collect_data_files
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['IonConverter.py'],
             pathex=['C:\\Users\\admin\\Desktop\\PdfConverter\\IonConverter'],
             binaries=[],
             datas=collect_data_files("tabula"),
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
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
          name='IonConverter',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
