from pathlib import Path
from matplotlib.image import imread, imsave
import random


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        self.path = Path(path)
        self.data = rgb2gray(imread(path)).tolist()

    def save_img(self):
        """
        Do not change the below implementation
        """
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

    def blur(self, blur_level=16):

        height = len(self.data)
        width = len(self.data[0])
        filter_sum = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
                average = sum(sum(sub_row) for sub_row in sub_matrix) // filter_sum
                row_result.append(average)
            result.append(row_result)

        self.data = result

    def contour(self):
        for i, row in enumerate(self.data):
            res = []
            for j in range(1, len(row)):
                res.append(abs(row[j-1] - row[j]))

            self.data[i] = res

    def rotate(self, direction='clockwise'):
        """
        Rotate the image in the specified direction.

        :param direction: 'clockwise' or 'counterclockwise'
        """

        # Transpose the image for both directions
        self._transpose()

        if direction == 'clockwise':
            # For clockwise rotation, reverse the rows after transposing
            self._reverse_rows()
        elif direction == 'counterclockwise':
            # For counterclockwise rotation, reverse the columns (the whole image here) after transposing
            self._reverse_columns()

    def salt_n_pepper(self):
        """
        Add salt and pepper noise to the image based on the specified algorithm. (see comments below)
        """
        height = len(self.data)
        width = len(self.data[0])

        for i in range(height):
            for j in range(width):
                rand = random.random()
                if rand < 0.2:
                    self.data[i][j] = 255  # Set to maximum intensity for 'salt'
                elif rand > 0.8:
                    self.data[i][j] = 0  # Set to minimum intensity for 'pepper'
                # If the random number is between 0.2 and 0.8, do nothing (keep the original pixel value)

    def concat(self, other_img, direction='horizontal'):
        # TODO remove the `raise` below, and write your implementation
        raise NotImplementedError()

    def segment(self):
        # TODO remove the `raise` below, and write your implementation
        raise NotImplementedError()

    def _transpose(self):
        """
        Transpose the image (swap rows with columns).
        """
        self.data = list(map(list, zip(*self.data)))

    def _reverse_rows(self):
        """
        Reverse each row in the image.
        """
        self.data = [row[::-1] for row in self.data]

    def _reverse_columns(self):
        """
        Reverse each column in the image.
        This can be done by reversing the entire image.
        """
        self.data.reverse()
