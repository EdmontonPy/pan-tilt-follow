#!/usr/bin/env python
import atexit

from ptf import PTF


def quit_gracefully():
    ptf.shutdown()

ptf = PTF()
atexit.register(quit_gracefully)

if __name__ == '__main__':
    ptf.run()
