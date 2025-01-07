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
  config.keys = process.env.EGG_KEYS || appInfo.name + '_prod';

  // add your middleware config here
  config.middleware = ['errorHandler'];

  // add sequelize config
  config.sequelize = {
    dialect: 'mysql',
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 3306,
    database: process.env.DB_NAME || 'erp_db',
    username: process.env.DB_USER || 'erp_user',
    password: process.env.DB_PASSWORD || 'erp_password',
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
    domainWhiteList: [process.env.FRONTEND_URL || '*'],
  };

  // add cors config
  config.cors = {
    origin: process.env.FRONTEND_URL || '*',
    allowMethods: 'GET,HEAD,PUT,POST,DELETE,PATCH,OPTIONS',
  };

  // add jwt config
  config.jwt = {
    secret: process.env.JWT_SECRET || 'erp-jwt-secret-prod',
  };

  return {
    ...config,
  };
};
