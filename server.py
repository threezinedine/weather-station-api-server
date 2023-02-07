import argparse
import subprocess
from dotenv import load_dotenv


parser = argparse.ArgumentParser()
parser.add_argument("action", choices=[
                    "run", "unit", "e2e", "all"], help="The action to do")
args = parser.parse_args()


def main():
    """
    The function which determine the server mode.
    The action is determined by the argument.
    If the argument is "run", run the file main.py
    If the argument is "unit", run th file test_unittest.py
    If the argument is "e2e", run the file test_e2e.py
    If the argument is "all", the file test.py
    """
    if args.action == "run":
        subprocess.run(["venv\Scripts\python.exe", "main.py"])
    elif args.action == "unit":
        subprocess.run(["venv\Scripts\pytest.exe", "test_unittest.py"])
    elif args.action == "e2e":
        subprocess.run(["venv\Scripts\pytest.exe", "test_e2e.py"])
    else:
        subprocess.run(["venv\Scripts\pytest.exe", "test.py"])


if __name__ == "__main__":
    load_dotenv()
    main()
