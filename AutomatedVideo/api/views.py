from rest_framework.views import APIView
from .serializers import PostRequestSerializer
from rest_framework.response import Response
from.tasks import create_video_task

class CreateVideoView(APIView):
    def post(self, request):
        serializer = PostRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                webhock = serializer.validated_data['webhock']
                template = serializer.validated_data['template']
                webhook_url = webhock['url']
                metadata = webhock['metadata']
                video_id = metadata['_id']
                employee_email = metadata['employee']
                employee_name = employee_email.split('@')[0]
                video_name = employee_name + video_id 
                directory_name = f"{video_name}"

                create_video_task.delay(template, video_name, metadata, webhook_url, directory_name)

                return Response({'response': "success"})
            except Exception as e:
                return Response({'error': str(e)}, status=500)
        else:
            return Response(serializer.errors, status=400)

class HealthCheckView(APIView):
    def get(self, request):
        return Response({'response': "success"},status=200)