from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GoIndia.views.home', name='home'),
    # url(r'^GoIndia/', include('GoIndia.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'GoIndi.views.home'),
    url(r'main$', 'GoIndi.views.main'),
    url(r'train$', 'GoIndi.views.trainapi'),
    url(r'train/availability$', 'GoIndi.views.trainavailabilityapi'),
    url(r'flight$', 'GoIndi.views.flightapi'),
    url(r'flight/direct$', 'GoIndi.views.flightdirectandnearapi'),
    url(r'flight/biggest$', 'GoIndi.views.flightbigapi'),
    url(r'flight/neartobig$', 'GoIndi.views.flightnearbigapi'),
    url(r'flight/bigtonear$', 'GoIndi.views.flightbignearapi'),
    url(r'bus$', 'GoIndi.views.busapi'),
    url(r'test$', 'GoIndi.views.test'),
    url(r'init$', 'GoIndi.views.traininit'),
)
