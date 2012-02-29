import sys

from hello import hello


hello()

for arg in sys.argv[1:]:
    hello(arg)
