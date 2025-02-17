from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Influencer, SocialMediaAccount
from .serializers import InfluencerSerializer
from scraper.social_media_scraper import SocialMediaScraper
import asyncio

# Create your views here.

class InfluencerViewSet(viewsets.ModelViewSet):
    queryset = Influencer.objects.all()
    serializer_class = InfluencerSerializer

    def get_queryset(self):
        return Influencer.objects.all().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Debugging line
        try:
            data = {
                'full_name': request.data.get('fullName'),
                'email': request.data.get('email'),
                'phone_number': request.data.get('phoneNumber'),
                'content_types': request.data.get('contentTypes', []),
                'collaboration_history': request.data.get('collaborationHistory'),
                'social_accounts': request.data.get('socialAccounts', [])
            }

            print("Data to be serialized:", data)  # Debugging line

            serializer = self.get_serializer(data=data)
            if not serializer.is_valid():
                print("Validation errors:", serializer.errors)  # Debugging line
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED, 
                headers=headers
            )
        except Exception as e:
            print("Error creating influencer:", str(e))
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        influencer = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in ['pending', 'approved', 'rejected']:
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        influencer.status = new_status
        influencer.save()
        
        return Response(self.get_serializer(influencer).data)
