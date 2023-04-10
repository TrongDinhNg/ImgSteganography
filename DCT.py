import cv2
import numpy as np
from scipy.fftpack import dct, idct

def ImgDCT():
    # Đọc ảnh và chuyển sang ảnh xám
    img = cv2.imread('Image/origin_image.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Thêm hàng và cột để kích thước chia hết cho 8
    h, w = img.shape
    h_new = h + (8 - h % 8) % 8
    w_new = w + (8 - w % 8) % 8
    img = np.pad(img, ((0, h_new - h), (0, w_new - w)), 'constant')

    # Chia ảnh thành các khối 8x8
    blocks = img.reshape(h_new // 8, 8, -1, 8).swapaxes(1, 2).reshape(-1, 8, 8)

    # Số lượng khối DCT
    num_blocks = blocks.shape[0]

    # Tạo ma trận chia
    Q = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                [12, 12, 14, 19, 26, 58, 60, 55],
                [14, 13, 16, 24, 40, 57, 69, 56],
                [14, 17, 22, 29, 51, 87, 80, 62],
                [18, 22, 37, 56, 68, 109, 103, 77],
                [24, 35, 55, 64, 81, 104, 113, 92],
                [49, 64, 78, 87, 103, 121, 120, 101],
                [72, 92, 95, 98, 112, 100, 103, 99]])

    # Áp dụng biến đổi DCT và chia ma trận DCT cho ma trận chia
    quantized_blocks = np.zeros(blocks.shape)

    for i in range(num_blocks):
        dct_block = dct(blocks[i], norm='ortho')
        quantized_dct = np.round(dct_block / Q)
        quantized_blocks[i] = quantized_dct

    # Tạo ma trận ngược chia
    Q_inv = 1 / Q

    # Khôi phục các khối DCT ban đầu
    restored_blocks = np.zeros(blocks.shape)

    for i in range(num_blocks):
        quantized_dct = quantized_blocks[i]
        restored_dct = quantized_dct * Q
        restored_block = idct(restored_dct, norm='ortho')
        restored_blocks[i] = restored_block

    # Tái tạo ảnh ban đầu từ các khối tái tạo
    restored_img = np.zeros(img.shape)

    for i in range(img.shape[0] // 8):
        for j in range(img.shape[1] // 8):
            block_index = i * (img.shape[1] // 8) + j
            block_dct = quantized_blocks[block_index]
            block = idct(block_dct * Q, norm='ortho')
            restored_img[i*8:(i+1)*8, j*8:(j+1)*8] = block


    # Chuyển đổi kiểu dữ liệu của ảnh tái tạo và lưu vào file
    restored_img = np.round(restored_img).astype(np.uint8)
    cv2.imwrite('reconstructed_image.jpg', restored_img)

    # Hiển thị ảnh đã chuyển sang miền DCT
    dct_blocks = np.zeros(blocks.shape)

    for i in range(num_blocks):
        dct_block = dct(blocks[i], norm='ortho')
        dct_blocks[i] = dct_block

    dct_img = np.zeros(img.shape)

    for i in range(img.shape[0] // 8):
        for j in range(img.shape[1] // 8):
            block_index = i * (img.shape[1] // 8) + j
            block_dct = dct_blocks[block_index]
            dct_img[i*8:(i+1)*8, j*8:(j+1)*8] = block_dct

    dct_img = np.round(dct_img).astype(np.uint8)



    # Hiển thị ảnh gốc và ảnh tái tạo
    # cv2.imshow('Original Image', img)
    cv2.imshow('DCT Image', dct_img)
    cv2.imshow('Reconstructed Image', restored_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
