C:\Python36-32\python -m pip install --upgrade pip setuptools  wheel
C:\Python37-32\python -m pip install --upgrade pip setuptools  wheel
C:\Python38-32\python -m pip install --upgrade pip setuptools  wheel
C:\Python27-32\python -m pip install --upgrade pip setuptools  wheel

call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars32.bat"

set VS90COMNTOOLS=%VS160COMNTOOLS%
set VS140COMNTOOLS=%VS160COMNTOOLS%

pushd ..
C:\Python36-32\python setup.py bdist_wheel -d wheelhouse
C:\Python37-32\python setup.py bdist_wheel -d wheelhouse
C:\Python38-32\python setup.py bdist_wheel -d wheelhouse
C:\Python27-32\python setup.py bdist_wheel -d wheelhouse
popd
