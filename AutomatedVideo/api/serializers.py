from rest_framework import serializers

# Serializer for 'metadata' in the webhook
class MetadataSerializer(serializers.Serializer):
    _id = serializers.CharField()
    employee = serializers.EmailField()
    hostname = serializers.URLField()

# Serializer for the 'webhook' structure
class WebhookSerializer(serializers.Serializer):
    url = serializers.URLField()
    metadata = MetadataSerializer()

# Serializer for the 'audio' in template
class AudioSerializer(serializers.Serializer):
    audio_path = serializers.URLField()
    audioDuration = serializers.FloatField()

# Serializer for the 'CNBCVideo' in the template
class CNBCVideoSerializer(serializers.Serializer):
    url = serializers.URLField()
    pause_duration = serializers.FloatField()

# Serializer for the 'footages' in the template
class FootageSerializer(serializers.Serializer):
    url = serializers.URLField()
    pause_duration = serializers.FloatField()

# Serializer for the 'intro' section of the template
class IntroSerializer(serializers.Serializer):
    CNBCVideo = CNBCVideoSerializer()
    footages = FootageSerializer(many=True)
    audio_path = serializers.URLField()
    audioDuration = serializers.FloatField()

# Serializer for the content section of the template
class ContentSerializer(serializers.Serializer):
    text = serializers.CharField()
    CNBCVideo = CNBCVideoSerializer()
    footages = FootageSerializer(many=True)
    audio_path = serializers.URLField()
    audioDuration = serializers.FloatField()

# Serializer for the 'template' structure
class TemplateSerializer(serializers.Serializer):
    intro = IntroSerializer()
    content = ContentSerializer(many=True)

# Main serializer for the POST request
class PostRequestSerializer(serializers.Serializer):
    webhock = WebhookSerializer()
    template = TemplateSerializer()
