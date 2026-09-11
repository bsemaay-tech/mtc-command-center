# The fifteen numbers — one sitting

For Baris. 5 September 2026.

The readiness checker was built last night. It works. It refuses everything, on purpose.

It refuses because it is waiting on you. Fifteen numbers are missing. Until they exist,
nothing can ever be called ready. That is the design, not a fault.

This packet answers, for each number: what it is, what goes wrong if it is too high,
what goes wrong if it is too low, what a sensible first answer looks like and why,
and what evidence would let you change it later.

**No number in this document is a value.** I am not allowed to pick these and I have not.
Every one of them is yours to say out loud.

---

## First, a correction on the count

The checker itself prints **fourteen** open numbers. You were told fifteen.

The fifteenth is real, and it is number 2 below. The checker shows the day-trading
minimum as **30 trades**. But your own words recorded it as a *starting rule*, not a
settled limit. So it is a number you still owe a decision on: keep it, or change it.

I am counting it. Fourteen truly blank, plus one to confirm. Fifteen.

---

## The five groups

| Group | Numbers | What it decides |
|---|---|---|
| A. Data quality | 1 | How broken can a price history be before you refuse it |
| B. How much trade evidence is enough | 3 | The smallest number of trades you will look at |
| C. The loss ceiling | 1 | How much one trade may lose |
| D. Backtest versus reality | 3 | How far apart the test and the real world may drift |
| E. Forward testing | 7 | How long a strategy runs live-but-fake before you trust it |

---

## Which ones block the most other work

**Rank 1 — the loss ceiling (group C, number 5).**
You already decided no trade may lose more than its own declared stop-loss. But you never
said what that stop-loss is. So the rule you already made cannot be computed at all.
One missing number makes one of your existing decisions useless. This is the worst
blockage in the set, and it is a single answer.

**Rank 2 — the three strategy types (groups B and E, nine numbers).**
You said day, swing and position strategies should have different rules. Nine of the
fifteen numbers sit inside that split. But nothing in the system yet knows what a
strategy's type even is. Answering these nine also forces the system to start recording
type. That is a large amount of downstream work waiting on one sitting of yours.

**Rank 3 — backtest versus reality (group D, three numbers).**
These three are locked together. None of them can be answered alone.

**Rank last — the data gap limit (group A, number 1).**
Do **not** answer this one first. It is blocked in front of you, not by you. See below.

---

# Group A — Data quality

## 1. The maximum data gap

**What it is.** Price history arrives with holes. Minutes or hours are missing. This
number says how much missing data makes a history too poor to trust.

**Too high.** You accept histories full of holes. Every test built on them is a guess
dressed as a measurement. The worst part is silent: the strategy looks fine because the
bad moments simply are not in the data.

**Too low.** Nearly every real history gets rejected. Research stops. You end up either
raising the number under pressure, or quietly ignoring it, which is worse.

**What a sensible first answer looks like.** You already answered this correctly, and
your answer was: do not guess it. Scan your real data first, see what the actual gap
level looks like, and set the limit from that. That is the right instinct and it stands.

**But there is a thing in front of it.** Nobody has yet defined how a gap is even
counted. Three different sensible ways of counting exist. They give three different
answers on the same data. Pick a limit now and it means nothing, because the counting
method can be chosen later to make anything pass.

**So the honest state of this number:** it is not waiting on your judgement. It is waiting
on a counting method being fixed, then a real scan being run, then you looking at the
result. You already ordered exactly that. Leave it.

**What would let you revisit it.** The first real scan of your own data, once the counting
method is fixed.

---

# Group B — How much trade evidence is enough

These three answer one question: how many trades must a strategy have produced before
you are willing to judge it at all? Below that count, the result is noise.

You already ruled that this cannot be one number for all strategies. A day strategy makes
many trades quickly. A position strategy may make a handful in a year. Demanding the same
count from both means never evaluating the slow ones.

## 2. The day-strategy minimum — confirm or change

**What it is.** The smallest number of trades a fast strategy must have before you judge it.
Currently recorded as thirty, marked as a starting rule only.

**Too high.** Good fast strategies wait in the queue for weeks, producing trades nobody
looks at. You lose time, not safety.

**Too low.** A strategy with a handful of lucky trades looks brilliant. You will promote
luck and call it skill. This is the single most common way people fool themselves.

**What a sensible first answer looks like.** Thirty was your own instinct and it is a
common floor for exactly this purpose. Confirming it costs you nothing and unblocks the
whole group. Changing it is also fine. What is not fine is leaving it ambiguous, because
"starting rule" is not a value the checker can use.

**What would let you revisit it.** Once you have a set of real day strategies, look at how
often ones that passed at thirty later fell apart. If they mostly held, thirty was enough.

## 3. The swing-strategy minimum

**What it is.** The same floor, for strategies holding positions for days or weeks.

**Too high.** Swing strategies are slow. A high count means years of waiting. You will
never evaluate one, so you will effectively have banned the category.

