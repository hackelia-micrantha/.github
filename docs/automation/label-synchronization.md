# Label reconciliation contract

The [organization label taxonomy](../standards/labels.md) specifies canonical names, colors, meanings and dimensions. Repository owners explicitly select their adoption set. Preserve unmanaged labels and ambiguous aliases; do not guess an equivalent meaning.

A read-only reconciliation plan distinguishes no-op, missing canonical label, metadata difference, unambiguous migration, collision and preserved unmanaged input. A plan is evidence, not permission to mutate. Any apply requires reviewed exact scope, least privilege, current preconditions, bounded effects and post-effect read-back. Race or uncertainty must block further effects until reconciled. Never expose private repository inventory or status through a public report.
