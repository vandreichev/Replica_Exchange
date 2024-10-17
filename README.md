# Replica_Exchange
! replica variables
set freq = 10000
set name = rex_280_400
set ntotp = 1000000
set printstep = 1000
set lstep = 0.001
set temp = 280
set dt = 10
repd exch nrep 13 freq @freq UNIT 17 -
temp 280 temp 290 temp 300 temp 310 temp 320 temp 330 temp 340 temp 350 temp 360 temp 370 temp 380 temp 390 temp 400
open write unit 17 card name @{name}_trex.log
open write unit 1 card name @{name}_trex.out
outu 1
