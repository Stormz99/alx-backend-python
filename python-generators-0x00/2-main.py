import sys
import batch_processing

try:
    batch_processing.batch_processing(50)
except BrokenPipeError:
    sys.stderr.close()
