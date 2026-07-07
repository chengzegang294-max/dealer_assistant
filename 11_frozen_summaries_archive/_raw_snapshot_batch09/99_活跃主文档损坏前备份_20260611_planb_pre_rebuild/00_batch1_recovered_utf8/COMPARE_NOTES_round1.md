# batch1 compare notes round1

- Scope: compare active docs with recovered backup copies.
- 02 current active doc head is readable and aligned with latest stable state.
- 03 current active doc contains valid latest sections around later line ranges, but the file head still carries older garbled legacy content.
- about current active doc also contains valid latest sections around later line ranges, but the file head includes older content and can confuse markdown tooling.
- Conclusion: popup risk is more likely caused by large markdown files plus stale mixed legacy blocks, not by current super runtime logic.
- Next manual repair target: clean or isolate stale head blocks in active 03/about after user confirmation.
