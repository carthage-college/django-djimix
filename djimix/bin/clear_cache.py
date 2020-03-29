# -*- coding: utf-8 -*-

import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djimix.settings.shell')

import django
django.setup()

from django.conf import settings
from django.urls import reverse
from django.core.cache import cache

from directory.api.views import get_peeps



def main():
    """Clear the cache and repopulate it for API data."""
    headers = {'Cache-Control': 'no-cache'}
    for key in ['student','facstaff']:
        cache.delete('provisioning_vw_{}_api'.format(key))
        peeps = get_peeps(key)

if __name__ == '__main__':
    sys.exit(main())
