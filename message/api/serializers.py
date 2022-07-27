from rest_framework import serializers
from message.models import MessagePost
from account.models import Account

class MessagePostSerializer(serializers.ModelSerializer):

    created_by = serializers.SerializerMethodField('get_all_about_author')

    class Meta:
        model = MessagePost
        fields = ['id','message','created_at','updated_at','created_by']

    def get_all_about_author(self, message_post):
            id = message_post.author.pk
            username = message_post.author.username
            email = message_post.author.email
            created_by = {'id':id, 'username': username, 'email':email}
            return created_by



