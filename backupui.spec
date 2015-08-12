# -*- mode: python -*-
a = Analysis(['backupui.py'],
             pathex=['D:\\mcxiaoke\\pyfanfou'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='pyfanfou.exe',
          debug=False,
          strip=None,
          upx=False,
          console=False , icon='icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=False,
               name=u'pyfanfou')
