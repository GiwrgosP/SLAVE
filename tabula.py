from PIL import Image
import glob

images = glob.glob('C:\\Users\\Vostro\\Documents\\GitHub\\SLAVE\\Fotos\\'+"/*.bmp")

for img in images:
    temp = Image.open(img)
    str = img[:-4]
    print(str)
    resizeImage = temp.resize((430,404))
    resizeImage.save(str+"resized.bmp")
