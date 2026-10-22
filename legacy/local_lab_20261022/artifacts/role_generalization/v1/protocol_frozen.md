# Frozen coordinate input ablation

Original GGNNLikeModel,12481P,T16,B4,250updates,.003AdamW; Gridg1101,targetb0,seeds2101/2102. Only change zeroes every slot21:25 at every node in copied train/val/measurement inputs. COORDS_ON reused, same byte initialization/input noncoordinate channels/targets/calendars/graph/edge distances. 120s CPU4; final state only; both finite train+val>=.98 gate. No automatic XOR/MHU/remote, retries,test,AB or scientific gate override.

Identity: 00bba94bd0208fb164f89b8fed14b71bbb34635d114edbbc70acc344aaf23376
Protocol: e0adac9817706f139a65dc4c2d8beaa5e78c3d560ee6000ab06e5b50ed9c910e
