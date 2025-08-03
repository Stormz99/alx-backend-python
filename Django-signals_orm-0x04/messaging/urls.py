from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/unread/', views.unread_inbox, name='unread_inbox'),
    path('thread/<int:message_id>/', views.threaded_conversation, name='threaded_conversation'),
]
