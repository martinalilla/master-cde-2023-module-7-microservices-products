# extract-openapi.py
import os
if os.environ.get("ENVIRONMENT") == 'local':
    from dotenv import load_dotenv
    dotenv_path = './.env.development'
    load_dotenv(dotenv_path)
    


import argparse
import json
import sys
import yaml
from app.main import app


parser = argparse.ArgumentParser(prog="extract-openapi.py")
parser.add_argument("--app",       help='App import string. Eg. "main:app"', default="main:app")
parser.add_argument("--app-dir", help="Directory containing the app", default="app")
parser.add_argument("--out",     help="Output file ending in .json or .yaml", default="openapi.yaml")

if __name__ == "__main__":
    args = parser.parse_args()

    if args.app_dir is not None:
        sys.path.insert(0, args.app_dir)

    openapi = app.openapi()
    version = openapi.get("openapi", "unknown version")

    #print(f"writing openapi spec v{version}")
    with open(args.out, "w") as f:
        if args.out.endswith(".json"):
            json.dump(openapi, f, indent=2)
        else:
            yaml.safe_dump(openapi, f, sort_keys=False)
