/* Link shim for building the runtime with an msvcrt MinGW (MSYS2 mingw64) against the UCRT-built libvpx.a:
   libvpx's setjmp is __intrinsic_setjmp[ex]; a tail jump keeps setjmp returning into the caller's frame */
__asm__(".globl __intrinsic_setjmp\n__intrinsic_setjmp:\n\tjmp _setjmp\n"
        ".globl __intrinsic_setjmpex\n__intrinsic_setjmpex:\n\tjmp _setjmp\n");
