export interface SocialMediaAccount {
    platform: 'instagram' | 'tiktok' | 'twitter';
    username: string;
    followers_count: number;
    last_updated: string;
}

export interface Influencer {
    id: string;
    full_name: string;
    email: string;
    phone_number: string;
    content_type: string[];
    collaboration_history?: string;
    status: 'pending' | 'approved' | 'rejected';
    social_accounts: SocialMediaAccount[];
    created_at: string;
}

export interface ApplicationFormData {
    full_name: string;
    email: string;
    phone_number: string;
    content_type: string[];
    collaboration_history?: string;
    social_accounts: {
        platform: string;
        username: string;
    }[];
} 