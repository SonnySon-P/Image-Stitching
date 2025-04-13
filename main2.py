import cv2
import numpy as np
import os

# 設定圖片資料夾路徑
imageFolder = "images"

# 取得資料夾中所有圖片
images = []
for file in os.listdir(imageFolder):
    if file.endswith((".jpg", ".png", ".jpeg")):
        imagePath = os.path.join(imageFolder, file)
        image = cv2.imread(imagePath)
        if image is None:
            print(f"無法讀取圖片：{file}")
        else:
            images.append(image)

# 確保有至少兩張圖片
if len(images) < 2:
    print("請至少提供兩張圖片以進行拼接")
    exit()

# 建立ORB特徵偵測器與Matcher
orb = cv2.ORB_create(5000)
matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

# 建立畫布，設定畫布大小為4032x3024
canvasWidth = 4032
canvasHeight = 3024
resultImage = np.ones((canvasHeight, canvasWidth, 3), dtype = np.uint8)

# 初始化
currentImage = images[0]
height, width = currentImage.shape[0 : 2]
resultImage[0 : height, 0 : width] = currentImage

# 建立單位矩陣
totalH = np.eye(3)

# 從第二張圖片開始拼接
for i in range(1, len(images)):
    nextImage = images[i]

    # 將圖片轉為灰階
    currentGrayImage = cv2.cvtColor(currentImage, cv2.COLOR_BGR2GRAY)
    nextGrayImage = cv2.cvtColor(nextImage, cv2.COLOR_BGR2GRAY)

    # 使用ORB偵測特徵點與描述子
    keypoint1, descriptor1 = orb.detectAndCompute(currentGrayImage, None)
    keypoint2, descriptor2 = orb.detectAndCompute(nextGrayImage, None)

    # 檢查特徵點是否足夠
    if descriptor1 is None or descriptor2 is None:
        print("特徵點不足，跳過此圖")
        continue

    # 特徵點配對
    matches = matcher.match(descriptor2, descriptor1)
    matches = sorted(matches, key = lambda x: x.distance)

    if len(matches) < 50:
        print("匹配太少，跳過此圖")
        continue

    # 取得匹配點，取50個特徵點
    sourcePoints = np.float32([keypoint2[m.queryIdx].pt for m in matches[0 : 50]]).reshape(-1, 1, 2)
    destinationPoints = np.float32([keypoint1[m.trainIdx].pt for m in matches[0 : 50]]).reshape(-1, 1, 2)

    # 計算單應矩陣
    H, status = cv2.findHomography(sourcePoints, destinationPoints, cv2.RANSAC, 5.0)

    if H is None:
        print("單應矩陣計算失敗，跳過此圖")
        continue

    # 更新總體轉換矩陣
    totalH = totalH @ H

    # 利用透視變換，生成拼接座標系中的位置
    warped = cv2.warpPerspective(nextImage, totalH, (canvasWidth, canvasHeight))

    # 疊圖
    mask = (warped > 0)  # 找出warped影像中，不是黑色的像素區域
    resultImage[mask] = warped[mask]

    # 成功拼接，並更新nextImage為目前的圖片
    currentImage = nextImage
    print("拼接成功")

# 顯示與儲存
cv2.imshow("拼接結果", resultImage)
cv2.waitKey(0)
cv2.destroyAllWindows()
