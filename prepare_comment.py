import argparse
import os
import subprocess
from pathlib import Path

from tabulate import tabulate


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root_dir", type=str, required=True)
    parser.add_argument("--repo_id", type=str, required=True)
    return parser.parse_args(args)


def get_branch(root):
    with open(os.devnull, "wb") as null_stream:
        result = subprocess.check_output(
            f"cd {root} && git rev-parse --abbrev-ref HEAD",
            shell=True,
            stdin=null_stream,
            stderr=null_stream,
        )
    result = result.decode('utf-8')
    result = result.strip()
    return result

def main(root_dir: str, repo_id: str):
    root_dir = Path(root_dir)
    if not root_dir.exists():
        raise ValueError(f"root_dir {root_dir} does not exist")

    branch = get_branch(root_dir)

    notebook_paths = sorted(root_dir.glob("**/*.ipynb"))

    table_data = []
    for notebook_path in notebook_paths:
        relpath = notebook_path.relative_to(root_dir)
        gh_link = f"https://github.com/{repo_id}/blob/{branch}/{relpath}"
        gh_link_md = f"[{relpath}]({gh_link})"
        colab_link = f"https://colab.research.google.com/github/{repo_id}/blob/{branch}/{relpath}"
        colab_badge_md = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_link})"
        row = [gh_link_md, colab_badge_md]
        table_data.append(row)

    md_table = tabulate(table_data, headers=["Notebook", "Colab"], tablefmt="github")
    comment = f"Here are links to notebooks available in this branch:\n\n{md_table}"
    Path('comment.txt').write_text(comment)

if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))
