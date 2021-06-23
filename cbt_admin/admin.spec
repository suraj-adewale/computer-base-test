# -*- mode: python -*-

block_cipher = None


a = Analysis(['c:/pythonprojects/pyqt5_/cbt_admin/admin.py'],
             pathex=["C:\\pythonprojects\\pyqt5_\\cbt_admin"], 
             binaries=[],
              datas=[(HOMEPATH + '\\PyQt5\\Qt\\bin\*', 'PyQt5\\Qt\\bin')],
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
          [],
          exclude_binaries=True,
          name='admin',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
    icon="C:/pythonprojects/pyqt5_/cbt/image/logo.ico" ) 
coll = COLLECT(exe,
        Tree("C:/pythonprojects/pyqt5_/cbt_admin"),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='admin')
