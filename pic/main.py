
import numpy as np
import matplotlib.pyplot as plt
def embed_ascii_in_matrix(matrix, ascii_value):
    # ASCII yi  binaryy ye çevirme
    binary_value = format(ascii_value, '07b')  # 7 bit


    for i in range(len(binary_value)):
        row = i // matrix.shape[1]
        col = i % matrix.shape[1]

        if binary_value[i] == '1':
            matrix[row, col] |= 1
        else:
            matrix[row, col] &= ~1

    return matrix


random_matrix = np.random.randint(0, 256, (23, 23), dtype=np.uint8)

# B baş harfimin ascıı değeri
ascii_of_b = ord('B')


stego_matrix = embed_ascii_in_matrix(random_matrix, ascii_of_b)

# matrixi resim olarak görme
plt.imshow(stego_matrix, cmap='gray')
plt.title("Stego Matrix with Embedded ASCII of 'B'")
plt.axis('off')
plt.show()
