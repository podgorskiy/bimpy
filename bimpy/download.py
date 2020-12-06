# Copyright 2017-2020 Stanislav Pidhorskyi. All rights reserved.
# License: https://raw.githubusercontent.com/podgorskiy/bimpy/master/LICENSE.txt

import os
import cgi
import sys

try:
    from urllib import request
    from http import cookies, cookiejar
except ImportError:
    # Fall back to Python 2
    import urllib2 as request
    import Cookie as cookies
    import cookielib as cookiejar


ENV_BIMPY_HOME = 'BIMPY_HOME'
ENV_XDG_CACHE_HOME = 'XDG_CACHE_HOME'
DEFAULT_CACHE_DIR = '~/.cache'


def _get_bimpy_home():
    return os.path.expanduser(os.getenv(ENV_BIMPY_HOME, os.path.join(os.getenv(ENV_XDG_CACHE_HOME, DEFAULT_CACHE_DIR), 'bimpy')))


def _get_fonts_dir():
    return os.path.join(_get_bimpy_home(), 'fonts')


def get_font_cached_or_download(url, file_name=None):
    font_dir = _get_fonts_dir()
    if not os.path.exists(font_dir):
        os.makedirs(font_dir)

    if file_name:
        file_path = os.path.join(font_dir, file_name)
        if os.path.exists(file_path):
            return file_path

    return from_url(url, directory=font_dir, file_name=file_name)


def from_url(url, directory=".", file_name=None):
    """ Downloads file from specified URL.
    Optionally it can be unpacked after downloading completes.
    Args:
        url (str): file URL.
        directory (str): Directory where to save the file
        file_name (str, optional): If not None, this will overwrite the file name, otherwise it will use the filename
            returned from http request. Defaults to None.
    Example:
        ::
            dlutils.download.from_url("http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz", directory)
    """
    request_obj = request.urlopen(url)
    return _download(request_obj, url, directory, file_name)


def _download(request_obj, url, directory, file_name):
    meta = request_obj.info()

    if file_name is None:
        cd = meta.get("content-disposition")
        if cd is not None:
            value, params = cgi.parse_header(cd)
            cd_file = params['filename']
            if cd_file is not None:
                file_name = cd_file

    if file_name is None:
        file_name = url.split('/')[-1]

    file_path = os.path.join(directory, file_name)

    file_size = 0
    length_header = meta.get("Content-Length")
    if length_header is not None:
        file_size = int(length_header)
        print("Downloading: %s Bytes: %d" % (file_name, file_size))
    else:
        print("Downloading: %s" % file_name)

    if os.path.exists(file_path) and (os.path.getsize(file_path) == file_size or file_size == 0):
        return file_path

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, 'wb') as file:
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = request_obj.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            file.write(buffer)
            if file_size > 0:
                status = "\r%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            else:
                status = "\r%10d" % file_size_dl
            sys.stdout.write(status)
            sys.stdout.flush()

        print()

    return file_path
