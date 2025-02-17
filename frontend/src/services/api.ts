import axios from 'axios';
import { ApplicationFormData } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const submitApplication = async (formData: ApplicationFormData) => {
    try {
        const response = await api.post('/influencers/', formData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getApplications = async () => {
    try {
        const response = await api.get('/influencers/');
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const updateApplicationStatus = async (id: string, status: string) => {
    try {
        const response = await api.patch(`/influencers/${id}/update_status/`, { status });
        return response.data;
    } catch (error) {
        throw error;
    }
}; 