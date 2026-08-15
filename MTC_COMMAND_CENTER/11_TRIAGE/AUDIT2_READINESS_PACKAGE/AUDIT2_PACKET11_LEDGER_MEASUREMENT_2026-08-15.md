# Packet 11 freeze-time hours ledger measurement

Status: MEASUREMENT ONLY — NOT RATIFIED

## Anchor

The latest owner-ratified anchor is **approximately 55 h used**, ratified on **2026-08-13 at approximately 10:00 Europe/Chisinau**. The source is `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-13.md`, section 2, introduced by commit `cf2d54c9c5631de10e62de011631babe10ada8e0` at `2026-08-13T10:25:34+03:00`. The source explicitly says the figure is `~55 h`; it is not an exact historical booking.

Earlier candidate anchors found in the required records were **20.5 h used**, the owner-ratified historical baseline carried into the 2026-08-10 ledger; **24.9 h used**, owner-ratified on 2026-08-11; and **~34.8 h used**, owner-ratified later on 2026-08-11. All appear in `MTC_COMMAND_CENTER/11_TRIAGE/LEDGER_STATUS_2026-08-10.md`; all are superseded by the 2026-08-13 approximately 55 h decision, which is therefore the anchor used below.

Commands that reproduce the anchor text, candidate anchors, and introducing commit:

```powershell
Select-String -LiteralPath 'MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-13.md' -Pattern '^## 2\.|answered|Booked honestly|P11-08'
Select-String -LiteralPath 'MTC_COMMAND_CENTER/11_TRIAGE/LEDGER_STATUS_2026-08-10.md' -Pattern 'Ratified baseline|RATIFIED 2026-08-11|Total used|owner-ratified 2026-08-11'
git log --diff-filter=A --format='%H %cI %an %s' -- 'MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-13.md'
```

## Measured sessions since the anchor

Measurement starts **after** the anchor-recording commit. It uses committer timestamps for every commit in `cf2d54c9c5631de10e62de011631babe10ada8e0..HEAD`. A gap **strictly greater than 90 minutes** between consecutive commits starts a new session. Each session span is its last committer timestamp minus its first; a one-commit session therefore measures zero hours. All timestamps below are the recorded `+03:00` committer timestamps.

Raw source command:

```powershell
git log --reverse --format='%H %cI %an %s' cf2d54c9c5631de10e62de011631babe10ada8e0..HEAD
```

Reproduction command for grouping, individual spans, and the total:

