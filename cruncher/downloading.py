# encoding: utf-8
#
# Copyright (C) 2011 Chris Jerdonek.  All rights reserved.
#

from datetime import datetime
import logging
import urllib
import os

from . import common
from .common import reraise
from .common import Error


_log = logging.getLogger(__name__)


def download(url, target_path):
    """
    Download the file at the given URL to the given target path.

    """
    _log.info("Downloading %s to %s..." % (url, target_path))
    try:
        urllib.urlretrieve(url, target_path)
    except Exception, ex:
        err = Error(ex)
        err.add("Error downloading url: %s" % url)
        reraise(err)

    info = os.stat(target_path)
    _log.info("Downloaded bytes: %s" % info.st_size)


def create_download_metadata(url, datetime_utc):
    """
    Return a DownloadMetadata instance.

    """
    # Stripping microseconds simplifies subsequent formatting code.
    datetime_utc = datetime_utc.replace(microsecond=0)

    datetime_local, local_tzname = common.utc_datetime_to_local_datetime_tzname(datetime_utc)

    data = DownloadMetadata()
    data.url = url
    data.datetime_utc = datetime_utc
    data.datetime_local = datetime_local
    data.local_tzname = local_tzname

    return data


class DownloadMetadata(object):

    def __init__(self):
        self.url = ""
        self.iso_datetime_utc = ""
        self.iso_datetime_local = ""
        self.local_tzname = ""

    def _iso_to_datetime(self, iso_string):
        return datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S")

    @property
    def datetime_utc(self):
        return self._iso_to_datetime(self.iso_datetime_utc)

    @datetime_utc.setter
    def datetime_utc(self, value):
        self.iso_datetime_utc = value.isoformat()

    @property
    def datetime_local(self):
        return self._iso_to_datetime(self.iso_datetime_local)

    @datetime_local.setter
    def datetime_local(self, value):
        self.iso_datetime_local = value.isoformat()




