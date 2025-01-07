/**
 * Try to get framework dir path
 * If can't find any framework, try to find egg dir path
 *
 * @param {String} cwd - current work path
 * @param {Array} [eggNames] - egg names, default is ['egg']
 * @return {String} framework or egg dir path
 * @deprecated
 */
export declare function getFrameworkOrEggPath(cwd: string, eggNames?: string[]): string;
