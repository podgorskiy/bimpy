rm -Rf build

sphinx-apidoc -o source/ ../bimpy
sphinx-build -M html source build
