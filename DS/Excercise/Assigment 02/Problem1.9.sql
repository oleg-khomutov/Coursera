SELECT
	A.docid 				AS [Row],
	B.docid 				AS [Col],
	SUM(A.count	* B.count)	AS [Val]
FROM
	frequency A,
	(
		SELECT	* FROM frequency
		UNION
		SELECT 'q' AS docid, 'washington' AS term, 1 AS count 
		UNION
		SELECT 'q' AS docid, 'taxes' AS term, 1 AS count
		UNION 
		SELECT 'q' AS docid, 'treasury' AS term, 1 AS count
	) AS B
WHERE
	(A.term = B.term) AND
	(B.docid = 'q')
GROUP BY
	[Row], [Col]
ORDER BY
	[Val];