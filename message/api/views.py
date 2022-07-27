from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from account.models import Account
from message.models import MessagePost
from message.api.serializers import MessagePostSerializer

from rest_framework.throttling import UserRateThrottle

# permission classes for authentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_detail_message_view(request,slug):
    try:
        message_post = MessagePost.objects.get(slug=slug)
    except MessagePost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessagePostSerializer(message_post)
        return Response(serializer.data)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_message_view(request,slug):
    try:
        message_post = MessagePost.objects.get(slug=slug)
    except MessagePost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # For making sure the one who wrote it is updating the message/blog
    user = request.user
    if message_post.author != user:
        return Response({'response':'You do not have permission to edit it'})


    if request.method == 'PUT':
        serializer = MessagePostSerializer(message_post, data=request.data)
        data ={}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data = data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def api_delete_message_view(request,slug):
    try:
        message_post = MessagePost.objects.get(slug=slug)
    except MessagePost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # For making sure the one who wrote it is deleting the message/blog

    user = request.user
    if message_post.author != user:
        return Response({'response': 'You do not have permission to delete it'})

    if request.method == 'DELETE':
        operation = message_post.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)

@api_view(['POST',])
@throttle_classes([UserRateThrottle])
@permission_classes((IsAuthenticated,))

def api_post_message_view(request):
   account = request.user

   message_post = MessagePost(author=account)

   if request.method == "POST":
       serializer = MessagePostSerializer(message_post, data=request.data)

      # data ={}
       if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
