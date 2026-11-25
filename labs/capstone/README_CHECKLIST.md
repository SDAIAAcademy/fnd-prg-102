# README and repository checklist

Tick each line before you post your link. Each group names the rubric criterion it serves.

## README (20)

- [ ] A first paragraph: what the project does and what it produces
- [ ] `## Reproduce` lists every tool needed and the lowest version that works (Git, uv, a
      container engine, Bash or Git Bash)
- [ ] It says where the data comes from: a link to the public source, or the command that
      generates the synthetic data
- [ ] It names the variable or argument that points to the data, and gives no path on your laptop
- [ ] One command rebuilds the environment, runs the project and checks the result
- [ ] It says what success looks like: the checksum line, a row count or a known first line
- [ ] Optional steps (a key, a container engine) are marked optional, with what to skip

## Clean rebuild (30)

- [ ] `pyproject.toml` (or your tool's project file) and its lock are both committed
- [ ] The rebuild uses the lock as it is (`uv sync --locked`, or your tool's equivalent)
- [ ] The rebuild command stops with a clear message when the data location is missing
- [ ] The expected output's checksum (or another exact test) is committed
- [ ] You followed the README in a fresh clone in an empty folder, and it passed

## Container (15)

- [ ] The definition installs from the lock (a hashed export, or the lock tool inside the image)
- [ ] A `USER` that is not root
- [ ] Data comes in through a mounted folder, read-only; results go out through another mount
- [ ] The README gives the build and run commands for a rootless engine

## Hygiene (15)

- [ ] Every setting that differs between machines, and any key, is read from the environment
- [ ] `.env.example` is committed with names and no values; `.env` is ignored
- [ ] `.gitignore` covers data, outputs, `.venv/`, `.env` and caches
- [ ] A scan of the whole history comes back clean (`gitleaks git`, or the course scanner with
      `--history`), and the hook is installed in your clone
- [ ] No data or output file appears in any commit (`git log --stat --all`)

## History (10)

- [ ] Small commits with plain messages that say what changed
- [ ] Changes reached `main` through pull requests, each reviewed by someone other than you
- [ ] The peer's reproduction log merged through a pull request you reviewed

## Follow-up (10)

- [ ] Every failed or guessed step in `reproduction/peer-1.md` has a commit that fixes it
- [ ] `reproduction/peer-2.md` records a successful second reproduction
