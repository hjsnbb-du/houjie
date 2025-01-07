# gals

[![NPM version][npm-image]][npm-url]
[![Node.js CI](https://github.com/node-modules/gals/actions/workflows/nodejs.yml/badge.svg)](https://github.com/node-modules/gals/actions/workflows/nodejs.yml)
[![Test coverage][codecov-image]][codecov-url]
[![npm download][download-image]][download-url]

[npm-image]: https://img.shields.io/npm/v/gals.svg?style=flat-square
[npm-url]: https://npmjs.org/package/gals
[codecov-image]: https://codecov.io/github/node-modules/gals/coverage.svg?branch=master
[codecov-url]: https://codecov.io/github/node-modules/gals?branch=master
[download-image]: https://img.shields.io/npm/dm/gals.svg?style=flat-square
[download-url]: https://npmjs.org/package/gals

global AsyncLocalStorage

## Install

```bash
npm install gals
```

## Usage

```ts
import { getAsyncLocalStorage } from 'gals';

const asyncLocalStorage = getAsyncLocalStorage();
const store = asyncLocalStorage.getStore();
```

## License

[MIT](LICENSE.txt)

<!-- GITCONTRIBUTOR_START -->

## Contributors

|[<img src="https://avatars.githubusercontent.com/u/156269?v=4" width="100px;"/><br/><sub><b>fengmk2</b></sub>](https://github.com/fengmk2)<br/>|
| :---: |


This project follows the git-contributor [spec](https://github.com/xudafeng/git-contributor), auto updated at `Wed Dec 20 2023 00:17:19 GMT+0800`.

<!-- GITCONTRIBUTOR_END -->
