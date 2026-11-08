# git

## Ignore a file without listing it publicly

`.git/info/exclude` works exactly like `.gitignore`, but it lives inside `.git/` and is never committed.

```
echo "my-private-file" >> .git/info/exclude
```

## A file was staged before it was ignored

Ignore rules only apply to untracked files. To un-stage one and keep your copy on disk:

```
git rm --cached <file>
```

Check before pushing a public repo: `git ls-files` lists everything git will publish.

## Multi-line commands in bash

End every line but the last with a backslash, and put nothing after it, not even a space:

```
git commit -m "subject" \
  -m "body line one" \
  -m "body line two"
```

Each `-m` becomes its own paragraph in the message.

## Commit prefixes

| Prefix | Means |
|---|---|
| `feat` | new behavior in the code |
| `fix` | a bug fix |
| `test` | only test files changed |
| `refactor` | structure changed, behavior didn't |
| `docs` | documentation only |
| `chore` | config and housekeeping (`.gitignore`, tooling) |
| `wip` | work in progress, may not run |

With test-first: `test(RED): ...` for the failing test, `feat(GREEN): ...` for the code that passes it.

## Fixing the last commit message

```
git commit --amend -m "new message"
git push --force    # only safe if nobody else has pulled it
```
