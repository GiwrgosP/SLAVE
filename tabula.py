import fitz


doc = fitz.open('C:\\Users\\Vostro\\Documents\\GitHub\\SLAVE\\Report1.pdf')
for page in doc:
    text = page.get_text("html")
    print(text)
