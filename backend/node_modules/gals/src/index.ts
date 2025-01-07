import { AsyncLocalStorage } from 'async_hooks';

export const kGALS = Symbol.for('gals#asyncLocalStorage');

export function getAsyncLocalStorage<T = any>(): AsyncLocalStorage<T> {
  const g: any = globalThis;
  if (!g[kGALS]) {
    g[kGALS] = new AsyncLocalStorage<T>();
  }
  return g[kGALS];
}
