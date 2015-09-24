from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'toureco.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('toureco_app.urls', namespace='toureco_app')),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += patterns('',
    (r'^static/(?P.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
