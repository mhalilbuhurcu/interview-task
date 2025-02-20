import ApplicationForm from '@/components/ApplicationForm';
import Head from 'next/head';



export default function Home() {
    return (
        <>
            <Head>
                <title>Influencer Application Platform</title>
                <meta name="description" content="Apply to become an influencer" />
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <div className="min-h-screen bg-gray-50">
                <main className="container mx-auto px-4 py-8">
                    <h1 className="text-3xl font-bold text-center mb-8">
                        Influencer Application Platform
                    </h1>
                    <ApplicationForm />
                    
                </main>
            </div>
        </>
    );
} 