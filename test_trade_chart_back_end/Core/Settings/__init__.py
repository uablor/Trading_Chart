from dotenv import load_dotenv

import os


load_dotenv()

GJANGO_ENV = os.getenv("GJANGO_ENV", "dev")

if GJANGO_ENV == "prod":
    from .prod import *
else:
    from .dev import *
