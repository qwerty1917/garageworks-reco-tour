from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'toureco.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('toureco_app.urls', namespace='toureco_app')),
    url(r'^admin/', include(admin.site.urls)),
]
