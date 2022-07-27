from message.api.views import ( api_detail_message_view,
                             api_post_message_view,
                             api_delete_message_view,
                             api_update_message_view,)
from django.urls import path

app_name = 'message'

urlpatterns = [
    path('<slug>/', api_detail_message_view, name="detail"),
    path('<slug>/delete', api_delete_message_view, name="delete"),
    path('<slug>/update', api_update_message_view, name="update"),
    path('messages', api_post_message_view, name="create"),

]