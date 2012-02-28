from hello import hello
import sys

hello()

for arg in sys.argv[1:]:
    hello(arg)
