# Integrating a linked worktree

Integrate when the skill's rule 6 says, once the worktree and its home clone are clean. The
repository's own instructions choose the required broad check and can add stricter
preconditions; MAM-basics' `AGENTS.md`, “Integrating a worktree branch here”, does both.

1. In the worktree's home clone, fetch `origin`. If `origin/main` moved, fast-forward `main` with
   `git -C <home-clone> merge --ff-only origin/main`.
2. In the worktree, merge `main` into the worktree branch. Resolve conflicts and make any fixes on
   that branch.
3. Run the repository's required check on the merged branch. Commit every explained generated
   change there; an unexplained change is a failure.
4. Immediately before the final fast-forward, fetch `origin` again in the home clone. If
   `origin/main` is not an ancestor of the worktree branch, merge `origin/main` into the worktree
   branch in the worktree and return to step 3. Otherwise fast-forward `main` with
   `git -C <home-clone> merge --ff-only <worktree-branch>`. If the home clone refuses because its
   `main` moved, return to step 2.
5. Push `main` normally. If the push is refused because `origin/main` moved, return to step 4.

The home clone receives only fast-forwards: to a freshly fetched `origin/main` and to the
verified worktree branch. Never replace a failed fast-forward or a refused push with a merge in
the home clone, and never rewrite history or discard work to make the push pass.

Removing the worktree and deleting its branch wait until the task has ended on Windows; never
force removal around a live process. Retirement of a completed worktree follows
`mam-repository-topology/references/repository-maintenance.md`, “Completed linked worktrees”,
for every agent and owner.
