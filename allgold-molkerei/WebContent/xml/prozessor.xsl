<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html>
	<head>
		<title>
			<xsl:value-of select="pma_xml_export/database/@name"/>
		</title>
	</head>
	<body>
		<p>
			<h3>
				<xsl:value-of select="pma_xml_export/database/@name"/>
			</h3>
		</p>
		<table border="2">
			<tr>
				<td> <b> ProduktID </b> </td>
				<td> <b> Name </b> </td>
				<td> <b> Preis </b> </td>
				<td> <b> Verfallsdatum </b> </td>
				<td> <b> Anschaffsdatum </b> </td>
			</tr>
			
			<!-- tablleninhalte -->
			
			
			<xsl:for-each select="/pma_xml_export/database/table">
			<tr>
				<td> <xsl:value-of select="column[@name='produktID']"/> </td>
				<td> <xsl:value-of select="column[@name='produktName']"/> </td>
				<td> <xsl:value-of select="column[@name='produktPreis']"/> </td>
				<td> <xsl:value-of select="column[@name='verfallsDatum']"/> </td>
				<td> <xsl:value-of select="column[@name='anschaffungsDatum']"/> </td>
				</tr>
			</xsl:for-each>
			
			
		</table>
	</body>
</html>
</xsl:template>		
</xsl:stylesheet>		