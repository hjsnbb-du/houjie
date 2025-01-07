/* eslint valid-jsdoc: "off" */

/**
 * @param {Egg.EggAppInfo} appInfo app info
 */
module.exports = appInfo => {
  /**
   * built-in config
   * @type {Egg.EggAppConfig}
   **/
  const config = exports = {};

  // use for cookie sign key, should change to your own and keep security
  config.keys = appInfo.name + '_1736237212577_5028';

  // add your middleware config here
  config.middleware = ['errorHandler'];

  // cluster configuration
  config.cluster = {
    listen: {
      port: 7003,
      hostname: '0.0.0.0',
    },
  };

  // add sequelize config
  config.sequelize = {
    dialect: 'mysql',
    host: 'localhost',
    port: 3306,
    database: 'erp_db',
    username: 'erp_user',
    password: 'erp_password',
    define: {
      timestamps: true,
      underscored: true,
    },
  };

  // add security config
  config.security = {
    csrf: {
      enable: false,
    },
    domainWhiteList: [
      'http://172.16.5.2:4173',
      'http://172.16.5.2:7004'
    ],
  };

  // add cors config
  config.cors = {
    origin: '*',
    allowMethods: 'GET,HEAD,PUT,POST,DELETE,PATCH,OPTIONS',
    credentials: true
  };

  // add jwt config
  config.jwt = {
    secret: 'erp-jwt-secret',
  };

  return {
    ...config,
  };
};
