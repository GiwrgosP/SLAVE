import tabula# readinf the PDF file that contain Table Data
# you can find find the pdf file with complete code in below
# read_pdf will save the pdf table into Pandas
Dataframedf = tabula.read_pdf("offense.pdf")
# in order to print first 5 lines of
Tabledf.head()
