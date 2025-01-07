'use strict';

module.exports = app => {
  const { STRING, INTEGER, ENUM, DATE } = app.Sequelize;

  const WorkOrder = app.model.define('work_order', {
    id: {
      type: INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    title: {
      type: STRING,
      allowNull: false
    },
    status: {
      type: ENUM('pending', 'completed'),
      defaultValue: 'pending',
      allowNull: false
    },
    customerId: {
      type: INTEGER,
      allowNull: true,
      references: {
        model: 'customers',
        key: 'id'
      },
      field: 'customer_id'
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
    tableName: 'work_orders',
    underscored: true,
    timestamps: true
  });

  WorkOrder.associate = function() {
    app.model.WorkOrder.belongsTo(app.model.Customer, {
      foreignKey: 'customerId',
      as: 'customer'
    });
  };

  return WorkOrder;
};
