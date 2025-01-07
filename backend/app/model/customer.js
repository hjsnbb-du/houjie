'use strict';

module.exports = app => {
  const { STRING, INTEGER, ENUM, DATE } = app.Sequelize;

  const Customer = app.model.define('customer', {
    id: {
      type: INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    name: {
      type: STRING,
      allowNull: false
    },
    status: {
      type: ENUM('active', 'follow_up', 'expired'),
      defaultValue: 'active',
      allowNull: false
    },
    createdAt: {
      type: DATE,
      field: 'created_at'
    },
    updatedAt: {
      type: DATE,
      field: 'updated_at'
    }
  }, {
    tableName: 'customers',
    underscored: true,
    timestamps: true
  });

  Customer.associate = function() {
    app.model.Customer.hasMany(app.model.WorkOrder, {
      foreignKey: 'customerId',
      as: 'workOrders'
    });
  };

  return Customer;
};
