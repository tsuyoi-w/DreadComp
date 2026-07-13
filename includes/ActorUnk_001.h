#pragma once
class ActorUnk_002 {
public:
    virtual void vfunc00(int);
    virtual void vfunc08(int);
    virtual void vfunc10(int);
    virtual void vfunc18(int);
    virtual void vfunc20(int);
    virtual void vfunc28(int);
    virtual void vfunc30(int);
    virtual void vfunc38(int);
    virtual void* vfunc40(unsigned long, int, int);
    virtual void vfunc48(long);
};
class ActorUnk_001 {
public:
    /* vtable 0x0 */
    /* 0x08 */ ActorUnk_002* Actor_002;
    /* 0x10 */ long mUnk_10;
    /* 0x18 */ long mUnk_18;
    /* 0x20 */ int mUnk_20;
    /* 0x24 */ int mUnk_24;

    ActorUnk_001(long param_2, ActorUnk_002* param_3, int param_4,
                 int param_5);
    ActorUnk_001();
    ~ActorUnk_001();
    virtual void vfunc_08();
    virtual void vfunc_30(unsigned long param_2);
    virtual bool vfunc_00();
    virtual void vfunc_10();
    virtual void vfunc_18();
    virtual void vfunc_20();
    virtual void vfunc_28();
}; // SIZE 0x28