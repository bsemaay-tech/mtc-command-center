from pathlib import Path
import json

base=Path(r"C:/tmp/P026_DRILLS_TA_20260914/fixtures")
config=base/'config'/'intended_config.json'
meta= json.loads((base/'config'/'intended_config.json').read_text(encoding='utf-8'))
meta['stores'][0]['path']=str((base/'contract_partition'/'stable_prefix'/'drill_3').resolve())
(base/'config'/'intended_config_d4.json').write_text(json.dumps(meta,ensure_ascii=False,sort_keys=True,indent=2)+"\n", encoding='utf-8')
print('wrote', base/'config'/'intended_config_d4.json')
