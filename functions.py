from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog
import matplotlib.pyplot as plt
from skimage import exposure
from numpy.linalg import norm
from skimage.color import rgb2gray
from skimage.color import rgba2rgb
from BingImage import Bing


class HOG:
    def __init__(self):
        self.num = 100
        self.main_path = r'D:\PyCharm\pythonProject\images_project'

    def getImages(self, text, db):
        bing = Bing(text, self.num, db)
        bing.run()

    def resizeImage(self, path):
        img = imread(path)
        resized_img = resize(img, (128 * 4, 64 * 4))
        return resized_img

    def getImageHOG(self, path, multicolor):
        img = self.resizeImage(path)
        if multicolor:
            out, hog_image = hog(img, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True, channel_axis=-1, feature_vector=True)
            return out, hog_image
        if len(img[0][0]) == 4:
            img = rgba2rgb(img)
        wb_img = rgb2gray(img)
        out, hog_image = hog(wb_img, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True, feature_vector=True)
        return out, hog_image

    def showHOGPicture(self, path, multicolor):
        out, hog_image = self.getImageHOG(path, multicolor)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)
        ax1.axis('off')
        ax1.imshow(hog_image)
        ax1.set_title('Input image')

        # Rescale histogram for better display
        hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))

        ax2.axis('off')
        ax2.imshow(hog_image_rescaled)
        ax2.set_title('Histogram of Oriented Gradients')
        plt.show()

    def getCousinDist(self, X, Y):
        cos_sim = (X @ Y)/(norm(X)*norm(Y))
        return 1 - cos_sim

    def Binary_To_File(self, BLOB):
        with open(r'..\pythonProject\images_project\current.jpg', 'wb') as file:
            file.write(BLOB)

    def findSamiestPict(self, path, picts, multicolor):
        Y, hog_img = self.getImageHOG(path, multicolor)
        cosinis = []
        indexes = []
        for pict in picts:
            self.Binary_To_File(pict[1])
            X, cur_hog = self.getImageHOG(r'..\pythonProject\images_project\current.jpg', multicolor)
            indexes.append(pict[0])
            cosinis.append(self.getCousinDist(X,Y))
        res = dict(sorted(dict(zip(cosinis, indexes)).items()))
        return res


    def Binary_To_File_Save(self, BLOB, request, name):
        with open(rf'..\pythonProject\Результат\{request}\{name}.jpg', 'wb') as file:
            file.write(BLOB)
