# ===
# This is the main GYP file, which builds better-sqlite3 with SQLite3 itself.
# ===

{
  'includes': ['deps/common.gypi'],
  'targets': [
    {
      'target_name': 'better_sqlite3',
      'dependencies': ['deps/sqlite3.gyp:sqlite3'],
      'sources': ['src/better_sqlite3.cpp'],
      'include_dirs': [
        '<(module_root_dir)/deps/binn/src',
        '<(module_root_dir)/deps/secp256k1-vrf/include'
      ],
      'libraries': [
        '<(module_root_dir)/deps/binn/libbinn.a',
        '<(module_root_dir)/deps/secp256k1-vrf/.libs/libsecp256k1-vrf.a'
      ],
      'cflags': ['-std=c++14'],
      'xcode_settings': {
        'OTHER_CPLUSPLUSFLAGS': ['-std=c++14', '-stdlib=libc++'],
      },
      'conditions': [
        ['OS == "win"', {
          'libraries': ['ws2_32.lib']
        }]
      ]
    },
    {
      'target_name': 'test_extension',
      'dependencies': ['deps/sqlite3.gyp:sqlite3'],
      'include_dirs': [
        '<(module_root_dir)/deps/binn/src'
      ],
      'conditions': [['sqlite3 == ""', { 'sources': ['deps/test_extension.c'] }]],
    },
  ],
}
