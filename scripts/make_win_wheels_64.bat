C:\Python36\python -m pip install --upgrade pip setuptools wheel
C:\Python37\python -m pip install --upgrade pip setuptools wheel
C:\Python38\python -m pip install --upgrade pip setuptools wheel
C:\Python27\python -m pip install --upgrade pip setuptools wheel

call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"

set VS90COMNTOOLS=%VS160COMNTOOLS%
set VS140COMNTOOLS=%VS160COMNTOOLS%

pushd ..
C:\Python36\python setup.py bdist_wheel -d wheelhouse
C:\Python37\python setup.py bdist_wheel -d wheelhouse
C:\Python38\python setup.py bdist_wheel -d wheelhouse
C:\Python27\python setup.py bdist_wheel -d wheelhouse
popd
