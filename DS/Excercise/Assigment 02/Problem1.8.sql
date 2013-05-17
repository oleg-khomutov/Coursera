SELECT
	A.docid 				AS [Row],
	B.docid 				AS [Col],
	SUM(A.count	* B.count)	AS [Val]
FROM
	frequency A, frequency B
WHERE
	(A.term = B.term) AND
	(A.docid = '10080_txt_crude') AND
	(B.docid = '17035_txt_earn')
GROUP BY
	[Row], [Col]
ORDER BY
	[Row];