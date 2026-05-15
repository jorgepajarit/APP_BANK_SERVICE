# conftest.py -- BankService pytest configuration
# Adds the fastapi_app root to sys.path so that domain.*, application.*
# and adapters.* can be imported cleanly in all test files.

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
