import logging
import sys
from requests import HTTPError

from .readwritelock import ReadWriteLock
from .interfaces import CachePolicy

log = logging.getLogger(sys.modules[__name__].__name__)


class ManualPollingCachePolicy(CachePolicy):

    def __init__(self, config_fetcher, config_cache):
        self._config_fetcher = config_fetcher
        self._config_cache = config_cache
        self._lock = ReadWriteLock()

    def get(self):
        try:
            self._lock.acquire_read()

            config = self._config_cache.get()
            return config
        finally:
            self._lock.release_read()

    def force_refresh(self):
        try:
            configuration = self._config_fetcher.get_configuration_json()

            try:
                self._lock.acquire_write()

                self._config_cache.set(configuration)
            finally:
                self._lock.release_write()

        except HTTPError as e:
            log.error('Received unexpected response from ConfigFetcher ' + str(e.response))
        except:
            log.exception(sys.exc_info()[0])

    def stop(self):
        pass