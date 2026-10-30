#!/usr/bin/env node
/* W01, frozen checker. Run: node w01_source_audit.mjs /path/to/noise-checkout */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const root=process.argv[2]; if(!root){console.error('usage: node w01_source_audit.mjs UPSTREAM_REPO_ROOT');process.exit(2);}
const paths={
 top:'RainbowNoise/CMakeLists.txt',
 src:'RainbowNoise/src/CMakeLists.txt',
 main:'RainbowNoise/src/Main/CMakeLists.txt',
 lib:'RainbowNoise/src/Library/CMakeLists.txt',
 cli:'RainbowNoise/src/Main/DartThrowing.cpp'
};
const files={};const sha={};
for(const [name,p] of Object.entries(paths)){
 const b=fs.readFileSync(path.join(root,p));files[name]=b.toString('utf8');
 sha[name]=crypto.createHash('sha256').update(b).digest('hex');
}
const checks=[
 ['cmake_legacy_minimum_2_6',/CMAKE_MINIMUM_REQUIRED\s*\(\s*VERSION\s+2\.6\s*\)/i.test(files.top)],
 ['root_adds_src',/ADD_SUBDIRECTORY\s*\(\s*src\s*\)/i.test(files.top)],
 ['src_adds_Main',/ADD_SUBDIRECTORY\s*\(\s*Main\s*\)/i.test(files.src)],
 ['src_adds_Library',/ADD_SUBDIRECTORY\s*\(\s*Library\s*\)/i.test(files.src)],
 ['Main_declares_DartThrowing_target',/ADD_EXECUTABLE\s*\(\s*DartThrowing(?:\s|\))/i.test(files.main)],
 ['Main_names_DartThrowing_cpp',/DartThrowing\.cpp/i.test(files.main)],
 ['cli_mentions_num_classes',/num_classes/i.test(files.cli)],
 ['cli_mentions_r_values',/r_values/i.test(files.cli)],
 ['cli_mentions_k_number',/k_number/i.test(files.cli)],
 ['cli_mentions_domain_size',/domain_size/i.test(files.cli)]
];
const result={protocol:'W01_SOURCE_ONLY',original_ref:'0d1be2030518517199dff5c7e7514ee072037d59',source_sha256:sha,checks:Object.fromEntries(checks),unknowns:['UPSTREAM_COMMIT_IDENTICAL_WITH_WORKTREE_NOT_INSTRUMENTED','WINDOWS_CMAKE_ERROR_LOG_NOT_READ','COMPILATION_NOT_RUN','QUOTAS_AND_OUTPUT_NOT_RUN','SCIENTIFIC_PERFORMANCE_NOT_RUN']};
console.log(JSON.stringify(result,null,2));
process.exit(checks.some(([,ok])=>!ok)?1:0);
