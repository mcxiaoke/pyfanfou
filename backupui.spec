# -*- mode: python -*-
a = Analysis(['backupui.py'],
             pathex=['D:\\mcxiaoke\\pyfanfou'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pyfanfou.exe',
          debug=False,
          strip=False,
          upx=False,
          console=False )
