/// <reference types="node" />
import { AsyncLocalStorage } from 'async_hooks';
export declare const kGALS: unique symbol;
export declare function getAsyncLocalStorage<T = any>(): AsyncLocalStorage<T>;
