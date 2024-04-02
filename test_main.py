from importlib import reload
import sys
import unittest

import main


# limit number of retries
MAX_RETRIES = 5
retries = 0


def autograding_successfully_imported():
    """Check if autograding module is successfully imported.

    If a submodule is imported (e.g. autograding.case), autograding may be imported
    as a namespace module.
    Namespace modules have __file__ attribute set tot None, so we can use that to check
    if autograding was imported as a module and not just a namespace module.
    """
    return (
        "autograding" in locals()
        and locals().get("autograding").__file__
    )

# autograding submodule might not be successfully fetched on init
# if unsuccessful, we have to fetch it manually
while not autograding_successfully_imported():
    try:
        import autograding
        reload(autograding)
        from autograding.case import FuncCall, InOut, RecursiveCall
    except (ImportError, ModuleNotFoundError):
        import subprocess
        subprocess.run(["git", "submodule", "update", "--init"])
        retries += 1
    else:
        break
    if retries >= MAX_RETRIES:
        sys.exit("[import autograding] Too many retries, exiting")


class TestMyRecursive(autograding.TestRecursive):
    def setUp(self):
        self.testcases = [
            RecursiveCall(module=main,
                          func=main.reverse,
                          args=("",),
                          ans="",
                          output="",
                          basecase=True),
            RecursiveCall(module=main,
                          func=main.reverse,
                          args=("1",),
                          ans="1",
                          output="",
                          basecase=True),
            RecursiveCall(module=main,
                          func=main.reverse,
                          args=("12345",),
                          ans="54321",
                          output="",
                          basecase=False),
            RecursiveCall(module=main,
                          func=main.is_palindrome,
                          args=("",),
                          ans=True,
                          output="",
                          basecase=True),
            RecursiveCall(module=main,
                          func=main.is_palindrome,
                          args=("a",),
                          ans=True,
                          output="",
                          basecase=True),
            RecursiveCall(module=main,
                          func=main.is_palindrome,
                          args=("racecar",),
                          ans=True,
                          output="",
                          basecase=False),
            RecursiveCall(module=main,
                          func=main.is_palindrome,
                          args=("aloe vera",),
                          ans=False,
                          output="",
                          basecase=False),
    ]


if __name__ == '__main__':
    unittest.main()
