"""Retrieve official files in sources.json. Cached by default; --refresh redownloads.
Use --latest-population to request the latest Nomis population period, including LAD benchmarks.
The delivered snapshot is pinned to mid-2024. Requires only Python's standard library.
"""
import argparse,concurrent.futures,json,pathlib,urllib.request,hashlib,datetime,time
ROOT=pathlib.Path(__file__).resolve().parents[1];RAW=ROOT/'raw';RAW.mkdir(exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--refresh',action='store_true');p.add_argument('--latest-population',action='store_true');args=p.parse_args()
sources=json.loads((ROOT/'scripts/sources.json').read_text())
def get(item):
 name,url=item;dest=RAW/name
 if args.latest_population and name.startswith('pop_'):url=url.replace('date=2024','date=latest')
 if dest.exists() and not args.refresh and not (args.latest_population and name.startswith('pop_')):return {'file':name,'url':url,'status':'cached','sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
 for attempt in range(3):
  try:
   data=urllib.request.urlopen(url,timeout=120).read()
   if name.endswith(('.csv','.geojson','.json')) and data.lstrip().startswith(b'<'):raise ValueError('Unexpected HTML response')
   if name.endswith(('.json','.geojson')):
    obj=json.loads(data)
    if 'error' in obj:raise ValueError(obj['error'])
   tmp=dest.with_suffix(dest.suffix+'.tmp');tmp.write_bytes(data);tmp.replace(dest)
   print('Downloaded',name,len(data),flush=True)
   return {'file':name,'url':url,'status':'downloaded','sha256':hashlib.sha256(data).hexdigest()}
  except Exception as e:
   if attempt==2:return {'file':name,'url':url,'status':'failed','error':str(e),'previous_cache_retained':dest.exists()}
   time.sleep(1+attempt)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(get,sources.items()))
log={'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':results};(ROOT/'acquisition_log.json').write_text(json.dumps(log,indent=2))
failed=[r for r in results if r['status']=='failed'];print(f'{len(results)-len(failed)}/{len(results)} files available without retrieval error')
if failed:
 for r in failed:print(r['file'],r['error'])
 raise SystemExit('Retrieval incomplete: inspect acquisition_log.json. Existing cached files were preserved; do not mistake stale files for an updated release.')
