@echo on

mkdir binn
mkdir binn\win_x64
mkdir binn\win_ia32
mkdir secp256k1-vrf
mkdir secp256k1-vrf\win_x64
mkdir secp256k1-vrf\win_ia32

cd ..


git clone --depth=1 https://github.com/liteserver/binn
cd binn

call vcvars64
cl /c src\binn.c
lib binn.obj
copy /y binn.lib ..\static_libs\binn\win_x64\libbinn.a

call vcvars32
cl /c src\binn.c
lib binn.obj
copy /y binn.lib ..\static_libs\binn\win_ia32\libbinn.a

cd ..



git clone --depth=1 https://github.com/aergoio/secp256k1-vrf
cd secp256k1-vrf

cl -I. -DECMULT_GEN_PREC_BITS=4 src/gen_context.c
gen_context.exe

call vcvars64
cl /c -I. -DUSE_NUM_NONE=1 -DUSE_ECMULT_STATIC_PRECOMPUTATION=1 -DECMULT_GEN_PREC_BITS=4 -DUSE_FIELD_INV_BUILTIN=1 -DUSE_SCALAR_INV_BUILTIN=1 -DUSE_FIELD_10X26=1 -DUSE_SCALAR_8X32=1 -DECMULT_WINDOW_SIZE=15 src/secp256k1.c
lib secp256k1.obj
copy /y secp256k1.lib ..\static_libs\secp256k1-vrf\win_x64\libsecp256k1-vrf.a


call vcvars32
cl /c -I. -DUSE_NUM_NONE=1 -DUSE_ECMULT_STATIC_PRECOMPUTATION=1 -DECMULT_GEN_PREC_BITS=4 -DUSE_FIELD_INV_BUILTIN=1 -DUSE_SCALAR_INV_BUILTIN=1 -DUSE_FIELD_10X26=1 -DUSE_SCALAR_8X32=1 -DECMULT_WINDOW_SIZE=15 src/secp256k1.c
lib secp256k1.obj
copy /y secp256k1.lib ..\static_libs\secp256k1-vrf\win_ia32\libsecp256k1-vrf.a

cd ..
