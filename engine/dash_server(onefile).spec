# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['dash_server.py'],
             pathex=['C:\\Users\\austi\\Projects\\rpids\\engine'],
             binaries=[],
             datas=[
                 ('C:\\Users\\austi\\anaconda3\\envs\\py38\\Lib\\site-packages\\dash_core_components\\', 'dash_core_components'),
                 ('C:\\Users\\austi\\anaconda3\\envs\\py38\\Lib\\site-packages\\dash_html_components\\', 'dash_html_components'),
                 ('C:\\Users\\austi\\anaconda3\\envs\\py38\\Lib\\site-packages\\dash_renderer\\','dash_renderer'),
                 ('C:\\Users\\austi\\anaconda3\\envs\\py38\\Lib\\site-packages\\plotly', 'plotly'),
                 ('C:\\Users\\austi\\anaconda3\\envs\\py38\\Lib\\site-packages\\sklearn\\.libs\\vcomp140.dll', '.\\sklearn\\.libs')
                 ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=True,
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
          name='dash_server',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
