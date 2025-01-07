// This file is created by egg-ts-helper@1.35.1
// Do not modify this file!!!!!!!!!
/* eslint-disable */

import 'egg';
import ExportAuth = require('../../../app/controller/auth');
import ExportDashboard = require('../../../app/controller/dashboard');
import ExportHome = require('../../../app/controller/home');

declare module 'egg' {
  interface IController {
    auth: ExportAuth;
    dashboard: ExportDashboard;
    home: ExportHome;
  }
}
