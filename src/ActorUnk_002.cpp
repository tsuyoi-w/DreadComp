#include "ActorUnk_002.h"
#include "nn/os/os_Mutex.h"

extern int FUN_71000668f8(nn::os::MutexType *p1) {
  nn::os::InitializeMutex(p1, true, 0);
  return 1;
}

ActorUnk_002::ActorUnk_002() : mUnk_30(0xffffffff) {
  FUN_71000668f8(&this->mUnk_38);
  this->mUnk_08 = &this->mUnk_58;
  this->mUnk_10 = &this->mUnk_90;
  this->mUnk_30 = 2;
  this->mUnk_18 = &this->mUnk_c8;
  this->mUnk_20 = &this->mUnk_100;
}

ActorUnk_002::~ActorUnk_002() {
  nn::os::FinalizeMutex(&this->mUnk_38);
  operator delete(this);
}

int ActorUnk_002::vfunc_58() { return 0; }