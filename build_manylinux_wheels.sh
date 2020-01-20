# Script to build wheels for manylinux. This script executes bimpy_docker.sh inside docker

docker run -it --rm -e PLAT=manylinux2010_x86_64 -v `pwd`:/io quay.io/pypa/manylinux2010_x86_64 sh /io/bimpy_docker.sh
