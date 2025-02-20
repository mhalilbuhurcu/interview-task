import { useState } from 'react';
import { useRouter } from 'next/router';
import { FaInstagram, FaTwitter, FaTiktok } from 'react-icons/fa';

interface SocialMediaAccount {
  platform: 'instagram' | 'tiktok' | 'twitter';
  username: string;
}

interface FormData {
  fullName: string;
  email: string;
  phoneNumber: string;
  socialAccounts: SocialMediaAccount[];
  contentTypes: string[];
  collaborationHistory: string;
}

const CONTENT_TYPES = [
  'Moda',
  'Teknoloji',
  'Oyun',
  'Yaşam Tarzı',
  'Seyahat',
  'Yemek',
  'Spor',
  'Güzellik',
  'Eğitim',
  'Eğlence'
];

// Helper function to capitalize the first letter
const capitalizeFirstLetter = (string: string) => {
  return string.charAt(0).toUpperCase() + string.slice(1);
};

export default function ApplicationForm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    fullName: '',
    email: '',
    phoneNumber: '',
    socialAccounts: [
      { platform: 'instagram', username: '' },
      { platform: 'tiktok', username: '' },
      { platform: 'twitter', username: '' }
    ],
    contentTypes: [],
    collaborationHistory: ''
  });
  const [error, setError] = useState<string | null>(null);

  const handleSocialAccountChange = (platform: 'instagram' | 'tiktok' | 'twitter', username: string) => {
    setFormData(prev => ({
      ...prev,
      socialAccounts: prev.socialAccounts.map(account => 
        account.platform === platform ? { ...account, username } : account
      )
    }));
  };

  const handleContentTypeChange = (type: string) => {
    setFormData(prev => ({
      ...prev,
      contentTypes: prev.contentTypes.includes(type)
        ? prev.contentTypes.filter(t => t !== type)
        : [...prev.contentTypes, type]
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null); // Reset error message

    try {
        // Filter out social accounts with empty usernames
        const validSocialAccounts = formData.socialAccounts.filter(account => account.username.trim() !== '');

        // Validate that at least one username is provided
        if (validSocialAccounts.length === 0) {
            setError('En az bir sosyal medya kullanıcı adı sağlamalısınız.');
            setLoading(false);
            return;
        }

        // Fetch follower counts for each populated social media account
        const followerPromises = validSocialAccounts.map(async (account) => {
            const response = await fetch(`http://localhost:8000/api/social_media/login_${account.platform}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username: account.username }),
            });

            if (response.ok) {
                const data = await response.json();
                return { platform: account.platform, followers_count: data.followers };
            } else {
                console.error(`Failed to fetch followers for ${account.platform}`);
                return { platform: account.platform, followers_count: null };
            }
        });

        // Wait for all follower counts to be fetched
        const followersData = await Promise.all(followerPromises);

        // Update the formData with fetched follower counts
        const updatedSocialAccounts = validSocialAccounts.map(account => {
            const followerData = followersData.find(f => f.platform === account.platform);
            return {
                ...account,
                followers_count: followerData ? followerData.followers_count : null,
            };
        });

        // Now you can send the complete form data to your backend
        const response = await fetch('http://localhost:8000/api/influencers/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                ...formData, 
                social_accounts: updatedSocialAccounts 
            }),
        });

        if (!response.ok) {
            const errorText = await response.text(); // Get the response text
            throw new Error(`Error: ${response.status} - ${errorText}`); // Throw an error with the response text
        }

        const data = await response.json();
        router.push('/thank-you');

    } catch (error) {
        console.error('Error submitting form:', error);
        setError('Başvuru gönderilirken bir hata oluştu.'); // Display a user-friendly error message
    } finally {
        setLoading(false);
    }
  };

  const handleSocialMediaLogin = (platform: string) => {
    router.push(`/${platform}-login`);
  };

  return (
    <div className="max-w-lg mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4 text-center">Influencer Başvuru Formu</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">Ad Soyad</label>
          <input
            type="text"
            name="fullName"
            value={formData.fullName}
            onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
            required
            className="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">E-posta</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            required
            className="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">Telefon Numarası</label>
          <input
            type="tel"
            name="phoneNumber"
            value={formData.phoneNumber}
            onChange={(e) => setFormData({ ...formData, phoneNumber: e.target.value })}
            required
            className="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">Sosyal Medya Hesapları</label>
          {formData.socialAccounts.map((account, index) => (
            <div key={index} className="flex items-center mb-2 mt-2">
              <span className="flex items-center w-25">
                {account.platform === 'instagram' && <FaInstagram className="text-pink-500 mr-1" />}
                {account.platform === 'tiktok' && <FaTiktok className="text-black mr-1" />}
                {account.platform === 'twitter' && <FaTwitter className="text-blue-500 mr-1" />}
                <label className="text-sm font-medium text-gray-700">{capitalizeFirstLetter(account.platform)}</label>
              </span>
              <input
                type="text"
                name="username"
                placeholder="Kullanıcı Adı"
                value={account.username}
                onChange={(e) => handleSocialAccountChange(account.platform, e.target.value)}
                className="flex-1 border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 ml-2"
                style={{ minWidth: '200px' }}
              />                         
            </div>
            
          ))}
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">İçerik Türleri</label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mt-2">
            {CONTENT_TYPES.map((type) => (
              <label key={type} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={formData.contentTypes.includes(type)}
                  onChange={() => handleContentTypeChange(type)}
                  className="rounded text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">{type}</span>
              </label>
            ))}
          </div>
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">İşbirliği Geçmişi</label>
          <textarea
            name="collaborationHistory"
            value={formData.collaborationHistory}
            onChange={(e) => setFormData({ ...formData, collaborationHistory: e.target.value })}
            className="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Daha önce yaptığınız işbirliklerini buraya yazabilirsiniz..."
          />
        </div>
        
        {error && <p className="text-red-500">{error}</p>}
        
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white font-bold py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {loading ? 'Gönderiliyor...' : 'Başvuruyu Gönder'}
        </button>
      </form>
    </div>
  );
} 