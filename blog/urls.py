from django.contrib import admin
from django.urls import path, include
from . import views
# from rest_framework.routers import DefaultRouter
# from blog.api import MessageModelViewSet, UserModelViewSet

# router = DefaultRouter()
# router.register(r'message', MessageModelViewSet, basename='message-api')
# router.register(r'user', UserModelViewSet, basename='user-api')

urlpatterns = [
    # path(r'notifications/api/v1/', include(router.urls)),
    # path('notifications/chat/incnum/',views.inc_num.as_view(),name="inc-num"),
    # path('notifications/chat/getusers/',views.get_users.as_view(),name="get-users"),
    path('getsea/',views.get_search.as_view(),name="get-sea"),
    # path('notifications/chat/putnotif/',views.put_notif.as_view(),name="put-notif"),
    # path('notifications/chat/removenotif/',views.remove_notif.as_view(),name="remove-notif"),
    # path('notifications/chat/userinp/',views.chat_user.as_view(),name="user-inp"),
    # path('notifications/chat/getmessages/',views.get_messages.as_view(),name="get-messages"),
    path('post/sendrequest/',views.send_request.as_view(),name="send-request"),
    path('',views.home,name="home"), #home includes header, container-box,modal
    path('search/',views.search, name="search"),
    path('search/delete',views.sea_delete.as_view(),name="delete_sea"),
    path('login/',views.user_login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('register/',views.register,name="register"),
    path('about/',views.about,name="about"),
    path('faqs/',views.faqs,name="faqs"),
    path('contact/',views.contact_us,name="contact"),
    path('feedback/',views.feedback_us,name="feedback"),
    path('contact/send/',views.send_msg,name="send-msg"),
    path('feedback/send/',views.send_feedback,name="send-feedback"),
    path('faqs/search/',views.faqs_search,name="faqs-search"),
    path('check_user',views.check_user.as_view(),name="check-user"),
    path('check_password',views.check_password.as_view(),name="check-password"),
    path('<str:sec>/',views.base,name="base"),
    path('uploadpost/sel-submit',views.sel_submit,name="sel-submit"),
    path('settings/prof-update',views.prof_update,name="prof-update"),
    path('settings/prof-update/del-dp',views.dp_delete.as_view(),name="del_dp"),
    path('settings/change-password',views.change_password,name="change-password"),
    path('settings/theme/light',views.theme_light.as_view(),name="theme-light"),
    path('settings/theme/dark',views.theme_dark.as_view(),name="theme-dark"),
    path('post/<sha>/',views.open_post,name="open-post"),
    path('post/like',views.like_post.as_view(),name="like-post"),
    path('post/<sha>/edit',views.post_edit,name="edit"),
    path('post/update',views.post_update,name="update_post"),
    path('post/delete',views.post_delete.as_view(),name="delete_post"),
    path('post/chan',views.post_chan.as_view(),name="chan_post"),
    path('post/img/del',views.img_delete.as_view(),name="del_img"),
]