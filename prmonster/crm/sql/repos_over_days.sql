SELECT
    DATE(created),
    COUNT(id)
FROM repos
WHERE
    created > date('now','-14 days')
ORDER BY created DESC