**Too low.** Slow strategies produce few trades, so each one carries huge weight. A tiny
count means one good trade decides everything. Very easy to fool yourself here.

**What a sensible first answer looks like.** Do not pick it from a book. Pick it by asking
yourself one question: how long am I willing to wait for a swing strategy to prove itself?
Then work out roughly how many trades a swing strategy produces in that time. That is your
number. It is derived from your patience, which is a real constraint you actually know.

**What would let you revisit it.** The trade rate your first real swing strategies actually
produce. If they trade far more or far less than you assumed, the number moves.

## 4. The position-strategy minimum

**What it is.** The same floor, for strategies holding for months.

**Too high.** You have banned the category. A position strategy may never reach a high
count in your lifetime of testing.

**Too low.** Almost nothing separates the strategy from a single lucky bet.

**What a sensible first answer looks like.** Same method as swing, but the tension is
sharper. Here you have already said something useful: for slow strategies, backtest
evidence may carry more weight, provided it passes every quality check. That is your
release valve. It means the position minimum can be lower than instinct says, because a
long clean backtest is carrying part of the load. Set it knowing that trade.

**What would let you revisit it.** Whether your slow strategies' backtests turned out to
predict their real behaviour. If they did, you can lean on them more. If not, less.

**One thing this group forces.** All three numbers require the system to know which type
each strategy is. It does not know that today. Answering these three starts that work.

---

# Group C — The loss ceiling

## 5. The stop-loss ceiling

**What it is.** The largest loss you will accept from a single trade, stated as a rule
rather than a hope. It is deliberately separate from how much you risk per trade.

**Too high.** One bad trade can take a chunk you cannot recover from. Worse, it makes the
rule you already wrote toothless. "No trade may lose more than its declared stop" is
satisfied trivially if the declared stop is enormous.

**Too low.** You get stopped out of good trades by ordinary market noise. The strategy
never gets the room it needs to work. It will look broken when it is not.

**What a sensible first answer looks like.** This one is not derived from your data. It is
derived from you. The question is: what single-trade loss would make me stop trading and
question everything? Set the ceiling below that. It is a number about your own tolerance,
not about market behaviour, which is why nobody else can propose it.

**Why this is rank 1.** You already made the decision that depends on it. Without this,
that decision cannot be checked against anything. One missing number is disabling a rule
you have already made.

**What would let you revisit it.** Real measured data on how far price moves against a
position before recovering. You said you would revisit after real gap data is measured.
That still holds.

---

# Group D — Backtest versus reality

A strategy behaves one way in a test and another way in the real world. That difference
always exists. These three numbers decide when the difference is too big to ignore.

**These three cannot be answered separately.** They lock together, and the reason is at
the end of this group.

## 6. How much difference is allowed

**What it is.** The gap between what the test promised and what really happened, and the
point at which you say "this is no longer the same strategy".

**Too high.** A strategy that has stopped working keeps its approval. The whole check
becomes decoration.

**Too low.** Every strategy fails, always. Real trading differs from a test for boring,
harmless reasons: fees, timing, queue position. Set this too tight and you are measuring
those, not measuring strategy failure.

**What a sensible first answer looks like.** You already gave the right answer here too:
do not set it yet, measure the real drift first, then set it from what you saw. That is
correct and I am not moving it. But see the trap below.

**What would let you revisit it.** The first published drift measurement from a real
shadow period.

## 7. How long the comparison window is

**What it is.** How much time you compare across. A week of drift and a year of drift are
completely different measurements.

**Too high.** A strategy can be broken for months and still pass, because the long window
dilutes the damage. You find out far too late.

**Too low.** Ordinary noise looks like failure. You will kill working strategies over one
bad week.

**What a sensible first answer looks like.** Tie it to how often the strategy trades. A
window should be long enough to contain a meaningful number of that strategy's own trades.
A window that contains three trades measures nothing.

**What would let you revisit it.** Watching how noisy the measurement is at your chosen
window. If it swings wildly week to week, the window is too short.

## 8. How many matched observations are required

**What it is.** The smallest number of paired test-and-real events needed before the
comparison is allowed to have an opinion at all.

**Too high.** The comparison almost never runs. You have a safety check that never fires.

**Too low.** You will declare a strategy broken, or fine, on two or three data points.
Worse than having no check, because it carries authority.

**What a sensible first answer looks like.** The same reasoning as the trade minimums in
group B. It is a "how many before this means anything" number, and it should not sit far
from those.

**What would let you revisit it.** How often the comparison produces a clear verdict versus
a coin flip at your chosen level.

## The trap in this group

You wisely said: measure the drift first, then set the limit.

But nothing can measure drift yet. There is no agreed definition of what "difference"
means here, and no agreed rule for lining test events up against real ones. Those two are
engineering questions, not yours. Until they are answered, no drift can be measured, so
your sensible "measure first" instruction cannot be carried out.

