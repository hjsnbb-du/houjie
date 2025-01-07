/**
 * @param {Egg.Application} app - egg application
 */
module.exports = app => {
  const { router, controller } = app;
  router.get('/', controller.home.index);
  router.post('/api/auth/login', controller.auth.login);
  router.post('/api/auth/register', controller.auth.register);
  router.get('/api/dashboard/stats', controller.dashboard.getStats);
  router.get('/api/dashboard/trends', controller.dashboard.getTrends);
};
