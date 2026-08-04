#pragma once

#include "ActorUnk_010.h"
#include "nn/os.h"

class ActorUnk_002 {
public:
  /* vtable 0x0 */
  /* 0x08 */ ActorUnk_010 *mUnk_08;
  /* 0x10 */ ActorUnk_010 *mUnk_10;
  /* 0x18 */ ActorUnk_010 *mUnk_18;
  /* 0x20 */ ActorUnk_010 *mUnk_20;
  /* 0x28 */ ulong mUnk_28;
  /* 0x30*/ ulong mUnk_30;
  /* 0x38 */ nn::os::MutexType mUnk_38;
  /* 0x58 */ ActorUnk_010 mUnk_58;
  /* 0x90 */ ActorUnk_010 mUnk_90;
  /* 0xc8 */ ActorUnk_010 mUnk_c8;
  /* 0x100 */ ActorUnk_010 mUnk_100;

  ActorUnk_002();
  virtual ~ActorUnk_002();

  virtual void vfunc_10(long);
  virtual void vfunc_18();
  virtual void vfunc_20(int);
  virtual void vfunc_28(int);
  virtual void vfunc_30(int);
  virtual void vfunc_38(long);
  virtual void *vfunc_40(unsigned long, int, int);
  virtual void vfunc_48(int);
  virtual void *vfunc_50(unsigned long, int, int);
  virtual int vfunc_58();
}; // SIZE

