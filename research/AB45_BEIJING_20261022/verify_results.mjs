import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const read = n => JSON.parse(readFileSync(new URL('./'+n, import.meta.url),'utf8'));
const dat=read('weekly_observed.json'), res=read('campaign_results.json');
assert.equal(dat.station_names.length,12);
assert.equal(dat.fields.length,4);
assert.equal(dat.weeks,209);
assert.equal(res.events.length,45);
assert.equal(res.ledger.length,45);
assert.equal(res.final.length,5);
const seen=new Set();
for(let i=0;i<45;i++){
 const ev=res.events[i], row=res.ledger[i], cfg=ev.design_before_result;
 assert.equal(ev.cycle,i+1); assert.equal(ev.test_open,false);
 assert.deepEqual(cfg,row.cfg);
 const key=[cfg.target,cfg.nTrain,cfg.budget,cfg.alpha].join('|');
 assert(!seen.has(key)); seen.add(key);
 if(i<44)assert.deepEqual(ev.next_design,res.events[i+1].design_before_result);
 for(const arm of Object.values(row.arms)){
   assert.equal(arm.selection.length,cfg.budget);
   assert.equal(new Set(arm.selection).size,cfg.budget);
   assert(arm.selection.every(j=>Number.isInteger(j)&&j>=0&&j<48));
   assert(Number.isFinite(arm.rmse)&&arm.rmse>=0);
 }
}
for(const f of res.final){assert(f.samples.eval>=30);assert(Number.isFinite(f.test_rmse));}
console.log('PASS: source dimensions, 45 sequential decisions, 45 budgets, data indexes, holdout markers, 5 final outcomes.');
