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
