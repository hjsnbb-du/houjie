'use strict';

module.exports = () => {
  return async function errorHandler(ctx, next) {
    try {
      await next();
    } catch (err) {
      // All errors are caught here
      ctx.app.emit('error', err, ctx);

      const status = err.status || 500;

      // Error response
      ctx.body = {
        success: false,
        message: err.message,
      };

      ctx.status = status;
    }
  };
};
