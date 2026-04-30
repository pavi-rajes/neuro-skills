# Asta Research Challenge Submission

## Project Title

AutoDiscovery-Driven Hypothesis Triage and Experiment Cards for Context-Dependent Neural Routing in Mice

---

## Project Summary

AutoDiscovery can generate dozens of hypothesis-experiments from a dataset in a single run — but scaling that output into real science requires two things that don't yet exist out of the box: a way to surface the surprising *and* methodologically sound experiments from the noisy ones, and a structured artifact that captures everything needed to take a promising finding further.

We applied AutoDiscovery to the Allen Institute Dynamic Routing dataset (5-subject pilot, simultaneous recordings across VIS, AUD, PFC, MOs, CA1 during a visual/auditory context-switching task) and used Asta's literature tools alongside custom Claude Code skills to build that pipeline.

AutoDiscovery generates a large, diverse hypothesis space — that breadth is a feature, not a bug. But turning that breadth into a prioritized research agenda requires a triage step. Of the 70 experiments in this run, 19 (27%) were clean enough to act on directly; the rest had issues ranging from underpowered sample sizes to null results that needed more careful interpretation. Rather than reviewing all 70 manually, we built a triage skill to automatically score experiments on scientific rigor and surface the ones worth investing in — turning a firehose into a ranked shortlist.

For the top experiments, we built an **experiment-card skill** that uses Asta's literature tools to gather supporting, opposing, and contextual evidence, constructs a knowledge map of what the field knows vs. what remains contested, and records reflections on what the result rules in or out. Critically, each card also captures the **scaling decision**: which sessions in the full 114-session dataset are the right ones to test this hypothesis — a non-trivial lookup that requires querying brain region coverage, unit counts, and trial structure across the full cohort.

The result is a structured artifact that is both human-readable and agent-actionable: a future agent could read an experiment card and autonomously launch the full follow-up analysis. The strongest finding from the pilot — PFC precedes VIS by ~6–7 trials in context updating after block switches (consistent across all 5 subjects, p=0.063) — has a card that specifies exactly what the full-cohort test looks like and what it would resolve.

**Time:** ~4 hours human time; ~2 hours compute.

---

## Reflections

**What worked well:**

The Asta plugins were fast and easy to integrate. Reading AutoDiscovery experiment output and piping it into literature agents required minimal setup — the skill interfaces composed naturally and the turnaround on literature searches was quick. Launching a literature agent per experiment, having it return supporting, opposing, and contextual papers, and feeding those directly into experiment cards felt seamless. The quality of the literature retrieval was high enough that the knowledge maps in the cards were genuinely useful, not just decorative. AutoDiscovery itself delivered on its core promise: diverse, creative hypotheses across multiple theoretical frameworks that a human experimenter would not have enumerated.

**What was missing:**

The biggest gap is that AutoDiscovery has no awareness of what data actually exists. It generated hypotheses requiring simultaneous dual-region recordings (e.g. VIS+AUD co-recorded) that only 2 of 5 subjects had — those experiments were structurally impossible before they ran. Dataset coverage constraints need to feed into hypothesis generation, not just experiment execution.

There is also no synthesis layer. After experiments run, Asta has no structured way to consolidate results + literature + reflections + scaling decisions into one place. The experiment card artifact — hypothesis, evidence, result interpretation, and a specific prescription for what data to use in a full follow-up — is exactly what an agent would need to autonomously launch the next step. It should be native to the AutoDiscovery loop.

---

## People Involved

Pavi Rajes (pavir@allenai.org)

---

## Supporting Files

- `autodiscovery-results/validation/c003951b_triage.md` — full triage report (70 experiments, PASS/FLAG/FAIL with rationale)
- `autodiscovery-results/experiment-cards/` — 5 experiment cards (node_3_14, node_4_6, node_4_12, node_4_21, node_4_31)
- `autodiscovery-results/viewer.html` — self-contained HTML viewer for browsing all experiment cards

---

## Research Environment

GitHub: https://github.com/pavi-rajes/neuro-skills (branch: `paper-analysis`)
