# Commit-graph practice (guided self-study, 30 minutes)

Six sequences to draw on paper, the evening after Day 1, AI off. For each one, draw the graph
after the last command (one circle per commit, an arrow from each commit to its parent, a label
for every branch and for HEAD), then write how many commits each branch reaches. Then check
yourself: run the sequence in an empty folder and read `git log --oneline --graph --all`.

These are practice sequences. The supervised check uses other sequences of the same kind.

Start each one in a new empty folder with:

    git init -b main
    git commit --allow-empty -m "Start"

## 1

    git commit --allow-empty -m "One"
    git commit --allow-empty -m "Two"

## 2

    git branch spare
    git commit --allow-empty -m "One"
    git switch spare

## 3

    git switch -c left
    git commit --allow-empty -m "L1"
    git switch main
    git commit --allow-empty -m "M1"
    git commit --allow-empty -m "M2"

## 4 (after Day 2, session 1)

    git switch -c topic
    git commit --allow-empty -m "T1"
    git switch main
    git merge topic

## 5 (after Day 2, session 1)

    git switch -c topic
    git commit --allow-empty -m "T1"
    git switch main
    git commit --allow-empty -m "M1"
    git merge --no-edit topic

## 6 (after Day 2, session 3)

    git commit --allow-empty -m "One"
    git commit --allow-empty -m "Two"
    git reset --hard HEAD~1
    git commit --allow-empty -m "Three"

<details>
<summary>Answers</summary>

1. A chain of 3; main reaches 3.
2. main reaches 2; spare reaches 1 (only Start); HEAD points at spare.
3. left reaches 2 (Start, L1); main reaches 3 (Start, M1, M2); 4 commits in all.
4. A fast-forward: main moves to T1; no merge commit; both reach 2.
5. A merge commit with two parents (M1 and T1); main reaches 4; topic reaches 2.
6. main reaches 3 (Start, One, Three); "Two" is no longer on any branch but stays in the reflog.

</details>
