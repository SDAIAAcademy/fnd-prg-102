# Lab 1.4: three sequences

Before you run a sequence, draw the graph you expect in graphs.md (or on paper): one circle per
commit, an arrow from each commit to its parent, a label for each branch and for HEAD.
Then run the sequence inside practice/ and compare with:

    git log --oneline --graph --all

## Sequence 1: two commits on main

    echo "threshold: 150" >> settings.txt
    git add settings.txt
    git commit -m "Record the alert threshold"
    echo "unit: ug/m3" >> settings.txt
    git commit -am "Record the unit"

## Sequence 2: stage one change of two

    echo "stations: 12" > stations.txt
    echo "clients: 4" >> settings.txt
    git add stations.txt
    git status --short          # which file is staged, which is only changed?
    git diff                    # what is not staged
    git diff --staged           # what the next commit will hold
    git commit -m "Count the stations"
    git commit -am "Count the clients"

## Sequence 3: a branch that moves, and main that moves too

    git branch review-notes
    git switch review-notes
    echo "reviewer: check the unit line" > review.txt
    git add review.txt
    git commit -m "Add a review note"
    git switch main
    echo "sectors: 5" >> settings.txt
    git commit -am "Count the sectors"
