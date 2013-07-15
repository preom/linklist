from django.conf.urls import url, patterns

urlpatterns = patterns("",
    url(r'^$', 'linklist.views.index'),
    url(r'^index$', 'linklist.views.index'),
    url(r'^signup$', 'linklist.views.signup'),
    url(r'^add_url_script$', 'linklist.views.addUrlScript'),
    url(r'^delete_url_script$', 'linklist.views.deleteUrlScript'),
    url(r'^addurl$', 'linklist.views.addUrl'),
    url(r'^link_list$', 'linklist.views.linkList'),
    url(r'^checkuser$', 'linklist.views.isExistingUser'),
    url(r'^isExistingUser$', 'linklist.views.isExistingUser'),
    url(r'^users$', 'linklist.views.users'),
    url(r'^adduser$', 'linklist.views.adduser'),
    url(r'^user_login$', 'linklist.views.user_login'),
)
