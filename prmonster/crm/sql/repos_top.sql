SELECT *
FROM repos rep
WHERE subscribers + starred + watchers > 2
ORDER BY
    subscribers DESC,
    starred DESC,
    watchers DESC
