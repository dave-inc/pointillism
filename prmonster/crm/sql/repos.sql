SELECT *
FROM repos rep
ORDER BY
    subscribers DESC,
    starred DESC,
    watchers DESC