```powershell
$anchor = 'cf2d54c9c5631de10e62de011631babe10ada8e0'
$rows = git log --reverse --format='%H%x09%cI%x09%an%x09%s' "$anchor..HEAD" | ForEach-Object {
    $p = $_ -split "`t", 4
    [pscustomobject]@{
        Hash = $p[0]
        Time = [datetimeoffset]::Parse($p[1], [cultureinfo]::InvariantCulture)
        Author = $p[2]
        Subject = $p[3]
    }
}
$sessions = @()
$current = @()
foreach ($row in $rows) {
    if ($current.Count -gt 0 -and (($row.Time - $current[-1].Time).TotalMinutes -gt 90)) {
        $sessions += ,@($current)
        $current = @()
    }
    $current += ,$row
}
if ($current.Count) { $sessions += ,@($current) }
$totalSeconds = 0
for ($i = 0; $i -lt $sessions.Count; $i++) {
    $s = $sessions[$i]
    $seconds = [int64](($s[-1].Time - $s[0].Time).TotalSeconds)
    $totalSeconds += $seconds
    [pscustomobject]@{
        Session = $i + 1
        Date = if ($s[0].Time.Date -eq $s[-1].Time.Date) { $s[0].Time.ToString('yyyy-MM-dd') } else { $s[0].Time.ToString('yyyy-MM-dd') + ' to ' + $s[-1].Time.ToString('yyyy-MM-dd') }
        First = $s[0].Hash
        Last = $s[-1].Hash
        SpanHours = '{0:F6}' -f ($seconds / 3600)
        SpanHMS = [timespan]::FromSeconds($seconds).ToString()
    }
}
"Commits=$($rows.Count); Sessions=$($sessions.Count); TotalSeconds=$totalSeconds; TotalHours=$('{0:F6}' -f ($totalSeconds / 3600)); AnchorPlusMeasuredApproxHours=$('{0:F2}' -f (55 + $totalSeconds / 3600))"
```

| Date | First commit | Last commit | Span in hours | One-line description |
|---|---|---|---:|---|
| 2026-08-13 | `5abd997ee344ab107b62316d4b74651cf1fce816` | `e81ad8848a8ee15e421b5fa9bcc1739aa014b439` | 1.725000 | Pathscope and RP7 adverse audits, RP7 repair/continuation work, and freeze-packet handoff. |
| 2026-08-13 | `57361dd412a69f783b63a8ac9b1ac5c646202d21` | `92e31c25d81a546a8a2028a8ed2b1a8ec4132ebe` | 2.198611 | Recorded owner audit-cap overrides, dispatched both repair lanes, preserved findings, and prepared audit launchers. |
| 2026-08-14 | `2fb3eac05f8da716609549179a7961aa692eae6b` | `6495e697828eb226bd34d59ccd7ff8fc86092021` | 0.996111 | Pathscope repair and rejection, RP7 continuation preservation, packet refresh, and final Pathscope-cycle preparation. |
| 2026-08-14 | `40091b2b795be3339dc0df7014df6bfc091e4eca` | `f05056e562bbb3513d90ba5bc1b0bac9df478688` | 0.241944 | Final Pathscope repair/audit transport block and RP7 reset continuation. |
| 2026-08-14 | `627fca64f805f1ad8b27fd06882adcc929e423b9` | `3016a8d9dd2cc49413dc5cc08038ff08142d693d` | 0.975278 | Compacted and preserved the RP7 Opus quota continuation. |
| 2026-08-15 | `2d0f24d0965c4ba7e7942dddac4fcac3bbb3240b` | `ba0cd476862b400f950920a16b0bc9957c966514` | 0.296389 | Finalized the RP7 cap-override candidate, froze audit contracts, and recorded the Codex T0 block. |
| 2026-08-15 | `6258693d0c6afccd0790d77abd096a548a74667c` | `6258693d0c6afccd0790d77abd096a548a74667c` | 0.000000 | Recorded the RP7 cap-override final audit boundary. |
| 2026-08-15 | `a1846a8357b3ffbad6d34e40135d4c81e82f18c8` | `6a1b473beb6cbf82d26c8379736d706d3dad51cf` | 0.228611 | Authorized the bounded RP7 repair and prepared its T0 audit packets. |
| 2026-08-15 | `80cbed461d0b0371e6eabbfff0e732e5001affaf` | `2d401822b1543e90721704d60b81b9b6b026db02` | 1.155278 | Repaired RP7, froze its audit contracts, and recorded final T0 acceptance. |
| 2026-08-15 | `5ec1787cf795272b5a823a4dab5894802710a16b` | `ddc8a9c802cc45f66f449b02f18a07448afc5f70` | 0.931944 | Dispatched the owner-authorized Pathscope retry and recorded its non-accepting result. |

## Measured totals

- Post-anchor measured commit-session span: **31,497 seconds = 8 h 44 m 57 s = 8.749167 h** across **38 commits in 10 sessions**.
- Anchor plus measured span: **approximately 63.75 h used** (`~55 h + 8.749167 h = ~63.749167 h`, displayed as approximately 63.75 h). This total remains approximate because its 55 h anchor is approximate; only the post-anchor commit-session span is exact under the stated method.
- There is no valid "remaining hours" subtraction from the original 50 h plan. Remaining work is estimated by gates, not by subtracting from 50.

## Limits

Commit-session spans undercount thinking, review, model dispatch, and waiting that produced no commit, including the zero-hour single-commit session; they can also overcount idle time between two commits inside a session. Git history alone cannot support a defensible range for true labor hours, so no true-hours range is asserted. The reproducible result is the **8 h 44 m 57 s measured commit-session span**, not a claim that exactly that much labor occurred.

## Owner signature block

I, Barış, ratify approximately 63.75 hours used at Packet 11 freeze-time, based on the approximately 55-hour owner-ratified anchor plus 8 hours 44 minutes 57 seconds of measured post-anchor commit-session span.
