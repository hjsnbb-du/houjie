"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getAsyncLocalStorage = exports.kGALS = void 0;
const async_hooks_1 = require("async_hooks");
exports.kGALS = Symbol.for('gals#asyncLocalStorage');
function getAsyncLocalStorage() {
    const g = globalThis;
    if (!g[exports.kGALS]) {
        g[exports.kGALS] = new async_hooks_1.AsyncLocalStorage();
    }
    return g[exports.kGALS];
}
exports.getAsyncLocalStorage = getAsyncLocalStorage;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaW5kZXguanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi8uLi9zcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7O0FBQUEsNkNBQWdEO0FBRW5DLFFBQUEsS0FBSyxHQUFHLE1BQU0sQ0FBQyxHQUFHLENBQUMsd0JBQXdCLENBQUMsQ0FBQztBQUUxRCxTQUFnQixvQkFBb0I7SUFDbEMsTUFBTSxDQUFDLEdBQVEsVUFBVSxDQUFDO0lBQzFCLElBQUksQ0FBQyxDQUFDLENBQUMsYUFBSyxDQUFDLEVBQUUsQ0FBQztRQUNkLENBQUMsQ0FBQyxhQUFLLENBQUMsR0FBRyxJQUFJLCtCQUFpQixFQUFLLENBQUM7SUFDeEMsQ0FBQztJQUNELE9BQU8sQ0FBQyxDQUFDLGFBQUssQ0FBQyxDQUFDO0FBQ2xCLENBQUM7QUFORCxvREFNQyJ9