SELECT
	A.row_num 				AS [Row],
	B.col_num 				AS [Col],
	SUM(A.value	* B.value) 	AS [Val]
FROM
	A, B
WHERE
	A.col_num = B.row_num
GROUP BY
	[Row], [Col]
ORDER BY
	[Col];