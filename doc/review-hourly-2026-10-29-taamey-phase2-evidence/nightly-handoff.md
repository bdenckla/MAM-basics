# October 29 nightly handoff: checked source 6ac28417a243447c24eefb168202585a9949a4ea

The hourly review completed 67 focused tests and documentation-only regeneration; it did not run the full mega or suite. Broad-tested remains 5c28eba09f95fd491afef38454149bde628ee2a7.

At this frozen commit the maintained broad commands remain `py/main_0_mega.py`, then `py/main_test.py`, launched from an isolated source root with its home clone's interpreter and exact required sibling inputs. The new final `taamey-d-doc` mega step calls only `main_taamey_d.almost_main(["doc"])`. The hand-run build wrapper is excluded from mega. The actual doc step passed a fail-fast tripwire for builder/template-fill/FontForge/subprocess entry points, and all committed font bytes and the site pin remained unchanged. No font build was performed. Reinspect scope if the source tip changes.

Keep the existing Basics uharfbuzz 0.57.0 / HarfBuzz 15.0.0 environment; requirements and constraints are unchanged from b1ca848e08476b3d84174755566d640afce02367. Do not downgrade it to another repository's renderer pins. Graphviz 16.0.0 is required. An isolated receipt checkout's code tree is not the checked source.

The owner/plan's approval and prior execution claims remain attributed. They add no authorization to build, migrate, publish, accept baselines or dispatch Pages. This handoff does not change the schedule or broaden this task. All hourly test/generator jobs stopped at 04:46:43.641 UTC.