**Your action here is not a number.** It is to require that the definition and the lining-up
rule get settled, so the measurement you asked for can actually happen.

---

# Group E — Forward testing

Before a strategy touches real money, it runs in fake-money mode against real live prices.
These seven numbers say how long that runs and what it must contain.

Two things here you have already settled, and they stay settled. Internal paper testing
and exchange test-network proof are two separate requirements; neither replaces the other.
And unexplained mismatches are never tolerated, at any count.

What is open is every time period and every trade count.

## 9 and 10. Day strategies — period and trade count

**What they are.** How long a fast strategy runs forward, and how many real forward trades
it must produce in that time.

**Too high.** Fast strategies generate evidence quickly. Making them wait long adds delay
without adding confidence. You lose the main advantage of the category.

**Too low.** The strategy has only seen one kind of market. It has proven it runs, not that
it works. This is exactly the case where a short good run gets mistaken for a real edge.

**What a sensible first answer looks like.** You already gave the shape: shorter than the
others, and a meaningful number of real trades. Derive the period from the trade count, not
the other way round. Decide how many forward trades convince you, then allow however long
that typically takes. The period is a consequence, not a choice.

**What would let you revisit it.** Comparing strategies that passed a short forward period
with how they later behaved. If short forward tests kept passing things that then failed,
lengthen it.

## 11 and 12. Swing strategies — period and trade count

**What they are.** The same two numbers, for the medium-speed category.

**Too high.** Months of waiting per candidate. Your research pipeline stalls.

**Too low.** Too few forward trades to say anything. The forward test becomes a formality
you tick off rather than evidence.

**What a sensible first answer looks like.** Same method: choose the trade count first,
then let the calendar period follow from the swing trade rate. You already said longer
calendar time is acceptable here, and that backtest evidence carries more weight. That
means the forward test's job here is narrower. It proves the strategy operates correctly,
not that the edge is real. A test with that narrower job can be shorter than instinct says.

**What would let you revisit it.** Whether operational problems in swing strategies showed
up early or late in the forward run.

## 13 and 14. Position strategies — period and trade count

**What they are.** The same two, for the slowest category.

**Too high.** You will never approve a position strategy. Realistically, waiting for many
forward trades from a months-long holder can exceed a year.

**Too low.** Almost no forward evidence at all. This is where your own rule bites hardest:
no strategy becomes live-ready from a short forward test alone. Set this too low and you
are in direct conflict with that rule.

**What a sensible first answer looks like.** This is the hardest pair in the packet and it
deserves the most honest framing. For position strategies, a forward test producing enough
trades to prove an edge is probably impractical. So be explicit about what the forward test
is for here: proving the machinery works, orders fill, records reconcile. Then a small
trade count is defensible, because it is not being asked to prove the edge. The backtest
and the quality checks carry that. State that split out loud when you set it.

**What would let you revisit it.** Whether position strategies that passed later showed
operational faults that a longer forward run would have caught.

## 15. How many normal market conditions must be covered

**What it is.** A strategy tested only in a calm rising market has proven nothing about
other markets. This number says how many distinct ordinary conditions the forward evidence
must span.

**Too high.** Some conditions may not occur for years. You have made approval depend on
the weather. Strategies will sit waiting forever.

**Too low.** At one, a strategy proves itself in a single market mood and is approved. The
first change in conditions is a live surprise with real money behind it.

**What a sensible first answer looks like.** Your own words already set a floor: more than
one. That is meaningful and it rules out the worst case. Above that, each addition costs
real waiting time. Note the honest problem: nothing yet defines what a "normal condition"
even is. Whatever count you pick, someone must be able to point at the evidence and say
which conditions it covered. Ask for that definition alongside the number.

**What would let you revisit it.** Whether strategies that passed under few conditions
failed when conditions changed. That is a direct, observable test of this number.

---

# How to spend the sitting

If you only answer some, answer them in this order.

1. **The stop-loss ceiling.** One answer. It re-enables a decision you already made.
2. **The day minimum — confirm thirty or change it.** One answer. It removes an ambiguity.
3. **The swing and position minimums.** Two answers. They unlock the strategy-type work.
4. **The seven forward-testing numbers.** They follow naturally once types exist.
5. **Group D — do not set numbers. Instruct that the definition and lining-up rule be settled.**
6. **The gap limit — leave it. It is waiting on a scan, exactly as you ordered.**

---

# What is true regardless of what you decide today

The checker will keep refusing everything until these are filled. It cannot be talked
into passing anything. It has no default values, no fallbacks and no substitutes. That
was checked independently and confirmed.

Two facts to hold on to.

Nothing has been approved. The checker cannot approve. It can only refuse or wait.

And the deeper precondition is still unmet. The corrected engine has not been accepted.
Even with all fifteen numbers answered, that stays unmet. Answering these fifteen removes
your part of the blockage. It does not make anything ready.
