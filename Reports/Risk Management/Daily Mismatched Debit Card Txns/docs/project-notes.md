Objective:
Pull from Identifi, parse text file and then identify mismatches
- Once complete, send to deposit ops

Tasks:
## 2025-09-10
- [ ] Investigate multiple account number situation where transcation doesn't show

# 2025-09-10 
Touched base with PQ today
acctnbr: 26190931
- 2 paypal transactions, 1 showed on 9/3/2025 file

Hypothesis, maybe it isn't showing with duplicate account numbers? I don't know if this would be an issue


# 2025-09-23
Failed today because I had 0.00 transactions
- missing transactions too, but we fixed by replaceing ',' with ''

upstream issue with COCC. EJ/Pat Quinn noticed this as well.

deb/credit will be blank for $0.00 transactions. Still visible on report.