import logging
import os
from pathlib import Path

from nomad.datamodel import EntryArchive

from nomad_differ_plugin.parsers.parser import NewParser


def test_parse_file():
    parser = NewParser()
    archive = EntryArchive()
    # csv_path = Path(__file__).resolve().parents[3] / '250507-localhost_output.csv'
    csv_path = os.path.join('tests', 'data', '250507-localhost_output.csv')
    parser.parse(csv_path, archive, logging.getLogger())

    assert archive.data.lab_id == '250507-localhost'
    assert archive.data.process_time[0] == '2025-05-07 11:58:47'
    assert archive.data.foreline_pressure[0] == 0.0244
    assert archive.data.rheed_pressure[0] == 0.0005
