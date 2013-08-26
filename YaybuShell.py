import sys
import os

code_dir = os.path.dirname(sys.path[0])


# Make sure egg-info files are on the PYTHONPATH
sys.path.append(code_dir)


# Bundle a cacert.pem so HTTPS is secure
import libcloud.security
libcloud.security.CA_CERTS_PATH.append(
    os.path.join(code_dir, "cacert.pem")
    )


# Fix libcloud on windows
import socket
import ctypes

class sockaddr(ctypes.Structure):
    _fields_ = [("sa_family", ctypes.c_short),
                ("__pad1", ctypes.c_ushort),
                ("ipv4_addr", ctypes.c_byte * 4),
                ("ipv6_addr", ctypes.c_byte * 16),
                ("__pad2", ctypes.c_ulong)]

WSAStringToAddressA = ctypes.windll.ws2_32.WSAStringToAddressA
WSAAddressToStringA = ctypes.windll.ws2_32.WSAAddressToStringA

def inet_pton(address_family, ip_string):
    addr = sockaddr()
    addr.sa_family = address_family
    addr_size = ctypes.c_int(ctypes.sizeof(addr))

    if WSAStringToAddressA(ip_string, address_family, None, ctypes.byref(addr), ctypes.byref(addr_size)) != 0:
        raise socket.error(ctypes.FormatError())

    if address_family == socket.AF_INET:
        return ctypes.string_at(addr.ipv4_addr, 4)
    if address_family == socket.AF_INET6:
        return ctypes.string_at(addr.ipv6_addr, 16)

    raise socket.error('unknown address family')

setattr(socket, "inet_pton", inet_pton)


# Make sure the yay generated files are included in the bundle
from yay import lextab
from yay import parsetab


from yaybu.core.main import main

if __name__ == "__main__":
    main()
