import type { ILogger } from './ILogger.js';
declare global {
    var __ONE_LOGGER_INSTANCES__: Map<string, ILogger>;
}
export interface LoggerOptions {
    loggerName: string;
    prefix?: string;
}
export declare class Logger implements ILogger {
    #private;
    constructor(options: LoggerOptions);
    info(message?: any, ...optionalParams: any[]): void;
    warn(message?: any, ...optionalParams: any[]): void;
    error(message?: any, ...optionalParams: any[]): void;
    protected _getRealLogger(): ILogger;
    static setRealLogger(loggerName: string, realLogger: ILogger | undefined): void;
}
