// This file is created by egg-ts-helper@1.35.1
// Do not modify this file!!!!!!!!!
/* eslint-disable */

import 'egg';
import ExportCustomer = require('../../../app/model/customer');
import ExportUser = require('../../../app/model/user');
import ExportWorkOrder = require('../../../app/model/workOrder');

declare module 'egg' {
  interface IModel {
    Customer: ReturnType<typeof ExportCustomer>;
    User: ReturnType<typeof ExportUser>;
    WorkOrder: ReturnType<typeof ExportWorkOrder>;
  }
}
