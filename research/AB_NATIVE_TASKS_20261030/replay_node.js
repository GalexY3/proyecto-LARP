#!/usr/bin/env node
/* Portable replay on user's PRIVATE original-coordinate checkout; never downloads data or writes outcomes.
 * Uses Node.js built-ins only. -- actual historical NPZ are NOT read by this script, it replays the IEEE754 hex exports.
 * Required repo branch research/ab-r-native-functional-20261030 with its original private exports.
 */
"use strict";
const fs=require("fs"),path=require("path"),vm=require("vm");
const root=path.resolve(__dirname,"../..");
const dir=__dirname;
const inputDir=path.join(root,"research/AB_NATIVE_RECOVERY_20261030/private_exports");
const input={};
for(const variant of ["full_spectral","local_only"])for(const seed of [1101,1102,1103]){
  const stem="avian_"+variant+"_N400_g"+seed;
  const file=path.join(inputDir,stem+".json");
  if(!fs.existsSync(file))throw Error("Missing native private JSON: "+file);
  input[stem]=JSON.parse(fs.readFileSync(file,"utf8"));
}
const source=fs.readFileSync(path.join(dir,"native_task_eval_v2.js"),"utf8");
const evaluate=vm.runInNewContext(source+"\n;evaluateNativeTask",{}, {timeout:300000});
if(typeof evaluate!=="function")throw Error("Cannot load frozen evaluator");
const actual=evaluate(input);
const expected=JSON.parse(fs.readFileSync(path.join(dir,"RESULTS_T01_T10_REPAIRED.json"),"utf8"));
for(const property of ["rows","summary"]){
  if(JSON.stringify(actual[property])!==JSON.stringify(expected[property]))throw Error("Replay disagreement: "+property);
}
const original=JSON.parse(fs.readFileSync(path.join(dir,"RESULTS_T01_T10.json"),"utf8"));
const oldNonGp=original.rows.filter(x=>Number(x.task.slice(1))>=6);
const newNonGp=actual.rows.filter(x=>Number(x.task.slice(1))>=6);
if(JSON.stringify(oldNonGp)!==JSON.stringify(newNonGp))throw Error("Non-GP cells changed unexpectedly");
console.log("PASS_NATIVE_EXACT_REPLAY", JSON.stringify({rows:actual.rows.length,aggregates:actual.summary.length,unaffected_original_T06_T10:oldNonGp.length,source:"verified original six N400 hex-coordinate exports",note:"No independent optical data, Wei or neural training"}));
