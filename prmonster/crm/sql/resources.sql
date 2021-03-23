SELECT
    res.filename,
    rep.owner,
    rep.name
FROM resources res
JOIN repos rep ON rep.id = res.repo_id
