import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';

export default function ThankYou() {
    const router = useRouter();

    useEffect(() => {
        // Redirect to home after 5 seconds
        const timeout = setTimeout(() => {
            router.push('/');
        }, 5000);

        return () => clearTimeout(timeout);
    }, [router]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full space-y-8 text-center">
                <div>
                    <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
                        Thank You for Your Application!
                    </h2>
                    <p className="mt-2 text-sm text-gray-600">
                        We have received your application and will review it shortly.
                        You will be notified via email about the status of your application.
                    </p>
                </div>
                <div className="mt-4">
                    <Link href="/" 
                          className="text-indigo-600 hover:text-indigo-500">
                        Return to Home Page
                    </Link>
                </div>
            </div>
        </div>
    );
} 