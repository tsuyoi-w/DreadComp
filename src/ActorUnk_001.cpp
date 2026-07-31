#include "ActorUnk_001.h"
#include "sched.h"

extern ActorUnk_002* FUN_7100083990();

ActorUnk_001::ActorUnk_001() {
    if (this->mUnk_10 != 0) {
        Actor_002->vfunc_48(this->mUnk_10);
        this->mUnk_10 = 0;
        this->mUnk_18 = 0;
    }
}

ActorUnk_001::ActorUnk_001(long param_1, ActorUnk_002* param_2, int param_3, int param_4) {
    this->Actor_002 = param_2;
    this->mUnk_10 = 0;
    this->mUnk_18 = param_1;
    this->mUnk_20 = param_3;
    this->mUnk_20 = param_4;
    if (param_1 != 0) {
        if (param_2 == nullptr) {
            param_2 = FUN_7100083990();
            this->Actor_002 = param_2;
        }

        this->mUnk_10 = (long)param_2->vfunc_40(param_1, param_3, param_4);
    }
}

ActorUnk_001::~ActorUnk_001() {
    if (this->mUnk_10 != 0) {
        Actor_002->vfunc_48(this->mUnk_10);
    }
    operator delete(this);
}

bool ActorUnk_001::vfunc_00() {
    return mUnk_10 != 0;
}

void ActorUnk_001::vfunc_08() {
    Actor_002->vfunc_48(this->mUnk_10);
    this->mUnk_10 = 0;
    this->mUnk_18 = 0;
}

void ActorUnk_001::vfunc_10() {
    *(int*)this = 3;
}

long ActorUnk_001::vfunc_18() {
    return this->mUnk_10;
}

long ActorUnk_001::vfunc_20() {
    return this->mUnk_18;
}

long ActorUnk_001::vfunc_28() {
    return this->mUnk_10;
}

void ActorUnk_001::vfunc_30(unsigned long param_1) {
    void* _dest = Actor_002->vfunc_40(param_1, mUnk_20, mUnk_24);
    size_t __n = mUnk_18;
    if (param_1 <= mUnk_18) {
        __n = param_1;
    }
    memcpy(_dest, (void*)mUnk_10, __n);
    Actor_002->vfunc_48(mUnk_10);
    mUnk_10 = (long)_dest;
    mUnk_18 = param_1;
}