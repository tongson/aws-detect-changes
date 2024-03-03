#!/usr/bin/env python3
import json
import os
import subprocess
from typing import Dict, TextIO, List, Any

JsonDict = Dict[str, Any]

def git_init(cwd: str) -> None:
    name = "AWS resource modification detection"
    email = "aws@example.com"
    try:
        subprocess.run(["git", "init"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd, check=True)
        subprocess.run(["git", "config", "user.email", email], cwd=cwd, check=True)
        subprocess.run(["git", "config", "user.name", name], cwd=cwd, check=True)
        subprocess.run(["git", "add", "."], cwd=cwd, check=True)
    except Exception as e:
        e.add_note("\nError initializing Git directory")
        raise

def git_status(cwd: str) -> str:
    try:
        changes = subprocess.run(["git", "status", "--short", "--porcelain=1"], cwd=cwd, text=True, check=True, capture_output=True)
    except Exception as e:
        e.add_note("\nError getting changes")
        raise
    else:
        return changes.stdout

def git_commit(cwd: str, msg: str) -> None:
    try:
        subprocess.run(["git", "add", "."], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd, check=True)
        subprocess.run(["git", "commit", "-a", "-m", msg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd, check=True)
    except Exception as e:
        e.add_note("\nError committing changes")
        raise

def json_load(results: TextIO) -> tuple[str, JsonDict]:
    try:
        data: JsonDict = json.load(results)
    except Exception as e:
        e.add_note("\nError loading JSON")
        raise
    else:
        account: str = data["_metadata"]["account_id"]
        return account, data

def process(account: str, data: JsonDict) -> None:
    git = account
    if not os.path.exists(git):
        try:
            os.makedirs(git, mode=0o700, exist_ok=False)
        except Exception as e:
            e.add_note("\nError creating git directory")
            raise
        else:
            git_init(git)
    

    region: str
    resource: JsonDict
    for region, resource in data["regions"].items():
        try:
            os.makedirs(f"{git}/{region}", mode=0o700, exist_ok=True)
        except Exception as e:
            e.add_note("\nError creating directories")
            raise
        else:
            res: str
            arr: List[str]
            for res, arr in resource.items():
                if  ("EC2"          in res) or \
                    ("EKS"          in res) or \
                    ("IAM"          in res) or \
                    ("S3"           in res) or \
                    ("LoadBalancer" in res):
                        i: str
                        for i in arr:
                            try:
                                write_file = open(f"{git}/{region}/{res}", "w")
                            except Exception as e:
                                e.add_note("\nError opening file for writing")
                                raise
                            else:
                                print(f"{i}", file=write_file)
                            finally:
                                write_file.close()
            output = git_status(git)
            if not len(output) == 0:
                for line in output.splitlines():
                    print(f"[{account}] {line}")
                git_commit(git, output.replace('\n', ';'))
            else:
                print(f"[{account}] No modifications to {region}")
     
def main() -> None:
    try:
        result: TextIO = open("result.json")
    except Exception as e:
        e.add_note("\nError opening JSON file")
        raise
    else:
        account: str
        results: JsonDict
        account, results = json_load(result)
        print(f"[{account}] Loaded results")
        process(account, results)
        print(f"[{account}] Processed results")
    finally:
        result.close()

if __name__ == "__main__":
    main()
