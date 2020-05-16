#!/usr/bin/env python
#coding=utf-8

import os
import hashlib
from datetime import datetime


def locate_file(app, filename):
    return os.path.join(app.config["UPLOAD_DIR"], filename)


def get_file_code() -> str:
    seed = datetime.now().strftime("%Y%m%d%H%M%S%f")
    longhash = hashlib.md5(seed.encode("utf-8")).hexdigest()
    return longhash[:6]
