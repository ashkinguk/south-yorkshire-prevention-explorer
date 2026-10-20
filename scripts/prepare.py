"""Rebuild all browser CSVs from cached official responses. Python 3.10+, stdlib only."""
import csv,json,pathlib,collections,math,shutil,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; RAW=ROOT/'raw'; OUT=ROOT/'data'; OUT.mkdir(exist_ok=True)
PLACES=['Barnsley','Doncaster','Rotherham','Sheffield']
def read(name):return list(csv.DictReader((RAW/name).open(encoding='utf-8-sig')))
def write(name,rows):
 with (OUT/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def unique(rows,key):
 d={r[key]:r for r in rows};assert len(d)==len(rows),(key,'duplicates');return d
names=[dict(MSOA21CD=r['msoa21cd'],MSOA21NM=r['msoa21nm'],name=r['msoa21hclnm'],place=r['localauthorityname'],boundary_status=r['type']) for r in read('names.csv') if r['localauthorityname'] in PLACES]
bycode=unique(names,'MSOA21CD');codes=set(bycode);assert len(codes)==171
assert all(r['name'] and r['MSOA21NM'] and r['place'] in PLACES for r in names)
write('msoa_names.csv',names)
totals=unique(read('pop_total.csv'),'GEOGRAPHY_CODE');male=collections.defaultdict(list)
for r in read('pop_male.csv'):male[r['GEOGRAPHY_CODE']].append(r)
assert set(totals)==set(male)==codes
periods={r['DATE'] for r in totals.values()};assert len(periods)==1
pop_year=next(iter(periods))
population=[]
for code in sorted(codes):
 rows=male[code];assert len(rows)==35 and {int(r['C_AGE']) for r in rows}==set(range(141,176))
 assert all(r['GENDER']=='1' and r['DATE']==pop_year and r['OBS_STATUS']=='A' for r in rows)
 total=int(totals[code]['OBS_VALUE']);count=sum(int(r['OBS_VALUE']) for r in rows)
 assert totals[code]['DATE']==pop_year and totals[code]['GENDER']=='0' and totals[code]['C_AGE']=='0' and 0<count<total
 population.append(dict(MSOA21CD=code,population_total=total,men_40_74=count,men_40_74_pct=100*count/total,population_period='mid-'+pop_year))
write('msoa_population.csv',population)
benchmark=[]
for b in read('pop_benchmark.csv'):
 actual=sum(r['population_total'] for r in population if bycode[r['MSOA21CD']]['place']==b['GEOGRAPHY_NAME'])
 expected=int(b['OBS_VALUE']);assert actual==expected,(b['GEOGRAPHY_NAME'],actual,expected)
 benchmark.append(dict(place=b['GEOGRAPHY_NAME'],sum_msoa=actual,published_lad=expected,difference=actual-expected))
eth=collections.defaultdict(dict);catnames={}
for r in read('ethnicity.csv'):
 code=r['GEOGRAPHY_CODE'];cat=int(r['C2021_ETH_20']);assert cat not in eth[code];assert r['DATE']=='2021' and r['OBS_STATUS']=='A';eth[code][cat]=int(r['OBS_VALUE']);catnames[cat]=r['C2021_ETH_20_NAME']
assert set(eth)==codes
ethnicity=[];diffs={}
for code,e in sorted(eth.items()):
 assert set(e)==set(range(20));total=e[0];assert total>0
 diffs[code]=sum(e[i] for i in range(1,20))-total
 minority=total-e[1];nonwhite=total-sum(e[i] for i in range(1,6))
 r=dict(MSOA21CD=code,census_total=total,ethnic_minority=minority,ethnic_minority_pct=100*minority/total,non_white=nonwhite,non_white_pct=100*nonwhite/total,ethnicity_period='Census 2021')
 r.update({f'ethnic_group_{i}':e[i] for i in range(1,20)});ethnicity.append(r)
write('msoa_ethnicity.csv',ethnicity)
(OUT/'ethnicity_categories.json').write_text(json.dumps(catnames,indent=2))
lookup=json.loads((RAW/'lookup.json').read_text());assert not lookup.get('exceededTransferLimit')
ls=unique([r['attributes'] for r in lookup['features']],'LSOA21CD');assert {r['MSOA21CD'] for r in ls.values()}==codes
imd=unique(read('imd.csv'),'LSOA code (2021)');expected={c for c,r in imd.items() if r['Local Authority District name (2024)'] in PLACES};assert set(ls)==expected
agg=collections.defaultdict(lambda:[0,0,0]);audit=[]
for code,l in ls.items():
 r=imd[code];pop=int(r['Total population: mid 2022']);dec=int(r['Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)']);assert 1<=dec<=10 and pop>0
 a=agg[l['MSOA21CD']];a[0]+=pop;a[1]+=pop if dec<=2 else 0;a[2]+=1
 audit.append(dict(LSOA21CD=code,MSOA21CD=l['MSOA21CD'],place=l['LAD22NM'],imd_decile=dec,population_mid2022=pop,deprived=int(dec<=2)))
deprivation=[dict(MSOA21CD=c,deprivation_population=a[1],deprivation_denominator=a[0],deprivation_pct=100*a[1]/a[0],lsoa_count=a[2],deprivation_period='IMD 2025; denominator mid-2022') for c,a in sorted(agg.items())]
write('msoa_deprivation.csv',deprivation);write('lsoa_deprivation_audit.csv',audit)
b=json.loads((RAW/'boundaries.geojson').read_text());bc=[r['properties']['MSOA21CD'] for r in b['features']];assert len(bc)==len(set(bc))==171 and set(bc)==codes
(OUT/'msoa_boundaries.geojson').write_text(json.dumps(b,separators=(',',':')))
changes=json.loads((RAW/'change_lookup.json').read_text());assert not changes.get('exceededTransferLimit')
changes=[r['attributes'] for r in changes['features']]
assert {r['MSOA21CD'] for r in changes}==codes
ft=[r for r in read('ft_data.csv') if r['Area Type']=='MSOA' and r['Sex']=='Persons' and r['Age']=='All ages' and not r['Category']]
latest=max(r['Time period Sortable'] for r in ft);ft=unique([r for r in ft if r['Time period Sortable']==latest],'Area Code')
definition=read('ft_definition.csv')[0];assert definition['Indicator ID']=='93227' and definition['Value type']=='Indirectly standardised ratio'
admissions=[]
for c in sorted(codes):
 links=[r for r in changes if r['MSOA21CD']==c]
 unchanged=len(links)==1 and links[0]['CHNGIND']=='U' and links[0]['MSOA11CD']==c
 row=ft.get(c) if unchanged else None
 admissions.append(dict(MSOA21CD=c,admissions_sar=row['Value'] if row else '',period=row['Time period'] if row else '2016/17 - 20/21',source='OHID Fingertips indicator 93227',geography='MSOA2021',status='unchanged_2011_boundary' if row else 'unavailable_merged_boundary',lower_ci_95=row['Lower CI 95.0 limit'] if row else '',upper_ci_95=row['Upper CI 95.0 limit'] if row else '',original_geography='MSOA2011',original_codes='|'.join(r['MSOA11CD'] for r in links),value_note=row['Value note'] if row else 'Observed and expected counts not published; SAR cannot be reliably combined'))
# Bundled source regeneration. Keep local replacement CSVs outside data/ before running.
write('msoa_admissions.csv',admissions)
write('msoa_geography_correspondence.csv',changes)
(OUT/'admissions_definition.json').write_text(json.dumps(definition,indent=2))
joined={c:dict(r) for c,r in bycode.items()}
for rows in [population,ethnicity,deprivation,admissions]:
 for r in rows:joined[r['MSOA21CD']].update(r)
def quantile(v,p):
 v=sorted(v);pos=(len(v)-1)*p;lo=math.floor(pos);hi=math.ceil(pos);return v[lo]+(v[hi]-v[lo])*(pos-lo)
metrics=['deprivation_pct','ethnic_minority_pct','men_40_74'];thresholds={k:quantile([r[k] for r in joined.values()],.8) for k in metrics}
for r in joined.values():
 for k in metrics:r['flag_'+k]=int(r[k]>=thresholds[k])
 r['criteria_met']=sum(r['flag_'+k] for k in metrics);r['matches_any']=int(r['criteria_met']>0);r['matches_all']=int(r['criteria_met']==3)
 for k in ['deprivation_pct','ethnic_minority_pct','non_white_pct','men_40_74_pct']:assert 0<=r[k]<=100
write('msoa_processed_default.csv',list(joined.values()))
qa=dict(status='Core checks passed; 170 admissions values mapped; one merged area unavailable; browser QA not available',msoas=len(codes),lsoas=len(ls),places=dict(collections.Counter(r['place'] for r in names)),benchmarks=benchmark,population=sum(r['population_total'] for r in population),men_40_74=sum(r['men_40_74'] for r in population),ethnicity_category_sum_differences=dict(collections.Counter(diffs.values())),default_thresholds=thresholds,default_any=sum(r['matches_any'] for r in joined.values()),default_all=sum(r['matches_all'] for r in joined.values()),core_join_complete=True,boundaries_complete=True,admissions_available=sum(r['admissions_sar']!='' for r in admissions),browser_tested=False)
(OUT/'qa.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in RAW.iterdir() if p.is_file()}
(OUT/'raw_checksums.json').write_text(json.dumps(manifest,indent=2))
