import { useState, useEffect } from 'react';
import { getApplications, updateApplicationStatus } from '@/services/api';

interface Application {
    id: string;
    full_name: string;
    email: string;
    status: string;
    social_accounts: Array<{
        platform: string;
        username: string;
        followers_count: number;
    }>;
    created_at: string;
}

export default function AdminDashboard() {
    const [applications, setApplications] = useState<Application[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchApplications();
    }, []);

    const fetchApplications = async () => {
        try {
            const data = await getApplications();
            setApplications(data);
        } catch (error) {
            console.error('Error fetching applications:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleStatusUpdate = async (id: string, status: string) => {
        try {
            await updateApplicationStatus(id, status);
            fetchApplications(); // Refresh the list
        } catch (error) {
            console.error('Error updating status:', error);
        }
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-2xl font-bold mb-6">Influencer Applications</h1>
            <div className="overflow-x-auto">
                <table className="min-w-full bg-white">
                    <thead>
                        <tr className="bg-gray-100">
                            <th className="px-6 py-3 text-left">Name</th>
                            <th className="px-6 py-3 text-left">Email</th>
                            <th className="px-6 py-3 text-left">Social Media</th>
                            <th className="px-6 py-3 text-left">Status</th>
                            <th className="px-6 py-3 text-left">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {applications.map((app) => (
                            <tr key={app.id} className="border-b">
                                <td className="px-6 py-4">{app.full_name}</td>
                                <td className="px-6 py-4">{app.email}</td>
                                <td className="px-6 py-4">
                                    {app.social_accounts.map((account) => (
                                        <div key={account.username}>
                                            {account.platform}: {account.followers_count} followers
                                        </div>
                                    ))}
                                </td>
                                <td className="px-6 py-4">
                                    <span className={`px-2 py-1 rounded ${
                                        app.status === 'approved' ? 'bg-green-100 text-green-800' :
                                        app.status === 'rejected' ? 'bg-red-100 text-red-800' :
                                        'bg-yellow-100 text-yellow-800'
                                    }`}>
                                        {app.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4">
                                    <select
                                        value={app.status}
                                        onChange={(e) => handleStatusUpdate(app.id, e.target.value)}
                                        className="border rounded px-2 py-1"
                                    >
                                        <option value="pending">Pending</option>
                                        <option value="approved">Approve</option>
                                        <option value="rejected">Reject</option>
                                    </select>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
} 