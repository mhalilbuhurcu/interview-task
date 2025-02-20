from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Influencer, SocialMediaAccount
from .serializers import InfluencerSerializer
from scraper.social_media_scraper import SocialMediaScraper

# Create your views here.

class InfluencerViewSet(viewsets.ModelViewSet):
    queryset = Influencer.objects.all()
    serializer_class = InfluencerSerializer
    scraper = SocialMediaScraper()  # Initialize the scraper here

    def get_queryset(self):
        return Influencer.objects.all().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Debugging line
        try:
            social_accounts = request.data.get('socialAccounts', [])
            print("Social Accounts:", social_accounts)  # Debugging line

            # Validate that at least one username is provided
            if not any(account.get('username', '').strip() for account in social_accounts):
                return Response(
                    {"error": "En az bir sosyal medya kullanıcı adı sağlamalısınız."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create or update the influencer
            influencer_email = request.data.get('email')
            influencer, created = Influencer.objects.update_or_create(
                email=influencer_email,
                defaults={
                    'full_name': request.data.get('fullName'),
                    'phone_number': request.data.get('phoneNumber'),
                    'collaboration_history': request.data.get('collaborationHistory'),
                    'status': request.data.get('status', 'pending'),
                    'content_types': request.data.get('content_types', [])
                }
            )

            # Fetch follower counts for provided social accounts
            for account_data in social_accounts:
                username = account_data.get('username')
                platform = account_data.get('platform')

                # Only fetch followers if username is provided
                if username:
                    followers_count = None
                    if platform == 'instagram':
                        followers_count = self.scraper.get_instagram_followers_instaloader(username)
                    elif platform == 'twitter':
                        followers_count = self.scraper.get_twitter_followers(username)
                    elif platform == 'tiktok':
                        followers_count = self.scraper.get_tiktok_followers(username)

                    # Update or create the influencer's social account data with followers count
                    SocialMediaAccount.objects.update_or_create(
                        influencer=influencer,
                        platform=platform,
                        username=username,  # Ensure username is included for uniqueness
                        defaults={'followers_count': followers_count}
                    )

            return Response({"message": "Influencer created/updated successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

class SocialMediaViewSet(viewsets.ViewSet):
    scraper = SocialMediaScraper()

    @action(detail=False, methods=['post'])
    def login_instagram(self, request):
        username = request.data.get('username')
        
        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the followers count
            followers = self.scraper.get_instagram_followers_instaloader(username)
            
            if followers is not None:
                influencer_email = request.data.get('email')
                influencer = get_object_or_404(Influencer, email=influencer_email)

                # Save the followers count to the SocialMediaAccount model
                SocialMediaAccount.objects.update_or_create(
                    influencer=influencer,
                    platform='instagram',
                    defaults={'username': username, 'followers_count': followers}
                )
            
                return Response({'followers': followers}, status=status.HTTP_200_OK)

            return Response({'error': 'Followers count could not be fetched.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            print(f"Error fetching Instagram followers: {e}")  # Debugging line
            return Response({'error': 'An error occurred while fetching followers.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def login_twitter(self, request):
        username = request.data.get('username')
        
        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            followers = self.scraper.get_twitter_followers(username)
            
            if followers is not None:
                influencer_email = request.data.get('email')
                influencer = get_object_or_404(Influencer, email=influencer_email)

                # Save the followers count to the SocialMediaAccount model
                SocialMediaAccount.objects.update_or_create(
                    influencer=influencer,
                    platform='twitter',
                    username=username,  # Ensure username is included for uniqueness
                    defaults={'followers_count': followers}
                )
            
            return Response({'followers': followers}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error fetching Twitter followers: {e}")  # Debugging line
            return Response({'error': 'An error occurred while fetching followers.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    async def login_tiktok(self, request):
        username = request.data.get('username')
        
        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Await the followers count fetching
            followers = await self.scraper.get_tiktok_followers(username)
            
            if followers is not None:
                return Response({'followers': followers}, status=status.HTTP_200_OK)
            
            return Response({'error': 'Followers count could not be fetched.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            print(f"Error fetching TikTok followers: {e}")  # Debugging line
            return Response({'error': 'An error occurred while fetching followers.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
