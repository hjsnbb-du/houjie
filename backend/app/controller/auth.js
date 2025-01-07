'use strict';

const Controller = require('egg').Controller;

class AuthController extends Controller {
  async register() {
    const { ctx, service } = this;
    const { username, password, email } = ctx.request.body;

    try {
      const user = await service.auth.register({ username, password, email });
      ctx.body = {
        success: true,
        data: {
          id: user.id,
          username: user.username,
          email: user.email,
        },
      };
    } catch (error) {
      ctx.throw(400, error.message);
    }
  }

  async login() {
    const { ctx, service } = this;
    const { username, password } = ctx.request.body;

    try {
      const { token, user } = await service.auth.login({ username, password });
      ctx.body = {
        success: true,
        data: {
          token,
          user: {
            id: user.id,
            username: user.username,
            email: user.email,
          },
        },
      };
    } catch (error) {
      ctx.throw(401, error.message);
    }
  }
}

module.exports = AuthController;
