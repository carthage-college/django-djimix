from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.utils.decorators import available_attrs
from django.utils.encoding import force_str
from django.shortcuts import resolve_url
from django.contrib.auth import login

from djauth.LDAPManager import LDAPManager
from djimix.core.encryption import decrypt
from djimix.core.utils import get_userid
from djtools.utils.users import in_group
from djtools.fields import NOW

from functools import wraps

import logging
logger = logging.getLogger('debug_logfile')
#logger.debug('here in neutral zone')


def portal_auth_required(session_var, group=None, redirect_url=None, encryption=False):
    """
    Accepts a @@UserID (FWK_User.ID) value via GET (uid) passed
    from jenzabar portal environment, or fall back to django auth
    so you can sign in automatically from the portal after
    authentication there or sign in via django auth.
    """

    def _portal_auth_required(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def wrapper(request, *args, **kwargs):
            #logger.debug('here in the rappa')
            resolved_redirect_url = force_str(
                resolve_url(redirect_url or reverse_lazy("auth_login"))
            )
            if not request.session.get(session_var):
                #logger.debug('if 1')
                if not request.user.is_authenticated:
                    #logger.debug('if 2')
                    # we want to redirect back to current view URL
                    refer = request.get_full_path()
                    #logger.debug('refer = {}'.format(refer))
                    redirect = '{}?next={}'.format(
                        reverse_lazy("auth_login"), refer
                    )
                    #logger.debug('redirect = {}'.format(redirect))
                    #logger.debug('uid = {}'.format(request.GET.get('uid')))
                    # UserID value from the portal
                    if request.GET.get('uid'):
                        guid = request.GET.get('uid')
                        #logger.debug(guid)
                        if encryption:
                            guid = decrypt(guid)
                        uid = get_userid(guid)
                        if uid:
                            #logger.debug(uid)
                            uid = int(uid)
                            try:
                                user = User.objects.get(pk=uid)
                            except:
                                try:
                                    # create a new django user
                                    l = LDAPManager()
                                    luser = l.search(uid)
                                    data = luser[0][1]
                                    #logger.debug('data\n')
                                    #logger.debug(data)
                                    password = User.objects.make_random_password(
                                        length=32
                                    )
                                    user = User.objects.create(
                                        pk=uid, username=data['cn'][0],
                                        email=data['mail'][0], last_login=NOW
                                    )
                                    user.set_password(password)
                                    user.first_name = data['givenName'][0]
                                    user.last_name = data['sn'][0]
                                    user.save()
                                    # add to groups
                                    try:
                                        for key, val in settings.LDAP_GROUPS.items():
                                            grp = data.get(key)
                                            if grp and grp[0] == 'A':
                                                g = Group.objects.get(name__iexact=key)
                                                g.user_set.add(user)
                                    except:
                                        pass
                                except:
                                    return HttpResponseRedirect(redirect)
                        else:
                            # we could not find a user from portal's UID
                            return HttpResponseRedirect(redirect)
                    else:
                        return HttpResponseRedirect(redirect)
                else:
                    user = request.user
                if group:
                    if not in_group(user, group) and not user.is_superuser:
                        return HttpResponseRedirect(resolved_redirect_url)
                # sign in the user manually
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                request.session[session_var] = True

            return view_func(request, *args, **kwargs)
        return wrapper
    return _portal_auth_required
