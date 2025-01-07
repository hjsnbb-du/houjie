'use strict';

const Service = require('egg').Service;

class DashboardService extends Service {
  async getStats() {
    // Mock data for statistics
    return {
      workOrders: {
        newToday: 15,
        completedToday: 12,
        totalCompleted: 156,
        pending: 45
      },
      customers: {
        total: 280,
        active: 180,
        followUp: 65,
        expired: 35
      }
    };
  }

  async getTrends() {
    // Generate mock data for the last 30 days
    const trends = [];
    const customerTrends = [];
    const today = new Date();

    for (let i = 29; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      const dateStr = date.toISOString().split('T')[0];

      // Random data for work orders (10-30 range)
      trends.push({
        date: dateStr,
        count: Math.floor(Math.random() * 20) + 10
      });

      // Random data for customers (5-15 range)
      customerTrends.push({
        date: dateStr,
        count: Math.floor(Math.random() * 10) + 5
      });
    }

    return {
      workOrders: trends,
      customers: customerTrends
    };
  }
}

module.exports = DashboardService;
