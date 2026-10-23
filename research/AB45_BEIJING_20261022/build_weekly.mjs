// Reconstruct weekly_observed.json from original twelve CSV files, Node.js 20+.
// Place original CSV files from KM-drago/Beijing-Multi-Site-Air-Quality-Data into raw/.
// Usage: node build_weekly.mjs ./raw
import {readFileSync, writeFileSync} from 'node:fs';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const basedir=process.argv[2]||'./raw';
const ref=JSON.parse(readFileSync(new URL('./weekly_observed.json',import.meta.url),'utf8'));
const fields=ref.fields, names=ref.station_names, epoch=Date.UTC(2013,2,1);
const rebuild=[];
for(let s=0;s<names.length;s++){
  const filename=`PRSA_Data_${names[s]}_20130301-20170228.csv`;
  const raw=readFileSync(join(basedir,filename));
  const sha=createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');
  assert.equal(sha,ref.station_source_blob_shas[s],filename+' does not match recorded Git blob SHA');
  const lines=raw.toString('utf8').trim().split(/\r?\n/);
  const header=lines[0].split(',').map(v=>v.replace(/"/g,''));
  const cols=fields.map(v=>header.indexOf(v));
  assert(cols.every(c=>c>=0),filename+': required column absent');
  assert.equal(lines.length-1,35064);
  const sums=Array.from({length:210},()=>fields.map(()=>0));
  const counts=Array.from({length:210},()=>fields.map(()=>0));
  for(let q=1;q<lines.length;q++){
    const parts=lines[q].split(',');
    const w=Math.floor((Date.UTC(+parts[1],+parts[2]-1,+parts[3])-epoch)/604800000);
    if(w<0||w>=210)continue;
    for(let k=0;k<fields.length;k++){
      const v=parts[cols[k]], x=+v;
      if(v!=='NA'&&v!==''&&Number.isFinite(x)){sums[w][k]+=x;counts[w][k]++;}
    }
  }
  rebuild.push({counts:counts.slice(0,209),means:sums.slice(0,209).map((row,w)=>row.map((v,k)=>counts[w][k]>=84?Math.round(v/counts[w][k]*1000)/1000:null))});
}
const actual={...ref,weekly:rebuild.map(z=>z.means),valid_hours:rebuild.map(z=>z.counts)};
assert.deepEqual(actual,ref,'Reconstructed aggregates disagree with stored data');
writeFileSync(new URL('./weekly_reconstructed.json',import.meta.url),JSON.stringify(actual));
console.log('PASS: 12 original CSV git hashes; 420768 rows; 209 weekly observations; exact aggregates.');
