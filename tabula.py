import fitz


doc = fitz.open('C:\\Users\\Vostro\\Documents\\GitHub\\SLAVE\\Report1.pdf')
pix = doc.get_pixmap()
print(pix)
pix.save("page-%i.png" % page.number)
