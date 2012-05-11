import signal
import sys
import time
from subprocess import Popen

from sleep import sleep


sleep.flush_queue()
worker_command = [sys.executable, '-m', 'thoonktasks.worker', 'examples.sleep']

# Send task once
sleep(3)

# Start worker
worker = Popen(worker_command)
time.sleep(2)

# Stop worker before task finished
worker.send_signal(signal.SIGINT)

# Wait for worker to exit
worker.wait()

# Start a new worker
worker = Popen(worker_command)

# Task is still in queue
time.sleep(4)

# Stop worker
worker.send_signal(signal.SIGINT)
worker.wait()
