import struct, socket, errno
from pyOSC3.OSC3 import OSCMessage, OSCStreamingClient as _OSCStreamingClient

class OSCStreamingClient(_OSCStreamingClient):

    def __init__(self):
        _OSCStreamingClient.__init__(self)

    def _receiveWithTimeout(self, count):
        # FIX: use bytes instead of str for python3 compatibility
        # see: https://github.com/Qirky/pyOSC3/issues/5
        chunk = bytes()
        while len(chunk) < count:
            try:
                tmp = self.socket.recv(count - len(chunk))
            except socket.timeout:
                if not self._running:
                    print("CLIENT: Socket timed out and termination requested.")
                    return None
                else:
                    continue
            except socket.error as e:
                if e[0] == errno.ECONNRESET:
                    print("CLIENT: Connection reset by peer.")
                    return None
                else:
                    raise e
            if not tmp or len(tmp) == 0:
                print("CLIENT: Socket has been closed.")
                return None
            chunk = chunk + tmp
        return chunk

    def _transmitMsgWithTimeout(self, msg):
        if not isinstance(msg, OSCMessage):
            raise TypeError("'msg' argument is not an OSCMessage or OSCBundle object")
        binary = msg.getBinary()
        length = len(binary)
        # FIX: prepend length of packet before the actual message (big endian)
        # see: https://github.com/Qirky/pyOSC3/issues/4
        len_big_endian = struct.pack('>L', length)
        if self._transmitWithTimeout(len_big_endian) and self._transmitWithTimeout(binary):
            return True
        else:
            return False