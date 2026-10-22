# Frozen GRU baseline diagnostic

GGNN-like GRU32 input[m32,u32], hiddenrawh32; no residual. Original encoder/LN/tanhmessage+distance/mean/readout kept with byte-identical initial parameters. GRUW Xavier namespace9921, biases0. 12481P versus12261, notexactmatched. Frozen same BALANCED calendar/inputs/roles/ports/triples; T16, B4, AdamW.003,250updates, seeds2101/2102. Order Grid-localb0(2)→Grid-localXOR(2)→MHU-localb0/XOR(4)→remoteall(8). Each gate requires bothseeds finite train+val>=.98 in every prior condition. Total240s CPU4, no retries/HPO/test/H1–H6/pilotoverride.

Identity: acc219867e36ec0352ddb344e299166b78a811eaf5379fd7c7f50cb1c8e5893e
Protocol: 872d5bfc3114cff6953c178fd4806660e2772a6ec2c7456161985a6ecc222d2e
