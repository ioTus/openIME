---
name: distill-large-source
description: Distilling a source too large to hold in context — a file that returns file_too_large, or a verbatim transcript or document over ~64 KB — into a signal entry or summary, across as many sessions as it takes.
---

Works through a large source in passes, keeping all progress in a committed notes file instead of in context. Any session on any platform can pick up at the cursor. The source stays whole and verbatim.

Tool names below are GitBridge's (`framework/adapters/gitbridge.md`): a ranged file read that reports whether more remains, a metadata-only read for the SHA, and an anchored in-place patch. On another transport, use its equivalents.

## The notes file

Lives beside the source as `<source-stem>-notes.md` and is indexed in that directory's `_index.md`. It stays after synthesis as the re-mining record. Frontmatter is the cursor:

- `source` — repo path of the source
- `source_sha` — blob SHA when the run began
- `size_bytes` — source size
- `chunk_bytes` — default 64000 (~16k tokens); lower it for small context windows
- `overlap_bytes` — default 4000
- `next_offset` — where the next pass reads from; starts at 0
- `last_anchor` — the opening ~12 words of the last complete line recorded; empty at start
- `status` — `in-progress` or `complete`

The body is one section per pass, `## Pass N — bytes A–B`, with these headings: **Span** (first and last timestamps or headings covered), **Structure** (chapter or section titles seen), **Claims and frameworks**, **Specifics** (numbers, names, tools, prompts, prices), **Candidate signals**, **Open questions**. Notes are conclusions with location pointers (timestamp or heading) so any point can be re-read with a targeted range. Quote only short phrases where exact wording matters.

## Authority

The user approves the run once. That approval covers creating and updating the notes file and its index line, one commit per pass, prefix `[docs]`. Every other write — the final entry, index rows, principle graduations — goes through normal draft → approve → push.

## One pass

1. Read the notes file's frontmatter and resume from its cursor. Read the cursor from the repo on every pass, never from memory of your last write: a patch returns a commit SHA, not the file's blob SHA, so a range read of the first ~500 bytes is the check. On the first run, create the file with the cursor at 0.
2. Verify the source with `read_files` `metadata_only`. The SHA matches `source_sha` → continue. It differs → stop and report the drift to the user.
3. Read the range: `read_files` on the single source path with `offset_bytes: next_offset`, `max_bytes: chunk_bytes`.
4. Find the start. Pass 1 starts at the top. Later passes locate `last_anchor` in the returned text and start at the line after it.
5. Find the end. `has_more: true` → end at the last complete line. `has_more: false` → end at the end of the text.
6. Write the pass section covering start to end, filling every heading (write "none" where a heading has nothing). Keep the section to about 8 KB so the finished notes file stays near one chunk and synthesis can load it whole.
7. Advance the cursor: `next_offset` = offset read + `returned_bytes` − `overlap_bytes`; `last_anchor` = opening words of the last complete line recorded. On the final pass, set `status: complete`.
8. Commit the section and the cursor together in one `patch_multiple_files` call: `replace` on the cursor lines in the frontmatter, and `insert_after` to append the section, matching the file's current last line including its newline, with `content` starting with a blank line. Never rewrite the whole notes file. Report the commit SHA and new cursor.

A pass is done when its section is committed and the cursor in the repo points past the lines it recorded.

## Running passes

- **Claude Code** — run passes sequentially, one subagent per pass. Each subagent returns only its commit SHA and cursor. Passes depend on the cursor, so they never run in parallel.
- **Chat** — run passes back to back until `status: complete`. The run approval covers every pass, so never stop between passes to ask. Stop early only when context is at real risk of compaction: say so and name the resume point. A later "continue", in this thread or a new one, resumes from the notes file with no handoff doc and runs to completion.

## Synthesis

Before drafting, check the destination folder and its index for an existing entry on this source — another session may have written one while the passes ran. If one exists, compare it against the notes and propose edits instead of a second entry.

Once `status: complete`, draft the entry from the notes file alone, in the destination's existing format (for the signal library: frontmatter, Signal, Key Takeaways, Notes, Cross-Project Relevance). To verify a specific claim, range-read the source at the pointer the notes give. Present the draft for approval.

The run is complete when the approved entry and its index rows are committed and the notes file is indexed.
