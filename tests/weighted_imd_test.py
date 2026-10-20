"""Independent Decimal-based recalculation from official raw IMD and geography."""
from pathlib import Path
from decimal import Decimal
import csv,json,hashlib,collections
p=Path(__file__).resolve().parents[1]
def read(f):return list(csv.DictReader((p/f).open(encoding='utf-8-sig')))
for path,digest in json.loads((p/'tests/baseline-hashes.json').read_text()).items():
 assert hashlib.sha256((p/path).read_bytes()).hexdigest()==digest,path+' changed unexpectedly'
lookup={r['attributes']['LSOA21CD']:r['attributes']['MSOA21CD'] for r in json.loads((p/'raw/lookup.json').read_text())['features']}
a=collections.defaultdict(list)
for r in read('raw/imd.csv'):
 if r['LSOA code (2021)'] in lookup:a[lookup[r['LSOA code (2021)']]].append((Decimal(r['Index of Multiple Deprivation (IMD) Score']),Decimal(r['Total population: mid 2022'])))
for r in read('data/msoa_imd_scores.csv'):
 pairs=a[r['MSOA21CD']];den=sum(n for _,n in pairs);weighted=sum(s*n for s,n in pairs)/den
 assert abs(weighted-Decimal(r['imd_weighted_score']))<Decimal('0.000000000001')
 assert den==Decimal(r['imd_weight_population'])
 assert min(s for s,_ in pairs)<=weighted<=max(s for s,_ in pairs)
assert len(a)==171 and sum(len(v) for v in a.values())==860
print('PASS all six original source files unchanged; all 171 weighted IMD scores independently reproduce from 860 LSOAs')
