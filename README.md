# MOCHA Leaderboard Data Generation

First install the packages via poetry or pip install. Then download the MCScript validation set via `wget https://raw.githubusercontent.com/DungLe13/commonsense/master/data/dev-data.xml`.

Then run the following: 

```bash
python create_data/create_cosmosqa_data.py
python create_data/create_mcscript_data.py
python create_data/create_narrativeqa_data.py
python create_data/create_socialiqa_data.py
python create_data/merge_all_data.py
```

Resulting data files will be written out into the `data/` directory. The final dev files are `data/dev*.jsonl` and test files are `data/test*.jsonl`.