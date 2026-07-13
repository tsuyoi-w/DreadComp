#include "ActorUnk_001.h"
#include "sched.h"

ActorUnk_001::ActorUnk_001() {}
ActorUnk_001::ActorUnk_001(long param_1, ActorUnk_002* param_2, int param_3, int param_4) {}
ActorUnk_001::~ActorUnk_001() {}
void ActorUnk_001::vfunc_08() {
    Actor_002->vfunc48(this->mUnk_10);
    this->mUnk_10 = 0;
    this->mUnk_18 = 0;
}
void ActorUnk_001::vfunc_30(unsigned long param_1) {
    void* __dest = Actor_002->vfunc40(param_1, mUnk_20, mUnk_24);
    size_t __n = mUnk_18;
    if (param_1 <= mUnk_18) {
        __n = param_1;
    }
    memcpy(__dest, (void*)mUnk_10, __n);
    Actor_002->vfunc48(mUnk_10);
    mUnk_10 = (long)__dest;
    mUnk_18 = param_1;
}
bool ActorUnk_001::vfunc_00() {
    return mUnk_10 != 0;
}
void ActorUnk_001::vfunc_10() {
    *(int*)this = 3;
}
void ActorUnk_001::vfunc_18() {}
void ActorUnk_001::vfunc_20() {}
long ActorUnk_001::vfunc_28() {
    return this->mUnk_10;
}