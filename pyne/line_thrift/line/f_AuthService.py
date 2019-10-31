#
# Autogenerated by Frugal Compiler (3.4.9)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#



import asyncio
from datetime import timedelta
import inspect

from frugal.aio.processor import FBaseProcessor
from frugal.aio.processor import FProcessorFunction
from frugal.exceptions import TApplicationExceptionType
from frugal.exceptions import TTransportExceptionType
from frugal.middleware import Method
from frugal.transport import TMemoryOutputBuffer
from frugal.util.deprecate import deprecated
from thrift.Thrift import TApplicationException
from thrift.Thrift import TMessageType
from thrift.transport.TTransport import TTransportException
from .ttypes import *


class Iface(object):

    async def loginZ(self, ctx, loginRequest):
        """
        Args:
            ctx: FContext
            loginRequest: LoginRequest
        """
        pass


class Client(Iface):

    def __init__(self, provider, middleware=None):
        """
        Create a new Client with an FServiceProvider containing a transport
        and protocol factory.

        Args:
            provider: FServiceProvider
            middleware: ServiceMiddleware or list of ServiceMiddleware
        """
        middleware = middleware or []
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]
        self._transport = provider.get_transport()
        self._protocol_factory = provider.get_protocol_factory()
        middleware += provider.get_middleware()
        self._methods = {
            'loginZ': Method(self._loginZ, middleware),
        }

    async def loginZ(self, ctx, loginRequest):
        """
        Args:
            ctx: FContext
            loginRequest: LoginRequest
        """
        return await self._methods['loginZ']([ctx, loginRequest])

    async def _loginZ(self, ctx, loginRequest):
        memory_buffer = TMemoryOutputBuffer(self._transport.get_request_size_limit())
        oprot = self._protocol_factory.get_protocol(memory_buffer)
        oprot.write_request_headers(ctx)
        oprot.writeMessageBegin('loginZ', TMessageType.CALL, 0)
        args = loginZ_args()
        args.loginRequest = loginRequest
        args.write(oprot)
        oprot.writeMessageEnd()
        response_transport = await self._transport.request(ctx, memory_buffer.getvalue())

        iprot = self._protocol_factory.get_protocol(response_transport)
        iprot.read_response_headers(ctx)
        _, mtype, _ = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            if x.type == TApplicationExceptionType.RESPONSE_TOO_LARGE:
                raise TTransportException(type=TTransportExceptionType.RESPONSE_TOO_LARGE, message=x.message)
            raise x
        result = loginZ_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        if result.success is not None:
            return result.success
        raise TApplicationException(TApplicationExceptionType.MISSING_RESULT, "loginZ failed: unknown result")


class Processor(FBaseProcessor):

    def __init__(self, handler, middleware=None):
        """
        Create a new Processor.

        Args:
            handler: Iface
        """
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]

        super(Processor, self).__init__()
        self.add_to_processor_map('loginZ', _loginZ(Method(handler.loginZ, middleware), self.get_write_lock()))


class _loginZ(FProcessorFunction):

    def __init__(self, handler, lock):
        super(_loginZ, self).__init__(handler, lock)

    async def process(self, ctx, iprot, oprot):
        args = loginZ_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = loginZ_result()
        try:
            ret = self._handler([ctx, args.loginRequest])
            if inspect.iscoroutine(ret):
                ret = await ret
            result.success = ret
        except TApplicationException as ex:
            async with self._lock:
                _write_application_exception(ctx, oprot, "loginZ", exception=ex)
                return
        except AuthException as e:
            result.e = e
        except Exception as e:
            async with self._lock:
                _write_application_exception(ctx, oprot, "loginZ", ex_code=TApplicationExceptionType.INTERNAL_ERROR, message=str(e))
            raise
        async with self._lock:
            try:
                oprot.write_response_headers(ctx)
                oprot.writeMessageBegin('loginZ', TMessageType.REPLY, 0)
                result.write(oprot)
                oprot.writeMessageEnd()
                oprot.get_transport().flush()
            except TTransportException as e:
                # catch a request too large error because the TMemoryOutputBuffer always throws that if too much data is written
                if e.type == TTransportExceptionType.REQUEST_TOO_LARGE:
                    raise _write_application_exception(ctx, oprot, "loginZ", ex_code=TApplicationExceptionType.RESPONSE_TOO_LARGE, message=e.message)
                else:
                    raise e


def _write_application_exception(ctx, oprot, method, ex_code=None, message=None, exception=None):
    if exception is not None:
        x = exception
    else:
        x = TApplicationException(type=ex_code, message=message)
    oprot.write_response_headers(ctx)
    oprot.writeMessageBegin(method, TMessageType.EXCEPTION, 0)
    x.write(oprot)
    oprot.writeMessageEnd()
    oprot.get_transport().flush()
    return x

class loginZ_args(object):
    """
    Attributes:
     - loginRequest
    """
    def __init__(self, loginRequest=None):
        self.loginRequest = loginRequest

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 2:
                if ftype == TType.STRUCT:
                    self.loginRequest = LoginRequest()
                    self.loginRequest.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('loginZ_args')
        if self.loginRequest is not None:
            oprot.writeFieldBegin('loginRequest', TType.STRUCT, 2)
            self.loginRequest.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.loginRequest))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class loginZ_result(object):
    """
    Attributes:
     - success
     - e
    """
    def __init__(self, success=None, e=None):
        self.success = success
        self.e = e

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = LoginResult()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.e = AuthException()
                    self.e.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('loginZ_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.e is not None:
            oprot.writeFieldBegin('e', TType.STRUCT, 1)
            self.e.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(make_hashable(self.success))
        value = (value * 31) ^ hash(make_hashable(self.e))
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

