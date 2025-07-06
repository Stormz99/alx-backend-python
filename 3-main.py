import sys
lazy_paginate = __import__('2-lazy_paginate').lazy_pagination

try:
    for page in lazy_paginate(50):
        for user in page:
            print(user)
except BrokenPipeError:
    sys.stderr.close()