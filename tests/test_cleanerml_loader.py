from __future__ import annotations

import os
from pathlib import Path

from privacy_eraser.cleaning import CleanerOption
from privacy_eraser.cleanerml_loader import load_cleaner_options_from_file


MIN_XML = """
<cleaner os="windows">
  <var name="TMP">
    <value os="windows">%LOCALAPPDATA%\\Temp</value>
  </var>
  <option id="temp">
    <label>Temp Files</label>
    <description>Delete temp files</description>
    <action command="delete" search="glob" path="$$TMP$$\\*.tmp" />
  </option>
  <option id="logs">
    <label>Logs</label>
    <action command="delete" search="walk.files" path="$$BASE$$" />
  </option>
</cleaner>
"""


def test_load_cleaner_options_from_file_var_expansion_and_delete(sandbox: Path, make_glob_files):
    xml_path = sandbox / "cleaner.xml"
    xml_path.write_text(MIN_XML)

    # Env var used in XML (%TMP%)
    tmp_dir = sandbox / "LOCALAPPDATA" / "Temp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    # Create *.tmp files to be matched by glob
    for i in range(3):
        (tmp_dir / f"t{i}.tmp").write_text("x")

    # Multi-var expansion: $$BASE$$ should expand using vars_map; provide it
    # by editing the XML content on the fly for this test
    # We'll simulate loader vars by adding a var in file
    xml2 = xml_path.read_text().replace(
        "</cleaner>",
        "  <var name=\"BASE\"><value>" + str(sandbox / "logs") + "</value></var>\n</cleaner>",
    )
    xml_path.write_text(xml2)

    # Seed logs dir with files
    logs = sandbox / "logs"
    (logs / "a").parent.mkdir(parents=True, exist_ok=True)
    (logs / "a").write_text("1")
    (logs / "b").write_text("2")

    options = load_cleaner_options_from_file(str(xml_path))
    ids = {o.id for o in options}
    assert {"temp", "logs"}.issubset(ids)

    # Execute both options
    for opt in options:
        prev = opt.preview()
        assert len(prev) >= 1
        c, b = opt.execute()
        assert c >= 1 and b >= 0

    # Ensure temp *.tmp files gone
    assert not any(tmp_dir.glob("*.tmp"))
    # Ensure logs dir cleared
    assert not any(logs.rglob("*"))


