#!/usr/bin/env node
// W03 frozen source-only checks, no upstream execution. Run on checkout 1iyiwei/noise@0d1be2030518517199dff5c7e7514ee072037d59.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import child from 'node:child_process';
const root=process.argv[2]; if(!root){console.error('usage: node w03_source_gate.mjs PATH_TO_UPSTREAM_CHECKOUT');process.exit(2)}
const paths={r:'RainbowNoise/src/Library/RMatrix.cpp',rng:'RainbowNoise/src/Library/Random.cpp',conflict:'RainbowNoise/src/Library/UniformConflictChecker.cpp',utility:'RainbowNoise/src/Library/Utility.cpp',main:'RainbowNoise/src/Main/DartThrowing.cpp'};
const rev=child.spawnSync('git',['-C',root,'rev-parse','HEAD'],{encoding:'utf8',timeout:5000});
if(rev.status!==0 || rev.stdout.trim()!=='0d1be2030518517199dff5c7e7514ee072037d59') throw Error('upstream SHA mismatch');
const data=Object.fromEntries(Object.entries(paths).map(([k,p])=>[k,fs.readFileSync(path.join(root,p),'utf8')]));
const checks={
 rmatrix_implementation:/RMatrix::BuildRMatrix\s*\(/.test(data.r),
 rmatrix_diagonal_inputs:/diagonal|diagonal_entries|class_r_values|r_values/i.test(data.r),
 random_init_arg:/Random::InitRandomNumberGenerator\s*\(/.test(data.rng),
 conflict_uses_rmatrix:/r_matrix|RMatrix/i.test(data.conflict),
 utility_has_quota_terms:/target_num_samples_per_class|num_samples_per_class|quota/i.test(data.utility),
 main_fixed_clock_seed:/const\s+unsigned\s+long\s+random_seed\s*=\s*time\s*\(0\)\s*;/.test(data.main),
 main_total_target:/target_num_samples\s*=\s*-k_number\s*;/.test(data.main),
 main_report_counts:/cerr\s*<<\s*"num samples per class"|cerr\s*<<\s*"target number of samples per class"/.test(data.main)
};
const result={protocol:'W03_SOURCE_ONLY',upstream_ref:rev.stdout.trim(),hashes:Object.fromEntries(Object.entries(data).map(([k,v])=>[k,crypto.createHash('sha256').update(v).digest('hex')])),checks,disclosures:['STATIC_PATTERNS_NOT_PROOF_OF_SEMANTICS','NO_AUTHENTIC_WEI_BUILD','NO_5_CLASS_QUOTA_RUN','NO_EXTERNAL_REPLICATION']};
console.log(JSON.stringify(result,null,2));
