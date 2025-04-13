from rest_framework import serializers

class MetadataSerializer(serializers.Serializer):
    _id = serializers.CharField()
    employee = serializers.EmailField()

# Webhook Serializer
class WebhookSerializer(serializers.Serializer):
    url = serializers.URLField()
    metadata = MetadataSerializer()
    
class TranscriptAudioSerializer(serializers.Serializer):
    url = serializers.URLField()
    start_time = serializers.FloatField()

class IntroSerializer(serializers.Serializer):
    url = serializers.URLField()
    pause_duration = serializers.FloatField()
    with_audio = serializers.BooleanField()

class OutroSerializer(serializers.Serializer):
    url = serializers.URLField()
    pause_duration = serializers.FloatField()
    with_audio = serializers.BooleanField()

class ContentSerializer(serializers.Serializer):
    url = serializers.URLField()
    pause_duration = serializers.FloatField()
    with_audio = serializers.BooleanField()

class TemplateSerializer(serializers.Serializer):
    transcript_audio = TranscriptAudioSerializer(many=True, required=False)
    intro = IntroSerializer(many=True, required=False)
    content = ContentSerializer(many=True, required=False)
    outro = OutroSerializer(many=True, required=False)

class PostRequestSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    webhock = WebhookSerializer()
    template = TemplateSerializer()
