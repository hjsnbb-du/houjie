interface Options {
    baseDir: string;
    framework?: string;
}
/**
 * Find the framework directory, lookup order
 * - specify framework path
 * - get framework name from
 * - use egg by default
 * @param {Object} options - options
 * @param  {String} options.baseDir - the current directory of application
 * @param  {String} [options.framework] - the directory of framework
 * @return {String} frameworkPath
 */
export declare function getFrameworkPath(options: Options): string;
export {};
