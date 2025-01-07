'use strict';

const Controller = require('egg').Controller;

class DashboardController extends Controller {
  async getStats() {
    const { ctx, service } = this;
    try {
      const stats = await service.dashboard.getStats();
      ctx.body = {
        success: true,
        data: stats
      };
    } catch (error) {
      ctx.status = 500;
      ctx.body = {
        success: false,
        error: error.message
      };
    }
  }

  async getTrends() {
    const { ctx, service } = this;
    try {
      const trends = await service.dashboard.getTrends();
      ctx.body = {
        success: true,
        data: trends
      };
    } catch (error) {
      ctx.status = 500;
      ctx.body = {
        success: false,
        error: error.message
      };
    }
  }
}

module.exports = DashboardController;
