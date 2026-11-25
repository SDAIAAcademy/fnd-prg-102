# Guided pre-work, 90 minutes

Do this before Day 1. It installs the three tools the labs use, sets up the lab workspace, and
gives you twenty minutes in a terminal so that Day 1 can start with the shell itself. If a step
fails, write down the command and the last line of its error and bring it to the first session.

| Part | Minutes |
|---|---|
| 1. Install Git, a Bash terminal and uv | 30 |
| 2. Tell Git who you are | 5 |
| 3. Set up the lab workspace | 15 |
| 4. Twenty minutes in the terminal | 20 |
| 5. Read: what a commit is | 15 |
| 6. Check yourself | 5 |
| **Total** | **90** |

## 1. Install Git, a Bash terminal and uv (30 minutes)

- **Windows:** install Git for Windows; it brings Git Bash, the terminal used in every lab. Open
  Git Bash, not PowerShell or the Command Prompt, for the labs.
- **macOS:** Git comes with the command line developer tools (`xcode-select --install`); the
  Terminal app runs zsh, and `bash` is there too.
- **Linux:** Git from your distribution's packages.
- **uv** on every system: follow the installation page of uv's documentation. It installs
  without administrator rights.

Then, in the terminal:

```bash
git --version        # 2.40 or later
uv --version
uv python install 3.13
```

No administrator rights? Use the provided Linux workspace: the trainer sends its address and
your account before Day 1.

## 2. Tell Git who you are (5 minutes)

Every commit records a name and an email. Use the name you want your peers to see and an email
you are happy to make public, or the private address your host offers.

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

On a company laptop, check with your IT team before changing global settings; inside a single
repository the same commands without `--global` apply to that repository only.

## 3. Set up the lab workspace (15 minutes)

From the course folder (cloned or unzipped):

```bash
uv run labs/kit/setup.py             # writes the lab workspace ../air-labs
cd ../air-labs
uv run lab.py list                   # twelve labs
uv run lab.py start 1.1              # the first lab's starting folder
ls 1.1
```

On Windows, keep the path short (for example a folder directly under your home folder):
`uv run labs/kit/setup.py --to ~/air-labs`.

## 4. Twenty minutes in the terminal (20 minutes)

Work in the lab workspace folder (`air-labs`). Type each command; read what it prints before the next one.

```bash
pwd                  # where am I?
ls                   # what is here?
ls -l                # with sizes, dates and permissions
cd 1.1               # go into a folder
cd ..                # back up one level
mkdir scratch        # make a folder
cd scratch
echo "first line" > note.txt
cat note.txt
cd .. && rm -r scratch
```

Then try `man ls` (or `ls --help` on Git Bash), find one option you did not know, and try it.
Tab completes a file name; the up arrow brings back the last command.

## 5. Read: what a commit is (15 minutes)

Read the first part of *Pro Git*, chapter 3, "Branches in a Nutshell" (git-scm.com), up to the
section on creating a new branch. Look at the drawings: each commit points to its parent, and a
branch is a label on one commit. Day 1's last session draws these graphs by hand.

## 6. Check yourself (5 minutes)

- `git --version`, `uv --version` and `git config user.name` all print something.
- `uv run lab.py list` in the workspace prints twelve labs.
- You can say, in one sentence, what `pwd`, `ls` and `cd ..` do.

If anything fails, bring the command and the last line of its error to Day 1.
