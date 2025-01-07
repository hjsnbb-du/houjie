'use strict';

const Service = require('egg').Service;
const bcrypt = require('bcrypt');

class AuthService extends Service {
  async register({ username, password, email }) {
    const { ctx } = this;

    // Check if username already exists
    const existingUser = await ctx.model.User.findOne({ where: { username } });
    if (existingUser) {
      throw new Error('Username already exists');
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Create user
    const user = await ctx.model.User.create({
      username,
      password: hashedPassword,
      email,
    });

    return user;
  }

  async login({ username, password }) {
    const { ctx, app } = this;

    // Find user
    const user = await ctx.model.User.findOne({ where: { username } });
    if (!user) {
      throw new Error('User not found');
    }

    // Verify password
    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) {
      throw new Error('Invalid password');
    }

    // Generate token
    const token = app.jwt.sign(
      {
        id: user.id,
        username: user.username,
      },
      app.config.jwt.secret,
      {
        expiresIn: '1d',
      }
    );

    return { token, user };
  }
}

module.exports = AuthService;
