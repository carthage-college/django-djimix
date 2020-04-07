# -*- coding: utf-8 -*-

import sys

from django.core.cache import cache
from djimix.people.utils import get_peeps


def main():
    """Clear the cache and repopulate it for API data."""
    for key in ('student', 'facstaff'):
        cache.delete('provisioning_vw_{0}_api'.format(key))
        try:
            get_peeps(key)
        except Exception as error:
            print(error)


if __name__ == '__main__':

    sys.exit(main())
