import { useState } from 'react';
import { useRouter } from 'next/router';


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

    console.log('Form Data:', formData);  // Debugging line

    try {
      const response = await fetch('http://localhost:8000/api/influencers/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        router.push('/thank-you');
      } else {
        const errorData = await response.json();  // Get the error response
        throw new Error(`Başvuru gönderilirken bir hata oluştu: ${JSON.stringify(errorData)}`);
      }
    } catch (error) {
      alert('Bir hata oluştu. Lütfen tekrar deneyin.');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
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
            <div key={index} className="flex space-x-2 mb-2">
              <input
                type="text"
                name="platform"
                placeholder="Platform"
                value={account.platform}
                onChange={(e) => handleSocialAccountChange(account.platform, e.target.value)}
                className="flex-1 border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <input
                type="text"
                name="username"
                placeholder="Kullanıcı Adı"
                value={account.username}
                onChange={(e) => handleSocialAccountChange(account.platform, e.target.value)}
                className="flex-1 border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          ))}
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">İçerik Türleri</label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
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