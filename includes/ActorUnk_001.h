#pragma once
#include "ActorUnk_002.h"
class ActorUnk_001 {
public:
    /* vtable 0x0 */
    /* 0x08 */ ActorUnk_002* Actor_002;
    /* 0x10 */ ulong mUnk_10;
    /* 0x18 */ ulong mUnk_18;
    /* 0x20 */ u32 mUnk_20;
    /* 0x24 */ u32 mUnk_24;

    ActorUnk_001(long, ActorUnk_002*, int, int);
    virtual ~ActorUnk_001();
    
    virtual bool vfunc_10();
    virtual void vfunc_18();
    virtual void vfunc_20();
    virtual long vfunc_28();
    virtual long vfunc_30();
    virtual long vfunc_38();
    virtual void vfunc_40(unsigned long param_2);
};  // SIZE 0x28