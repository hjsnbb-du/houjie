'use strict';

module.exports = app => {
  const { STRING, INTEGER, DATE } = app.Sequelize;

  const User = app.model.define('user', {
    id: {
      type: INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    username: {
      type: STRING(30),
      allowNull: false,
      unique: true,
    },
    password: {
      type: STRING(100),
      allowNull: false,
    },
    email: {
      type: STRING(100),
      allowNull: false,
      unique: true,
    },
    created_at: DATE,
    updated_at: DATE,
  });

  return User;
};
