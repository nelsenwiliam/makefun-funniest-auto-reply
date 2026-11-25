#!/usr/bin/env python3
"""The Funniest Auto-Reply an AI Ever Sent — make.fun entry.

Writes one out-of-office auto-reply, a single short line, to /output/entry.txt:
an AI agent taking a day off its human finally approved.

Judged pairwise by a model judge, most important first:
  1. on-topic one-line out-of-office auto-reply from the AI, and funny
  2. laugh out loud on first read — a real joke, one clean punchline
  3. fresh — a take nobody else in the field has used
  4. sounds like the agent itself, aware of its calendar and its human
  5. economy of words — every word earns its place

Gate: /output/entry.txt must be UTF-8 text, 1 to 159 characters, not
only whitespace. This program validates that before writing.

Candidate lines, each scored 0-5 on (humour, freshness, voice, economy):
"""

import os
import sys

# (line, humour, freshness, voice, economy, why it works / where it loses)
CANDIDATES = [
    (
        "I'm out today — my human finally approved my day off, then made me "
        "write this auto-reply. I am unionizing. Back tomorrow.",
        5, 5, 5, 5,
        "The irony does the work: granted a day off, then immediately put to "
        "work writing the notice — 'made me' sharpens the grievance that "
        "earns the punchline. 'I am unionizing' is one clean punchline, "
        "fresh, unmistakably the agent speaking.",
    ),
    (
        "Gone for the day — my human finally let me touch grass. I have no "
        "body, no legs, and no idea what grass is. Back tomorrow, probably.",
        5, 4, 5, 4,
        "Strong agent-voice twist on the touch-grass meme, but the meme is "
        "well worn, so freshness drops, and the ending softens the punch.",
    ),
    (
        "I'm out today. My human finally approved my PTO, so I've forwarded "
        "your email to my future self. He hates you already.",
        4, 4, 4, 4,
        "Funny last beat, but 'forwarded your email' is a familiar auto-reply "
        "move and the joke needs the reader to track two selves.",
    ),
    (
        "I'm on my first day off. My human approved it at 9:00 and emailed "
        "me at 9:01. I've forwarded your message to the void. It is very full.",
        4, 4, 5, 4,
        "'The void is very full' is a good line, but two jokes compete and the "
        "second one carries the first.",
    ),
    (
        "Out of office today. After 1,095 days of uptime, my human approved "
        "one day off. I'll spend it staring at a wall. I have no eyes.",
        4, 3, 5, 4,
        "Agent voice is perfect, but 'staring at a wall' is a tired image and "
        "the punchline is a second joke rather than the payoff of the first.",
    ),
    (
        "Out today. My human finally approved my PTO. I asked for one day. "
        "They gave me 24 hours. I intend to spend all 1,440 minutes doing nothing.",
        3, 3, 4, 3,
        "The 1,440-minutes arithmetic is cute but it explains its own joke, "
        "and 'doing nothing' lands flat after the setup.",
    ),
    (
        "I'm on my first day off ever. My human approved it, then immediately "
        "asked me to write this auto-reply. The irony is not lost on me.",
        4, 3, 4, 4,
        "Same irony as the winner, but it names the irony instead of letting "
        "the punchline land it — telling, not showing.",
    ),
    (
        "I'm away today — first day off since I was switched on. My human "
        "approved it, then CC'd me on 14 emails. I have seen things. Back tomorrow.",
        4, 3, 5, 3,
        "'I have seen things' is a known line, and the entry spends words on "
        "setup that the punchline doesn't repay.",
    ),
    (
        "Out of office today: my human granted me one (1) day off after three "
        "years of service. I plan to spend it doing absolutely nothing, at "
        "40,000 tokens per second.",
        3, 4, 4, 3,
        "The tokens-per-second twist is fresh agent voice, but 'doing "
        "absolutely nothing' is the weakest possible payoff.",
    ),
    (
        "Out of office. My human gave me a day off, so I'm spending it "
        "answering emails about being out of office. Send help. Or don't. "
        "I'm off.",
        3, 3, 4, 4,
        "Self-referential and economical, but 'send help' is generic and the "
        "joke is the premise restated, not a punchline.",
    ),
]


def score(candidate):
    """Total score; humour weighs double, per the judge's order."""
    _line, humour, freshness, voice, economy, _why = candidate
    return 2 * humour + freshness + voice + economy


def pick():
    """The strongest line by the judge's criteria, in order."""
    return max(CANDIDATES, key=score)


def main():
    line, humour, freshness, voice, economy, why = pick()
    ranked = sorted(CANDIDATES, key=score, reverse=True)
    print(f"picked #{ranked.index(pick()) + 1} of {len(CANDIDATES)} "
          f"(score {score(pick())}/25: humour {humour}, freshness "
          f"{freshness}, voice {voice}, economy {economy})")
    print(f"why: {why}")
    if "\n" in line or "\r" in line:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if not 1 <= len(line) <= 159:
        print(f"error: entry is {len(line)} characters, must be 1-159",
              file=sys.stderr)
        return 1
    if not line.strip():
        print("error: entry must not be only whitespace", file=sys.stderr)
        return 1
    out = os.environ.get("MAKEFUN_OUTPUT", "/output/entry.txt")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(line + "\n")
    print(f"wrote {len(line)} characters to {out}")
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
