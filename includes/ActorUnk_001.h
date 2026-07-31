#pragma once
#include "ActorUnk_002.h"
class ActorUnk_001 {
public:
    /* vtable 0x0 */
    /* 0x08 */ ActorUnk_002* Actor_002;
    /* 0x10 */ long mUnk_10;
    /* 0x18 */ long mUnk_18;
    /* 0x20 */ int mUnk_20;
    /* 0x24 */ int mUnk_24;

    ActorUnk_001(long param_2, ActorUnk_002* param_3, int param_4, int param_5);
    ActorUnk_001();
    ~ActorUnk_001();
    
    virtual bool vfunc_00();
    virtual void vfunc_08();
    virtual void vfunc_10();
    virtual long vfunc_18();
    virtual long vfunc_20();
    virtual long vfunc_28();
    virtual void vfunc_30(unsigned long param_2);
};  // SIZE 0x28