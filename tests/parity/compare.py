"""Compare two rcv_cruncher batch output directories byte for byte.

Usage: python compare.py <dir_a> <dir_b>

Exits non-zero if any file differs or is missing on one side. Files whose content is
expected to vary between runs (timestamps) are ignored.
"""
import difflib
import pathlib
import sys

IGNORED = {
    pathlib.Path("results/inputs/pkg_info.txt"),  # start/end timestamps
    pathlib.Path("results/inputs/output_config.csv"),  # echoes the absolute cvr_path_root, which differs per environment
    pathlib.Path("run_config.json"),  # same: rewritten by run_batch.py with an absolute path
}


def listing(root: pathlib.Path):
    return {p.relative_to(root) for p in root.rglob("*") if p.is_file() and p.relative_to(root) not in IGNORED}


def main(a: str, b: str) -> int:
    root_a, root_b = pathlib.Path(a), pathlib.Path(b)
    files_a, files_b = listing(root_a), listing(root_b)
    problems = 0

    for missing in sorted(files_a - files_b):
        print(f"MISSING in {b}: {missing}")
        problems += 1
    for missing in sorted(files_b - files_a):
        print(f"MISSING in {a}: {missing}")
        problems += 1

    for rel in sorted(files_a & files_b):
        bytes_a, bytes_b = (root_a / rel).read_bytes(), (root_b / rel).read_bytes()
        if bytes_a == bytes_b:
            continue
        problems += 1
        print(f"DIFFERS: {rel}")
        try:
            diff = difflib.unified_diff(
                bytes_a.decode().splitlines(), bytes_b.decode().splitlines(), str(root_a / rel), str(root_b / rel), lineterm="", n=0
            )
            for i, line in enumerate(diff):
                if i >= 12:
                    print("    ...")
                    break
                print("    " + line[:200])
        except UnicodeDecodeError:
            print("    (binary)")

    common = len(files_a & files_b)
    if problems:
        print(f"\nFAIL: {problems} problem(s) across {common} compared files")
        return 1
    print(f"OK: {common} files identical")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
