SELECT
    DATE(created),
    COUNT(id)
FROM repos
-- WHERE created > date('now','-14 days')
GROUP BY DATE(created)
ORDER BY created DESC
