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


# Make sure the yay generated files are included in the bundle
from yay import lextab
from yay import parsetab


from yaybu.core.main import main

if __name__ == "__main__":
    main()
