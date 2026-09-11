# Market-data collector — written permission packet

Packet 5 of 7. Prepared under decision 187. Prepared for your signature, not signed.

## What you are being asked to approve

You are asked to approve **starting one program that reads public price bars and writes them to disk**.
Nothing has connected to anything. The program has never been run, by anyone.
It was built and checked without a single network call. That was checked twice, independently.
Your approval, plus your answers below, is the only thing that would let it start.

## Which machine

The plan points at your always-on rented server, the one called KVM2, not your own PC.
The program was built and checked on your own PC. It has run on neither.
You must name the machine here. That name is part of what you approve.
Be aware: the program records the name you give but does not enforce it.

## What it reads

One market only: the Bitcoin perpetual market on Hyperliquid.
Four time frames only: 15 minutes, 1 hour, 4 hours, 1 day.
Nothing else is accepted. The program refuses any other market or time frame.
It reads public prices, the same numbers anyone can see without an account.

## What it writes, and where

It writes plain text files into one folder that you name, on that machine.
Two kinds of file, one of each per calendar month: price bars, and a record of gaps.
Files are only ever added to. Nothing already written is changed or deleted.
There is no default location. If you do not name a folder, it refuses to start.
The folder grows every month, forever. It must be backed up; losing it cannot be undone.

## How you are told when it stops — read this part twice

**Today, nothing tells you.** The alarm that would call your phone is a separate job, and it is unfinished.
This program sends no message, no email and no alert of any kind.
It also does not reconnect by itself. If the feed drops, it may simply go quiet.
It fills a gap only when new data arrives afterwards. If nothing arrives, nothing is noticed.
The packet asks you to name how you will be told. The program records your answer and does nothing with it.
So until the alarm job is finished, **checking that it is still alive is a manual habit you must keep**.
The exchange keeps about 52 days of 15-minute history. A gap older than that is lost forever.

## What it may NEVER do

No account of any kind. No key that carries permission to trade.
No order, ever. No position, ever. No path to a broker.
No action at the venue at all, beyond asking for public prices.
The audit searched the program for every one of these and found none.
This limit does not expire, and no later decision changes it without your separate word.

## How you stop it

It runs as one ordinary program in one window. You stop it by stopping that program.
Nothing is installed as a service. Nothing starts it automatically. It does not restart itself.
Stopping it loses nothing already written. It only stops new data arriving.

## What it costs you in attention

- Answering the questions below, and naming the machine and the folder.
- Checking by hand that it is still running, until the alarm job exists.
- Someone technical watching the first run, because the venue's real behaviour is untested.
- Watching disk space, and keeping the backup, month after month.
- Deciding who is allowed to write the approval file. Anyone who can write it can start the program.

## The seventeen unset numbers

No answer, hint or example value is supplied for any of them. None has been invented.
The short label in brackets is an engineer's filing code. You can ignore it.

**These two change what it actually does on day one:**

1. **[N2]** How many live connections should it hold, and how are the four time frames split between them?
   Note: as built, the only answer it will accept is one connection.
2. **[N7]** When filling a gap, how many bars may it request at once, and how long between requests?

**This one is worth deciding early, though nothing is lost by waiting:**

3. **[N5]** Should each bar be filed under its start time or its end time? Both times are stored either way.

**These fourteen belong to parts that are not built yet. Answering them now changes no behaviour:**

4. **[F3]** Should any time frame use different "getting old" and "stale" limits than the ones you set? Which, and what?
5. **[F4]** How long may it stay in catch-up before you are warned?
6. **[N3]** After a drop, how long should it wait before retrying? How long at most? How much should that wait vary?
7. **[N4]** How many failed reconnections in a row before it falls back to asking for data periodically?
8. **[N6]** How far may the machine's clock differ from the exchange's before you are warned?
9. **[N8]** How big a difference between two sources of the same bar counts as a real disagreement?
10. **[N10]** How much overlap between the two sources is enough to run the one-off comparison study?
11. **[N11]** For hourly, four-hourly and daily data, how close to losing history should raise a warning?
    The 15-minute answer is already set at 40 days.
12. **[N12]** Which still-unset data-quality limits from the other package should this one use?
13. **[N13]** How far may a test result differ from live before that other package calls it a problem?
14. **[N14]** What is the longest acceptable delay between it stopping and you being told?
15. **[N17]** What is the lowest price and the lowest volume that should be accepted as real?
16. **[N18]** While running in the reduced mode, how often may it ask for data?
17. **[N19]** How many disagreements in a row before it declares the two sources out of step?

**One flat fact you must decide about:** the program refuses to start unless **all seventeen** carry an answer.
So either you answer all seventeen, or you tell the engineers to narrow that lock.
Separately, four technical definitions are still unfinished. They are engineering work, not your questions.
It cannot start until those are settled either.

## What approving this does NOT approve

- It does not approve any account, key, order, position or broker path. Those stay forbidden.
- It does not approve a second market, a fifth time frame, or a second collector.
- It does not approve installing a service, or anything that starts on its own.
- It does not approve the alarm job, the backup job, or the daily quality checks. None exists yet.
- It does not approve the four unfinished technical definitions, or any answer to your seventeen numbers.
- It does not certify that the program works against the real exchange. That is untested and cannot be tested from here.

## What is not verified

The exchange's real behaviour is unknown to us. The first live run may fail in ways nobody has seen.
On the machine where it was built, the exchange software is already installed.
Only the approval lock stands between the program and the venue.
The approval file itself is the key. Where it lives, and who may write it, is part of this decision.

No recommendation is offered here. The decision is yours.
