SELECT
	count(*)
FROM
	frequency ft, frequency fw
WHERE
	ft.term = 'transactions' AND
	fw.term = 'world' AND
	ft.docid = fw.docid;