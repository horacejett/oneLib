#!/bin/bash

export PYTHONPATH="./"
echo "Reindexing telemetry events..."
python onelib/script/base_telemetry_events_reindex.py
echo "Reindexing completed."