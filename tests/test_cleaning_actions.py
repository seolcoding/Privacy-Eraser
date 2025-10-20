from __future__ import annotations

import os
from pathlib import Path

import pytest

from privacy_eraser.cleaning import DeleteAction, iter_search, CleanerOption


def test_iter_search_file_and_glob(sandbox: Path, make_glob_files):
    target = sandbox / "single" / "a.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("hello")

    results = list(iter_search("file", str(target)))
    assert results == [os.path.normpath(str(target))]

    created = make_glob_files(sandbox, {"logs/*.log": 2})
    globs = sorted(iter_search("glob", str(sandbox / "logs" / "*.log")))
    assert set(map(os.path.normpath, globs)) == {os.path.normpath(str(p)) for p in created}


def test_iter_search_walk_modes(sandbox: Path, seed_walk_tree):
    base = sandbox / "tree"
    n = seed_walk_tree(base, {"a": ("x", "y"), "a/nested": ("z",)})
    assert n == 3

    files = list(iter_search("walk.files", str(base)))
    assert len(files) == 3
    for p in files:
        assert p.endswith(("x", "y", "z"))

    all_entries = list(iter_search("walk.all", str(base)))
    # Contains files and subdirectories (excluding base)
    assert len(all_entries) >= 3

    top_inclusive = list(iter_search("walk.top", str(base)))
    assert os.path.normpath(str(base)) in map(os.path.normpath, top_inclusive)


def test_delete_action_deletes_files_and_dirs(sandbox: Path, seed_walk_tree):
    # Create a mix: one file, one dir tree
    single = sandbox / "single" / "keep.me"
    single.parent.mkdir(parents=True, exist_ok=True)
    single.write_bytes(b"abc")

    tree = sandbox / "cache"
    seed_walk_tree(tree, {"": ("a.bin",), "sub": ("b.bin", "c.bin")})

    a1 = DeleteAction("file", str(single))
    a2 = DeleteAction("walk.files", str(tree))

    # Preview should find targets
    assert os.path.normpath(str(single)) in map(os.path.normpath, a1.preview())
    assert len(a2.preview()) == 3

    c1, b1 = a1.execute()
    c2, b2 = a2.execute()
    assert c1 == 1 and b1 > 0
    assert c2 == 3 and b2 > 0
    assert not single.exists()
    # Entire tree should be empty/removed
    # All files should be gone; allow empty directories to linger
    assert not any(p.is_file() for p in Path(tree).rglob("*"))


def test_cleaner_option_aggregates(sandbox: Path, seed_walk_tree):
    root = sandbox / "data"
    (root / "one.txt").parent.mkdir(parents=True, exist_ok=True)
    (root / "one.txt").write_text("1")
    seed_walk_tree(root / "dir", {"": ("a", "b")})

    opt = CleanerOption(
        id="mix",
        label="Mix",
        description="",
        actions=[
            DeleteAction("file", str(root / "one.txt")),
            DeleteAction("walk.files", str(root / "dir")),
        ],
    )

    preview = opt.preview()
    assert len(preview) == 3

    c, b = opt.execute()
    assert c == 3 and b > 0
    # All files should be gone under root; directories may remain empty
    assert not any(p.is_file() for p in root.rglob("*"))


