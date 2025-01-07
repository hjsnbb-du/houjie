'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.bulkInsert('customers', [
      {
        name: '测试客户1',
        status: 'active',
        created_at: new Date(),
        updated_at: new Date()
      },
      {
        name: '测试客户2',
        status: 'follow_up',
        created_at: new Date(),
        updated_at: new Date()
      },
      {
        name: '测试客户3',
        status: 'expired',
        created_at: new Date(),
        updated_at: new Date()
      }
    ]);

    const customers = await queryInterface.sequelize.query(
      'SELECT id from customers;'
    );
    const customerRows = customers[0];

    await queryInterface.bulkInsert('work_orders', [
      {
        title: '工单1',
        status: 'pending',
        customer_id: customerRows[0].id,
        created_at: new Date(),
        updated_at: new Date()
      },
      {
        title: '工单2',
        status: 'completed',
        customer_id: customerRows[0].id,
        created_at: new Date(),
        updated_at: new Date()
      },
      {
        title: '工单3',
        status: 'pending',
        customer_id: customerRows[1].id,
        created_at: new Date(),
        updated_at: new Date()
      }
    ]);
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.bulkDelete('work_orders', null, {});
    await queryInterface.bulkDelete('customers', null, {});
  }
};
