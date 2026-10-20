(function(root){
'use strict';
const metrics=['deprivation_pct','ethnic_minority_pct','men_40_74'];
function parseCSV(text){
 text=text.replace(/^\uFEFF/,'');let rows=[],row=[],value='',quoted=false;
 for(let i=0;i<text.length;i++){let c=text[i];if(c==='"'){if(quoted&&text[i+1]==='"'){value+='"';i++;}else if(!quoted&&value!=='')throw Error('Unexpected quote in CSV');else quoted=!quoted;}
 else if(c===','&&!quoted){row.push(value);value='';}else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&text[i+1]==='\n')i++;row.push(value);if(row.some(v=>v!==''))rows.push(row);row=[];value='';}else value+=c;}
 if(quoted)throw Error('Unclosed CSV quote');if(value!==''||row.length){row.push(value);rows.push(row);}if(!rows.length)throw Error('Empty CSV');let h=rows.shift().map(v=>v.trim());if(new Set(h).size!==h.length)throw Error('Duplicate CSV column');return rows.map((r,i)=>{if(r.length!==h.length)throw Error(`CSV row ${i+2}: expected ${h.length} fields, received ${r.length}`);return Object.fromEntries(h.map((k,j)=>[k,r[j].trim()]));});
}
function quantile(values,q){const a=values.slice().sort((a,b)=>a-b);if(!a.length)throw Error('No valid values for threshold');const p=(a.length-1)*q,i=Math.floor(p);return a[i]+((a[i+1]??a[i])-a[i])*(p-i);}
function classify(rows,top,selected,rule){if(!(top>=1&&top<=100))throw Error('Top percentage must be between 1 and 100');const thresholds=Object.fromEntries(metrics.map(k=>[k,quantile(rows.map(r=>r[k]),1-top/100)]));return {thresholds,rows:rows.map(r=>{const flags=Object.fromEntries(metrics.map(k=>['flag_'+k,r[k]>=thresholds[k]]));const criteria_met=selected.filter(k=>flags['flag_'+k]).length;return {...r,...flags,criteria_met,all_criteria_met:metrics.filter(k=>flags['flag_'+k]).length,matches:selected.length>0&&(rule==='ALL'?criteria_met===selected.length:criteria_met>0)};})};}
function filterRows(rows,state){const q=state.search.toLowerCase();return rows.filter(r=>(state.place==='South Yorkshire'||r.place===state.place)&&(!state.onlyMatches||r.matches)&&(!q||`${r.name} ${r.MSOA21CD} ${r.MSOA21NM}`.toLowerCase().includes(q)));}
function csv(rows,columns=Object.keys(rows[0]||{})){const cell=v=>{let s=String(v??'');if(/^[=+@\-]/.test(s)&&!/^\-?\d+(\.\d+)?$/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';};return [columns.map(cell).join(','),...rows.map(r=>columns.map(k=>cell(r[k])).join(','))].join('\r\n');}
function validateAdmissions(rows,codes){const required=['MSOA21CD','admissions_sar','period','source','geography'];if(!rows.length)throw Error('CSV contains no data rows');for(const k of required)if(!(k in rows[0]))throw Error('Missing required column: '+k);let seen=new Set();let periods=new Set(),sources=new Set();let clean=rows.map((r,i)=>{const code=r.MSOA21CD;if(!codes.has(code))throw Error(`Row ${i+2}: unknown South Yorkshire MSOA21CD ${code}`);if(seen.has(code))throw Error('Duplicate MSOA: '+code);seen.add(code);if(r.geography!=='MSOA2021')throw Error(`Row ${i+2}: geography must be MSOA2021; harmonise older boundaries first`);let v=r.admissions_sar===''?null:Number(r.admissions_sar);if(v!==null&&(!/^\d+(\.\d+)?$/.test(r.admissions_sar)||!Number.isFinite(v)||v<0))throw Error(`Row ${i+2}: SAR must be blank or a non-negative number`);if(!r.period||!r.source)throw Error(`Row ${i+2}: period and source are required`);periods.add(r.period);sources.add(r.source);return {...r,admissions_sar:v};});if(periods.size!==1||sources.size!==1)throw Error('Use one consistent period and source per replacement file');return {rows:clean,missing:[...codes].filter(c=>!seen.has(c)),period:[...periods][0],source:[...sources][0],available:clean.filter(r=>r.admissions_sar!==null).length};}
function bubbleRadius(count){return Math.sqrt(Math.max(0,count))*.32;}
function admissionsColor(value){
 if(value===null||value===undefined||!Number.isFinite(value))return null;
 const low=[94,178,169],mid=[240,243,246],high=[89,70,141];
 const t=value<=100?Math.max(0,value)/100:Math.min(1,(value-100)/100),a=value<=100?low:mid,b=value<=100?mid:high;
 return '#'+a.map((v,i)=>Math.round(v+(b[i]-v)*t).toString(16).padStart(2,'0')).join('');
}
function healthFilter(rows,mode,threshold){return mode==='restrict'?rows.filter(r=>r.admissions_sar!==null&&r.admissions_sar>threshold):rows;}
function summary(rows,geographyCount){const shortlist=rows.filter(r=>r.matches),sum=k=>shortlist.reduce((n,r)=>n+r[k],0);return {count:shortlist.length,geographyCount,residents:sum('population_total'),allThree:shortlist.filter(r=>r.all_criteria_met===3).length,admissionsHigher:shortlist.filter(r=>r.admissions_sar!==null&&r.admissions_sar>100).length,admissionsAvailable:shortlist.filter(r=>r.admissions_sar!==null).length,deprived:sum('deprivation_population'),ethnicity:sum('ethnic_minority'),men:sum('men_40_74')};}
function scoreBenchmark(rows){return rows.reduce((s,r)=>s+r.imd_weighted_score*r.imd_weight_population,0)/rows.reduce((s,r)=>s+r.imd_weight_population,0);}
const api={metrics,parseCSV,quantile,classify,filterRows,csv,validateAdmissions,bubbleRadius,admissionsColor,healthFilter,summary,scoreBenchmark};if(typeof module!=='undefined')module.exports=api;else root.Core=api;
})(globalThis);
