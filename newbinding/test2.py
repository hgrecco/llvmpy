import api
import extra
import _capsule
from StringIO import StringIO
api.capsule.set_debug(True)


api.InitializeNativeTarget()
context = api.getGlobalContext()


m = api.Module.new("modname", context)
print m.getModuleIdentifier()
m.setModuleIdentifier('modname2')
print m.getModuleIdentifier()
print 'endianness', m.getEndianness()
assert m.getEndianness() == api.Module.Endianness.AnyEndianness
print 'pointer-size', m.getPointerSize()
assert m.getPointerSize() == api.Module.PointerSize.AnyPointerSize
m.dump()


os = extra.make_raw_ostream_for_printing()
m.print_(os, None)
print os.str()


int1ty = api.Type.getInt1Ty(context)
int1ty.dump()

print int1ty.isIntegerTy(1)

fnty = api.FunctionType.get(int1ty, False)
fnty.dump()

types = [int1ty, api.Type.getIntNTy(context, 21)]
fnty = api.FunctionType.get(int1ty, types, False)

print fnty

const = m.getOrInsertFunction("foo", fnty)
fn = extra.downcast(const, api.Function)
print fn
assert fn.hasName()
assert 'foo' == fn.getName()
fn.setName('bar')
assert 'bar' == fn.getName()

assert fn.getReturnType() is int1ty

assert fnty is fn.getFunctionType()

assert fn.isVarArg() == False
assert fn.getIntrinsicID() == 0
assert not fn.isIntrinsic()

fn_uselist = fn.list_use()
assert isinstance(fn_uselist, list)
assert len(fn_uselist) == 0

builder = api.IRBuilder.new(context)
print builder

bb = api.BasicBlock.Create(context, "entry", fn, None)
assert bb.empty()
builder.SetInsertPoint(bb)

assert bb.getTerminator() is None

arg0, arg1 = fn.getArgumentList()
print arg0, arg1

ret = builder.CreateCall(fn, [arg0, arg1], '')
builder.CreateRet(ret)

print fn

errio = StringIO()
ee = api.ExecutionEngine.createJIT(m)
print ee, errio.getvalue()
print ee.getDataLayout().getStringRepresentation()

datalayout_str = 'e-p:64:64:64-S128-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:64:64-f16:16:16-f32:32:32-f64:64:64-f128:128:128-v64:64:64-v128:128:128-a0:0:64-s0:64:64-f80:128:128-n8:16:32:64'

assert datalayout_str == str(api.DataLayout.new(datalayout_str))
assert datalayout_str == str(api.DataLayout.new(str(api.DataLayout.new(datalayout_str))))

