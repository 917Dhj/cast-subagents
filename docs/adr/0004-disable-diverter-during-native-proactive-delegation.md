---
status: accepted
---

# Disable Diverter during native proactive delegation

When the Root Session's higher-priority policy explicitly enables Native Proactive Delegation, Diverter is ineligible even if the user explicitly invokes it. Native orchestration remains the sole Orchestration Owner; Diverter silently skips lineup selection, delegation approval, and Execution Backend startup, then lets the current task continue under the native policy. Without that explicit policy signal, Diverter remains eligible. The bundled `SKILL.md` is the single decision source because automatic, implicit, and explicit activation all converge there; the stateless `SessionStart` hook remains activation-only. This capability-based boundary targets current Codex behavior, avoids competing orchestration planes, and does not couple the plugin to a particular model name or reasoning label.
