# Memory Bank - Gold Tracker DZ

**Methodology Version:** 1.0
**Initialized:** 2026-02-15
**Maintainer:** @mus_Doro3_bot

---

## 📚 What is This?

This folder contains the **canonical memory files** for the Gold Tracker DZ project. Following the Memory Bank methodology, these files provide persistent project context for AI agents working on this codebase.

### Why It Exists
- **AI agents are stateless** - They don't remember past sessions
- **Projects have long-term context** - Decisions, patterns, constraints persist
- **Memory gives continuity** - Reading these files = "waking up" with project knowledge

---

## 📁 File Structure

| File | Purpose | Updated When |
|------|---------|--------------|
| **projectbrief.md** | Project purpose, scope, goals, non-goals | Project definition changes |
| **productContext.md** | Domain knowledge, user personas, market context | User/product understanding evolves |
| **systemPatterns.md** | Architecture, design patterns, data flow | Structural decisions made |
| **techContext.md** | Stack, dependencies, constraints | Technical choices change |
| **activeContext.md** | **Current focus**, next steps, open questions | **Every session/ticket** |
| **progress.md** | Completed work, in-progress, blocked | **Every milestone** |

---

## 🔄 How to Use (For AI Agents)

### Session Start
```
1. Read all files in /memory-bank/
2. Use them as hard constraints and definitions
3. Treat them as "what we know" about the project
```

### While Working
```
1. Keep a "candidate memories" list (new decisions, constraints)
2. Don't update files mid-task (wait for milestone)
3. Cross-reference existing context before making decisions
```

### Milestone Update (End of Task/Session)
```
1. Summarize what changed (new decisions, resolved unknowns)
2. Update activeContext.md (current task/next steps)
3. Update progress.md (what's done/blocked)
4. ONLY update other files if something truly changed:
   - Architecture decision? → systemPatterns.md
   - New tech/constraint? → techContext.md
   - Scope change? → projectbrief.md
5. Consolidate (merge duplicates, don't just append)
6. Write back all changed files
```

---

## 🧠 What Counts as Memory?

### ✅ INCLUDE
- Architecture decisions and design patterns
- Tech stack rules and constraints
- Current focus and open technical challenges
- User/product context and personas
- Resolved blockers and lessons learned
- Configuration choices (e.g., "we use DuckDNS, not Route53")

### ❌ EXCLUDE
- **Secrets/credentials** (never store API keys, passwords)
- **Large code dumps** (keep it short, reference git instead)
- **Raw transcripts** (summarize, don't copy-paste)
- **Temporary noise** (failed experiments, dead ends)
- **Opinions without decisions** (if we didn't choose it, don't store it)

---

## 🔒 Security & Validation

### Memory Poisoning Risk
Since agents write to these files, malicious/false info could persist. Mitigation:

1. **Validate before writing:** Cross-check with actual system state
2. **Version control:** Git tracks changes (rollback if bad data)
3. **Human review:** @attmus reviews major updates
4. **Sandbox updates:** Test in branch before merging to main

### Expiration
- Active context expires after 2 weeks of inactivity
- Technical context reviewed monthly
- Product context reviewed quarterly

---

## 📝 Example: Updating Memory

### Scenario: We Added Redis Caching

**❌ BAD (just appending):**
```markdown
## 2026-02-16
Added Redis. It's fast.
```

**✅ GOOD (structured update):**
```markdown
### Updated techContext.md
- Added Redis to stack (caching layer)
- Configuration: Redis on port 6379, TTL 1 hour
- Reason: Reduce database load for price queries

### Updated systemPatterns.md
- New pattern: Cache-aside for API responses
- Cache key pattern: `prices:{karat}:{jeweler_id}`

### Updated activeContext.md
- Current focus: Monitor cache hit rates
- Next step: Tune TTL based on traffic patterns
```

---

## 🚀 Quick Reference

### For Humans
- **Want to know project status?** → Read `progress.md`
- **Want to know why we built this?** → Read `projectbrief.md`
- **Want to know how it works?** → Read `systemPatterns.md`
- **Want to know what's next?** → Read `activeContext.md`

### For AI Agents
- **Starting work?** → Read all files, start with `activeContext.md`
- **Making decisions?** → Cross-reference `systemPatterns.md` and `techContext.md`
- **Updating users?** → Cite `progress.md` for status
- **Finishing task?** → Update `activeContext.md` and `progress.md`

---

## 📊 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-15 | Initial memory bank structure created |

---

## 👥 Contributors

- **Primary Maintainer:** @mus_Doro3_bot (memory updates, consolidation)
- **Reviewers:** @attmus (project owner), @mus_clawd_bot (strategy)

---

*This methodology ensures continuity across AI sessions while keeping project context clean, structured, and actionable.*
