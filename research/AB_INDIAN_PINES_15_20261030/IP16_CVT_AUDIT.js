/* IP16: prospective post-exposure CVT quantization competence gate.
 * This fixes IP03's missing outcome without re-running optical IP01–IP15.
 * Pixel lattice 145x145. No Wei binary, no neural, no raw positions published.
*/
function auditIP16(native){
 "use strict";
 const W=145,N=W*W,SEEDS=[1101,1102,1103],COUNTS=[163,85,68,50,34];
 const gsha={
 MHU:["18f4567d4c72aa7bdd9e2de6cb4f7f5a007df8ad","5642a47b34d1ac3ae840c06a989855db2b5dc6d9","5e2d9ba161bba318ed219c5116e383d443656453"],
 LOCAL:["de57ad4d700303aabb495affa08ecd986371a5f1","05febd925bb0e61a94d4a5d9230d34e0dd3af24b","931c4f73495121fc7034ae6ebdf6b2218ecdcccc"]};
 function rng(seed){let a=seed>>>0;return ()=>{a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return ((t^(t>>>14))>>>0)/4294967296;};}
 function parseFloatHex(h){const m=/^([+-]?)0x([0-9a-f]+)(?:\.([0-9a-f]+))?p([+-]?\d+)$/i.exec(h);if(!m)throw Error("INVALID_HEXFLOAT");
   const z=m[3]||"";return (m[1]==="-"?-1:1)*(parseInt(m[2],16)+(z?parseInt(z,16)/16**z.length:0))*2**Number(m[4]);}
 function readNative(m,seed){
   const item=native[m+seed],i=SEEDS.indexOf(seed);
   if(!item||item.sha!==gsha[m][i]||item.obj.points_float64_hex.length!==400||item.obj.labels_int64.length!==400||item.obj.L_hex!=="0x1.4000000000000p+4")throw Error("SOURCE_MISMATCH");
   const counts=Array(5).fill(0),sites=[],seen=new Set();
   for(let j=0;j<400;j++){
     const c=item.obj.labels_int64[j];counts[c]++;const xy=item.obj.points_float64_hex[j],x=Math.floor(parseFloatHex(xy[0])*W/20),y=Math.floor(parseFloatHex(xy[1])*W/20);
     if(x<0||y<0||x>=W||y>=W)throw Error("MAP_BOUNDS");
     if(seen.has(x*W+y))throw Error("NATIVE_MAP_COLLISION");seen.add(x*W+y);sites.push({x,y});
   }
   if(counts.some((v,c)=>v!==COUNTS[c]))throw Error("TYPE_QUOTAS");
   return sites;
 }
 function randomSites(seed){
    const r=rng(seed^0xBADC0DE),ord=Array.from({length:N},(_,i)=>i),sites=[];
    for(let i=0;i<400;i++){
      const j=i+Math.floor(r()*(N-i));[ord[i],ord[j]]=[ord[j],ord[i]];
      sites.push({x:Math.floor(ord[i]/W),y:ord[i]%W});
    }
    return sites;
 }
 function cvt(seed){
   const r=rng(seed^0xC037),sites=[];
   for(let ix=0;ix<20;ix++)for(let iy=0;iy<20;iy++)
      sites.push({x:Math.min(W-.01,Math.max(.01,(ix+.5)*W/20+(r()-.5)*3)),
                  y:Math.min(W-.01,Math.max(.01,(iy+.5)*W/20+(r()-.5)*3))});
   const start=sites.map(s=>({...s}));
   for(let iter=0;iter<8;iter++){
     const accum=Array.from({length:400},()=>[0,0,0]);
     for(let x=0;x<W;x++)for(let y=0;y<W;y++){
       let best=0,d=Infinity;for(let p=0;p<400;p++){
         const dx=x+.5-sites[p].x,dy=y+.5-sites[p].y,t=dx*dx+dy*dy;
         if(t<d){d=t;best=p;}
       }
       accum[best][0]+=x+.5;accum[best][1]+=y+.5;accum[best][2]++;
     }
     for(let p=0;p<400;p++)if(accum[p][2]){
       sites[p].x=accum[p][0]/accum[p][2];sites[p].y=accum[p][1]/accum[p][2];
     }
   }
   const snapped=sites.map(s=>({x:Math.floor(s.x),y:Math.floor(s.y)}));
   if(new Set(snapped.map(s=>s.x*W+s.y)).size!==400)throw Error("CVT_SNAPPED_COLLISION");
   return {initial:start,continuous:sites,snapped};
 }
 function energy(sites){
    if(sites.length!==400)throw Error("ENERGY_EXPECTS_400");
    let sum=0,max=0;const near=Array(N);let k=0;
    for(let x=0;x<W;x++)for(let y=0;y<W;y++){
      let d=Infinity;for(let p=0;p<sites.length;p++){
         const dx=x-sites[p].x,dy=y-sites[p].y,t=dx*dx+dy*dy;
         if(t<d)d=t;
      }
      sum+=d;max=Math.max(max,d);near[k++]=d;
    }
    near.sort((a,b)=>a-b);
    return {mean_min_squared_pixel_distance:sum/N,p95_min_distance_pixels:Math.sqrt(near[Math.floor((N-1)*.95)]),max_min_distance_pixels:Math.sqrt(max)};
 }
 const all=[];
 for(const seed of SEEDS){
   const v=cvt(seed),init=energy(v.initial),continuous=energy(v.continuous),snap=energy(v.snapped),random=energy(randomSites(seed)),
     mhu=energy(readNative("MHU",seed)),local=energy(readNative("LOCAL",seed));
   all.push({seed,initial: init,after_lloyd_continuous:continuous,after_lloyd_snapped:snap,
     random,mhu,local,
     final_cvt_over_random_energy:snap.mean_min_squared_pixel_distance/random.mean_min_squared_pixel_distance,
     cvt_final_over_initial:snap.mean_min_squared_pixel_distance/init.mean_min_squared_pixel_distance,
     cvt_continuous_over_initial:continuous.mean_min_squared_pixel_distance/init.mean_min_squared_pixel_distance});
 }
 const mean=a=>a.reduce((s,x)=>s+x,0)/a.length;
 const summary={mean_cvt_over_random_ratio:mean(all.map(x=>x.final_cvt_over_random_energy)),
   mean_cvt_over_initial_ratio:mean(all.map(x=>x.cvt_final_over_initial)),
   mean_continuous_cvt_over_initial:mean(all.map(x=>x.cvt_continuous_over_initial)),
   CVT_better_than_random_seeds:all.filter(x=>x.final_cvt_over_random_energy<1).length,
   CVT_continuous_energy_improved_seeds:all.filter(x=>x.cvt_continuous_over_initial<1).length,
   three_seed_energy_MHU_vs_LOCAL:all.map(x=>({seed:x.seed,ratio:x.mhu.mean_min_squared_pixel_distance/x.local.mean_min_squared_pixel_distance}))};
 return {protocol:"IP16_CVT_LLOYD_PIXEL_COMPETENCE",source:"145x145 lattice / original six exported MHU+LOCAL N400",original_geometry_sha_pinned:gsha,
   iterations:8,source_scene:"AVIRIS_IndianPines grid dimensions",result_by_seed:all,summary,
   code_coverage:"CVT_PROTOTYPE_CENTROIDAL_QUANTIZATION_NOT_AUTHENTIC_WEI_ORIGINAL",
   limitations:["AFTER_IP03_ENDPOINT_FAILURE","POST_EXPOSURE_BASELINE_INSTRUMENT_TEST","NO_OPTICAL_OUTCOME_USED","NO_NATIVE_WEI_BINARY","ONE_SCENE_GRID_ONLY","NO_CAUSAL_INFERENCE"],
   scientific_grade:"0/3",CT2_math_before_after:[24,24],CT2_functional_before_after:[18,18]};
}