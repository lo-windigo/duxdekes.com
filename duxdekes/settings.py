"""
Django settings for duxdekes project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from oscar import get_core_apps, OSCAR_MAIN_TEMPLATE_DIR
from oscar.defaults import *
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _


####################
# Default Settings #
####################

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1']
ROOT_URLCONF = 'duxdekes.urls'
WSGI_APPLICATION = 'duxdekes.wsgi.application'
# Required for sites framework
SITE_ID = 1

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'duxdekes',
    #'products',
    'django.contrib.flatpages',
    'compressor',
    'widget_tweaks',
] + get_core_apps( [
    'cart.basket',
    'cart.catalogue',
    'cart.checkout',
    'cart.dashboard',
    'cart.dashboard.catalogue',
    'cart.dashboard.orders',
    #'cart.dashboard.shipping',
    'cart.order',
    'cart.partner',
    'cart.shipping',
], )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
#    {
#        'NAME': 'oscar.apps.customer.auth_backends.EmailBackend',
#    },
#    {
#        'NAME': 'django.contrib.auth.backends.ModelBackend',
#    },
]

# Login redirect URL
LOGIN_REDIRECT_URL='/dashboard/'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'

# User-uploaded media files
# https://docs.djangoproject.com/en/1.10/ref/settings/#media-url
MEDIA_URL = '/media/'


##################
# Oscar settings #
##################
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

OSCAR_SHOP_NAME="Dux' Dekes"
OSCAR_SHOP_TAGLINE="Handcrafted decoys"
OSCAR_DEFAULT_CURRENCY = 'USD'
OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_INITIAL_LINE_STATUS = 'Pending'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Order Total Adjusted', 'Processed', 'Cancelled',),
    'Processed': ('Refunded', 'Cancelled',),
    'Order Total Adjusted': ('Charge Finalized', 'Refunded', 'Cancelled',),
    'Charge Finalized': ('Processed', 'Refunded', 'Cancelled',),
    'Refunded': (),
    'Cancelled': (),
    'Needs Adjustment': (), # Legacy
}
OSCAR_HOMEPAGE = reverse_lazy('home')
OSCAR_ALLOW_ANON_CHECKOUT = True
OSCAR_ALLOW_ANON_REVIEWS = False
OSCAR_HIDDEN_FEATURES = [
    'reviews',
    'wishlists',
]

OSCAR_DASHBOARD_NAVIGATION = [
    {
        'label': _('Dashboard'),
        'icon': 'icon-th-list',
        'url_name': 'dashboard:index',
    },
    {
        'label': _('Catalogue'),
        'icon': 'icon-sitemap',
        'children': [
            {
                'label': _('Categories'),
                'url_name': 'dashboard:catalogue-category-list',
            },
#            {
#                'label': _('Ranges'),
#                'url_name': 'dashboard:range-list',
#            },
#            {
#                'label': _('Low stock alerts'),
#                'url_name': 'dashboard:stock-alert-list',
#            },
#            {
#                'label': _('Bauer Instructions'),
#                'url_name': 'dashboard:bauer',
#            },
            {
                'label': _('Unfinished Blanks'),
                'url_name': 'dashboard:catalogue-unfinished-list',
            },
            {
                'label': _('Finished Decoys'),
                'url_name': 'dashboard:catalogue-finished-list',
            },
            {
                'label': _('Instructions'),
                'url_name': 'dashboard:catalogue-instructions-list',
            },
            {
                'label': _('Product Types'),
                'url_name': 'dashboard:catalogue-class-list',
            },
            {
                'label': _('Products'),
                'url_name': 'dashboard:catalogue-product-list',
            },
        ]
    },
    {
        'label': _('Fulfilment'),
        'icon': 'icon-shopping-cart',
        'children': [
            {
                'label': _('Orders'),
                'url_name': 'dashboard:order-list',
            },
            {
                'label': _('Statistics'),
                'url_name': 'dashboard:order-stats',
            },
            {
                'label': _('Shipping Cost Report'),
                'url_name': 'dashboard:order-history',
            },
            {
                'label': _('Box Sizes'),
                'url_name': 'dashboard:shipping:box-list',
            },
#            {
#                'label': _('Partners'),
#                'url_name': 'dashboard:partner-list',
#            },
            # The shipping method dashboard is disabled by default as it might
            # be confusing. Weight-based shipping methods aren't hooked into
            # the shipping repository by default (as it would make
            # customising the repository slightly more difficult).
            # {
            #     'label': _('Shipping charges'),
            #     'url_name': 'dashboard:shipping-method-list',
            # },
        ]
    },
#    {
#        'label': _('Customers'),
#        'icon': 'icon-group',
#        'children': [
#            {
#                'label': _('Customers'),
#                'url_name': 'dashboard:users-index',
#            },
#            {
#                'label': _('Stock alert requests'),
#                'url_name': 'dashboard:user-alert-list',
#            },
#        ]
#    },
#    {
#        'label': _('Offers'),
#        'icon': 'icon-bullhorn',
#        'children': [
#            {
#                'label': _('Offers'),
#                'url_name': 'dashboard:offer-list',
#            },
#            {
#                'label': _('Vouchers'),
#                'url_name': 'dashboard:voucher-list',
#            },
#        ],
#    },
    {
        'label': _('Content'),
        'icon': 'icon-folder-close',
        'children': [
            {
                'label': _('Content blocks'),
                'url_name': 'dashboard:promotion-list',
            },
            {
                'label': _('Content blocks by page'),
                'url_name': 'dashboard:promotion-list-by-page',
            },
            {
                'label': _('Pages'),
                'url_name': 'dashboard:page-list',
            },
            {
                'label': _('Email templates'),
                'url_name': 'dashboard:comms-list',
            },
#            {
#                'label': _('Reviews'),
#                'url_name': 'dashboard:reviews-list',
#            },
        ]
    },
#    {
#        'label': _('Reports'),
#        'icon': 'icon-bar-chart',
#        'url_name': 'dashboard:reports-index',
#    },
    {
        'label': _('Settings'),
        'icon': 'icon-cog',
        'url_name': 'dashboard:settings:index',
    },
]



##################
# Local settings #
##################

# Import the local settings file (borrowed from Mezzanine)
f = os.path.join(BASE_DIR, "duxdekes/local_settings.py")
if os.path.exists(f):
    import sys
    import types
    module_name = "local_settings"
    module = types.ModuleType(module_name)
    module.__file__ = f
    sys.modules[module_name] = module
    exec(open(f, "rb").read())


##
## Settings that extend local settings
##

# Append Domains defined in local settings
ALLOWED_HOSTS += [
	DOMAIN,
	"." + DOMAIN
]

# Template details
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            OSCAR_MAIN_TEMPLATE_DIR,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ],
        },
    },
]


###################
# Sorl thumbnails #
###################
THUMBNAIL_DEBUG = DEBUG


####################
# Signal Receivers #
####################

from duxdekes import receivers
