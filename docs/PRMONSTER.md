# PRMonster

Run this frequently.

## JUST RUN THIS

This will check recent github content for new dot files,
and then attemp to make PRs.

```.sh
make search leads run FILE=leads.repo

```

## new leads

By not assigning a `TARGET_USER`, it will search for most recently indexed files.
These are good people to hit, but the API is going to bomb out after 1000 files or so.
So run it frequently. If anything new comes in, it will likely be in the first 1000, and 
so odds are good for getting new leads (or no one uses dot files) 

Keep log and graph so we can get an idea of DOT file editing volume. This will get before and
after repo counts

```python
wc -l github.leads.sorted
make search leads
wc -l github.leads.sorted
```


## Make PR

You should be able to take one-two URLs from `github.leads.sorted` and the PR
should take care of itself.

- This should happen from pointillism.io user.
- PRMonster should be separate repo.


TODO: Document python3 -m prmonster

### Automated PR

Make a `.repos` file to update many repositories using
automated scripts. A `.repos` file consists of `\n` delimited
`owner/project` lines.

Run the script:

```.sh
# make daily leads
python3 -m prmonster
```

#### Client Leads

```.sh
make leads
cat github.leads.sorted
```

