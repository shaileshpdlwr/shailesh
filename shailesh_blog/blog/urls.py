from django.urls import path,re_path
from blog import views

urlpatterns = [
    path('',views.post_list_view),
    path('detail/<slug:slug>',views.post_detail,name='post_detail'),
    path('tag/<slug:tag_slug>/',views.post_list_view,name='post_by_tag'),
   # re_path(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list_view, name='post_list_view_by_tag_name'),
    path('blog/',views.PostListView.as_view()),
    path('mail/<id>/',views.mail_send_view),
    # path('login/'.views.)

]

#Reverse for 'post_list_by_tag_name' not found. 'post_list_by_tag_name' is not a valid view function or pattern name.

#post_list_view_by_tag_name' 