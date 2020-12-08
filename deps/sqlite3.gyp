# ===
# This configuration defines options specific to compiling SQLite3 itself.
# Compile-time options are loaded by the auto-generated file "defines.gypi".
# Before SQLite3 is compiled, it gets extracted from "sqlite3.tar.gz".
# The --sqlite3 option can be provided to use a custom amalgamation instead.
# ===

{
  'includes': ['common.gypi'],
  'targets': [
    {
      'target_name': 'clone_repos',
      'type': 'none',
      'hard_dependency': 1,
      'actions': [{
        'action_name': 'clone_repos',
        'inputs': [],
        'outputs': [
          '<(module_root_dir)/deps/aergolite',
          '<(module_root_dir)/deps/binn',
          '<(module_root_dir)/deps/secp256k1-vrf'
        ],
        'action': ['node', 'clone.js', '<(module_root_dir)/deps'],
      }]
    },

    {
      'target_name': 'locate_sqlite3',
      'type': 'none',
      'hard_dependency': 1,
      'dependencies': ['clone_repos'],
      'conditions': [
        ['sqlite3 == ""', {
          'actions': [{
            'action_name': 'symlink_aergolite',
            'inputs': [],
            'outputs': [
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/sqlite3.c',
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/sqlite3.h',
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/sqlite3ext.h',
            ],
            'action': ['node', 'symlink.js', '<(SHARED_INTERMEDIATE_DIR)/sqlite3', '<(module_root_dir)/deps/aergolite/amalgamation'],
          }],
        }, {
          'actions': [{
            'action_name': 'symlink_sqlite3',
            'inputs': [],
            'outputs': [
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/sqlite3.c',
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/sqlite3.h',
            ],
            'action': ['node', 'symlink.js', '<(SHARED_INTERMEDIATE_DIR)/sqlite3', '<(sqlite3)'],
          }],
        }],
      ],
    },

    {
      'target_name': 'binn',
      'type': 'none',
      'hard_dependency': 1,
      'dependencies': ['clone_repos'],
      'conditions': [
        ['OS == "win"', {

          'copies': [{
            'files': ['<(module_root_dir)/deps/static_libs/binn/<(OS)_<(target_arch)/libbinn.a'],
            'destination': '<(module_root_dir)/deps/binn/',
          }]

        },{

          'actions': [{
            'action_name': 'build_binn_library',
            'inputs': ['<(module_root_dir)/deps/binn'],
            'outputs': ['<(module_root_dir)/deps/binn/libbinn.a'],
            'action': [ 'make', '-C', '<(module_root_dir)/deps/binn', 'static', 'CFLAGS=-fPIC' ]
          }]

        }],
      ],
    },

    {
      'target_name': 'secp256k1-vrf',
      'type': 'none',
      'hard_dependency': 1,
      'dependencies': ['clone_repos'],
      'conditions': [
        ['OS == "win"', {

          'copies': [{
            'files': ['<(module_root_dir)/deps/static_libs/secp256k1-vrf/<(OS)_<(target_arch)/libsecp256k1-vrf.a'],
            'destination': '<(module_root_dir)/deps/secp256k1-vrf/.libs/',
          }]

        },{

          'actions': [{
            'action_name': 'build_secp256k1_step1',
            'inputs': ['<(module_root_dir)/deps/secp256k1-vrf/autogen.sh'],
            'outputs': ['<(module_root_dir)/deps/secp256k1-vrf/configure'],
            'action': [ 'eval', 'cd <(module_root_dir)/deps/secp256k1-vrf && ./autogen.sh' ]
          },{
            'action_name': 'build_secp256k1_step2',
            'inputs': ['<(module_root_dir)/deps/secp256k1-vrf/configure'],
            'outputs': ['<(module_root_dir)/deps/secp256k1-vrf/makefile'],
            'action': [ 'eval', 'cd <(module_root_dir)/deps/secp256k1-vrf && ./configure --with-bignum=no --disable-benchmark' ]
          },{
            'action_name': 'build_secp256k1_step3',
            'inputs': ['<(module_root_dir)/deps/secp256k1-vrf'],
            'outputs': ['<(module_root_dir)/deps/secp256k1-vrf/.libs/libsecp256k1-vrf.a'],
            'action': [ 'make', '-C', '<(module_root_dir)/deps/secp256k1-vrf', 'CFLAGS=-fPIC' ]
          }]

        }],
      ],
    },

    {
      'target_name': 'sqlite3',
      'type': 'static_library',
      'dependencies': ['locate_sqlite3', 'binn', 'secp256k1-vrf'],
      'sources': ['<(SHARED_INTERMEDIATE_DIR)/sqlite3/sqlite3.c'],
      'include_dirs': [
        '<(SHARED_INTERMEDIATE_DIR)/sqlite3/',
        '<(module_root_dir)/deps/binn/src',
        '<(module_root_dir)/deps/secp256k1-vrf/include'
      ],
      'direct_dependent_settings': {
        'include_dirs': ['<(SHARED_INTERMEDIATE_DIR)/sqlite3/'],
      },
      'cflags': ['-std=c99', '-w'],
      'xcode_settings': {
        'OTHER_CFLAGS': ['-std=c99'],
        'WARNING_CFLAGS': ['-w'],
      },
      'conditions': [
        ['sqlite3 == ""', {
          'includes': ['defines.gypi'],
        }, {
          'defines': [
            # This is currently required by better-sqlite3.
            'SQLITE_ENABLE_COLUMN_METADATA',
          ],
        }]
      ],
      'configurations': {
        'Debug': {
          'msvs_settings': { 'VCCLCompilerTool': { 'RuntimeLibrary': 1 } }, # static debug
        },
        'Release': {
          'msvs_settings': { 'VCCLCompilerTool': { 'RuntimeLibrary': 0 } }, # static release
        },
      },
    },
  ],
}
