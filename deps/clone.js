'use strict';
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const dest = path.resolve(path.sep, process.argv[2]);

if (fs.existsSync(path.join(dest, 'binn/README.md'))) {
  console.log('the binn folder exists')
} else {
  execSync('git clone --depth=1 https://github.com/liteserver/binn ' + dest + '/binn', { stdio: 'inherit' });
}

if (fs.existsSync(path.join(dest, 'secp256k1-vrf/README.md'))) {
  console.log('the secp256k1-vrf folder exists')
} else {
  execSync('git clone --depth=1 https://github.com/aergoio/secp256k1-vrf ' + dest + '/secp256k1-vrf', { stdio: 'inherit' });
}

if (fs.existsSync(path.join(dest, 'aergolite/README.md'))) {
  console.log('the aergolite folder already exists')
} else {
  execSync('git clone --depth=1 https://github.com/aergoio/aergolite ' + dest + '/aergolite', { stdio: 'inherit' });
}

if (fs.existsSync(path.join(dest, 'aergolite/amalgamation/sqlite3.c'))) {
  console.log('the aergolite amalgamation folder already exists')
} else {
  execSync('cd ' + dest + '/aergolite && make amalgamation', { stdio: 'inherit' });
}
