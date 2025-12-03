import pytest
import sys

print("Running ALL tests...")
if __name__ == "__main__":
    retcode = pytest.main(["-v", "--tb=short"])
    print(f"\nFinished with return code: {retcode}")
    sys.exit(retcode)
