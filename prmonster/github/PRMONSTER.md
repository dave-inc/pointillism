# PRMonster

Run this frequently.

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

# Automated PR

```
python3 -m prmonster.pr
```