# 2025-08-21
Fixed this up.

Repo could still use cleaning up

The missing items on XAA are due to the accounts being closed or not included on allowed minor list

This was found in exploration notebook.

We can take the _merge right only to get XAA only and then join back active account data to see products:
- IOLTA
- Community checking
- Some personal stuff.

# 2025-08-29
Added new minors for business accounts that we missed on first pass

still needs a revamp. This will simplify pulling from directly 


# 2025-09-09
Hi Chad –

 

I know your schedule is jam packed and we are meeting on Wednesday but, in the interim I just wanted to explain to you that my report is show less fee income than your report is showing.

 

I would expect it to be the same or less but not more.  It could be less because you might be missing certain minors but, I don’t think that is the case.  I wouldn’t expect it to be more though because the fee income data on your report is directly coming from my report.  It either would match on account number or not but, I don’t know how your report is actually showing more.

 

My post ECR fee net number is $50,744.72 which I’ve proofed all the way to Accountings entry they show.

 

Your report post ECR net number is $55,727.65. This is a $4,982.93 difference.

 

Perhaps in between us meeting you’re able to put eyes on this and see what that difference is accounting for?

 

Thanks and talk soon,

Steve

---

I figured it out I think. The way I look at cycle date is to rank them in descending order. This may or may not be the most current month. For some reason, some of the accounts show up with Cycle Date end most recent for 0.0 and others just don't even list a record. I am looking at most recent month on my consolidated report rather than strictly specifying the most recent month is the only allowed one. That would make sense to me.

Can validate the delta afterward because you can take my output(full unadjusted) and then you can take steve's output - do an outer join and you should be able to see the records that show up on his and not on mine and that should be the $ diff
- XAA report will be higher. 