# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['DLC.py'],
             pathex=['/Users/frankma/code/DLC-packaging/macos_v2.2rc3/pyinstaller_packaging'],
             binaries=[],
             datas=[],
             hiddenimports=['sklearn.neighbors._typedefs',
             'sklearn.utils._cython_blas', 
             'sklearn.utils._weight_vector',
             'sklearn.neighbors._quad_tree',
             'sklearn.tree', 
             'sklearn.tree._utils',
             'skimage.filters.rank.core_cy_3d',
             'statsmodels.tsa.statespace._filters',
             'statsmodels.tsa.statespace._filters._conventional',
             'statsmodels.tsa.statespace._filters._univariate',
             'statsmodels.tsa.statespace._filters._univariate_diffuse',
             'statsmodels.tsa.statespace._filters._inversions',
             'statsmodels.tsa.statespace._smoothers',
             'statsmodels.tsa.statespace._smoothers._alternative',
             'statsmodels.tsa.statespace._smoothers._classical',
             'statsmodels.tsa.statespace._smoothers._conventional',
             'statsmodels.tsa.statespace._smoothers._univariate',
             'statsmodels.tsa.statespace._smoothers._univariate_diffuse'],
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
          name='DLC',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='DLC')
app = BUNDLE(coll,
             name='DLC.app',
             icon=None,
             bundle_identifier=None)
