import { useState, useEffect } from 'react';
import { DashboardStats, DashboardTrends } from '../components/dashboard/types';

const CACHE_KEY = 'dashboard_data';
const CACHE_EXPIRY = 5 * 60 * 1000; // 5 minutes
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

interface CachedData {
  stats: DashboardStats;
  trends: DashboardTrends;
  timestamp: number;
}

interface UseDashboardDataReturn {
  stats: DashboardStats | null;
  trends: DashboardTrends | null;
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

const getCachedData = (): CachedData | null => {
  const cached = localStorage.getItem(CACHE_KEY);
  if (!cached) return null;

  const data = JSON.parse(cached) as CachedData;
  if (Date.now() - data.timestamp > CACHE_EXPIRY) {
    localStorage.removeItem(CACHE_KEY);
    return null;
  }

  return data;
};

export const useDashboardData = (): UseDashboardDataReturn => {
  const [stats, setStats] = useState<DashboardStats | null>(() => {
    const cached = getCachedData();
    return cached?.stats || null;
  });
  const [trends, setTrends] = useState<DashboardTrends | null>(() => {
    const cached = getCachedData();
    return cached?.trends || null;
  });
  const [loading, setLoading] = useState(!stats || !trends);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Clear existing cache
      localStorage.removeItem(CACHE_KEY);

      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      console.log('Fetching from:', `${API_BASE_URL}/api/dashboard/stats`); // Debug log
      console.log('Using token:', token); // Debug log

      const [statsResponse, trendsResponse] = await Promise.all([
        fetch(`${API_BASE_URL}/api/dashboard/stats`, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }),
        fetch(`${API_BASE_URL}/api/dashboard/trends`, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        })
      ]);

      if (!statsResponse.ok || !trendsResponse.ok) {
        console.error('Stats response:', statsResponse.status, await statsResponse.text());
        console.error('Trends response:', trendsResponse.status, await trendsResponse.text());
        throw new Error('Failed to fetch dashboard data');
      }

      const statsData = await statsResponse.json();
      const trendsData = await trendsResponse.json();

      console.log('Stats data:', statsData); // Debug log
      console.log('Trends data:', trendsData); // Debug log

      const newStats = statsData.data;  // Access the data property from the response
      const newTrends = trendsData.data;

      // Update cache
      localStorage.setItem(CACHE_KEY, JSON.stringify({
        stats: newStats,
        trends: newTrends,
        timestamp: Date.now()
      }));

      setStats(newStats);
      setTrends(newTrends);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('An error occurred'));
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!stats || !trends) {
      fetchData();
    }

    const interval = setInterval(fetchData, CACHE_EXPIRY);

    return () => {
      clearInterval(interval);
    };
  }, []);

  return {
    stats,
    trends,
    loading,
    error,
    refetch: fetchData
  };
};
