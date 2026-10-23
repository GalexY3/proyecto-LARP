# B04 execution manifest schema errata (discovered during GitHub/local byte comparison)

**Original GitHub prereg:** commit 422dccc4da448029601720358d845da980830874, blob 4748f1513fa7c6564d450b70adbf2c2d309096b0. It correctly includes a `group=true` column and a populated claim for C16–C20.

**Fault:** local TSV omitted the literal `true` for each row. The local JSON builder therefore placed the hypothesis prose string into `group` and `null` in `claim`. Python treated the nonempty group string as truthy, so numerical execution still followed the intended subgroup algorithm, but the local metadata and raw-manifest identity were invalid.

**Pre-repair SHA256 raw JSON results:** C16=4a40d213738b5dee31a99483625e1a2c7694acc61d8217da9960eb084d7be077; C17=a59337dfc13569dfaac2e2cc1f4e1975e60a6f6cf46c5b81ced6abd1072530a5; C18=0556a51e203bef60173ae525c2077c4f6f6324182b51ba923709d1ecd8c04e1a; C19=fef308503e78c33cc31543b9cb1b78b03518fd2dda2271a1d754b972fea8143f; C20=83a05369be37886946e8da86b24823c70f1f881b0b4f3b716a5e2723c6cb10a0.

**Repair:** restore the exact GitHub-preregistered TSV locally, regenerate B04.json, rerun C16–C20 using identical code, seeds and sample draws, compare **raw JSON SHA256** to all hashes above. If they mismatch, mark B04 INVALID and reopen instrumentation. C20 remains INVALID due zero outcome variance irrespective of reproduction. This is an execution metadata repair, not a new experimental hypothesis; no new data or seeds introduced.
