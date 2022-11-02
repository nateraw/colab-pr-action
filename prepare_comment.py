import argparse
from pathlib import Path

from tabulate import tabulate


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root_dir", type=str, required=True)
    parser.add_argument("--repo_id", type=str, required=True)
    parser.add_argument("--branch", type=str, required=True)
    return parser.parse_args(args)


def main(root_dir: str, repo_id: str, branch: str):
    root_dir = Path(root_dir)
    if not root_dir.exists():
        raise ValueError(f"root_dir {root_dir} does not exist")

    notebook_paths = sorted(root_dir.glob("**/*.ipynb"))
    
    table_data = []
    for notebook_path in notebook_paths:
        row = [notebook_path, f"https://github.com/{repo_id}/blob/{branch}/{notebook_path.relative_to(root_dir)}"]
        table_data.append(row)
    
    return tabulate(table_data, headers=["Notebook", "Link"], tablefmt="github")

if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))
