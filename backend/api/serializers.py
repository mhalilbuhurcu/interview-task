from rest_framework import serializers
from .models import Influencer, SocialMediaAccount

class SocialMediaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaAccount
        fields = ['platform', 'username', 'followers_count', 'last_updated']

class InfluencerSerializer(serializers.ModelSerializer):
    social_accounts = SocialMediaAccountSerializer(many=True)
    content_types = serializers.ListField(write_only=True, required=True)
    contentTypes = serializers.ListField(source='content_types', read_only=True)

    class Meta:
        model = Influencer
        fields = [
            'id', 'full_name', 'email', 'phone_number',
            'content_types', 'contentTypes', 'collaboration_history',
            'status', 'social_accounts', 'created_at'
        ]

    def create(self, validated_data):
        social_accounts_data = validated_data.pop('social_accounts', [])
        content_types = validated_data.pop('content_types', [])
        
        influencer = Influencer.objects.create(
            **validated_data,
            content_types=content_types
        )

        for account_data in social_accounts_data:
            SocialMediaAccount.objects.create(
                influencer=influencer,
                **account_data
            )

        return influencer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['contentTypes'] = instance.content_types
        return representation
