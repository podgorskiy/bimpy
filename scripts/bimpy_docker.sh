#!/usr/bin/env bash
# Script to build wheels for manylinux. This script runs inside docker.
# See build_maylinux_wheels.sh

git clone https://github.com/podgorskiy/bimpy.git
cd bimpy
git submodule update --init
cd glfw
git pull origin master
cd ..

yum install -y libX11-devel libXcursor-devel libXrandr-devel libXinerama-devel mesa-libGL-devel libXi-devel

for PYBIN in /opt/python/*/bin; do
    #"${PYBIN}/pip" install -r /io/dev-requirements.txt
    #"${PYBIN}/pip" wheel /io/ -w wheelhouse/
    "${PYBIN}/python" setup.py bdist_wheel -d /io/wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in /io/wheelhouse/*.whl; do
    auditwheel show "$whl"
    auditwheel repair "$whl" --plat $PLAT -w /io/wheelhouse/
done