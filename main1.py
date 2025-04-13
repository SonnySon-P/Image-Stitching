import cv2
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

# 確保有足夠的圖片可以進行拼接
if len(images) < 2:
    print("請至少提供兩張圖片以進行拼接。")
    exit()

# 建立影像拼接器
stitcher = cv2.Stitcher_create()

# 執行影像拼接
status, stitched = stitcher.stitch(images)

# 根據狀態碼顯示結果
if status == cv2.Stitcher_OK:
    print("影像拼接成功！")
    cv2.imshow("拼接結果", stitched)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print(f"影像拼接失敗，錯誤代碼：{status}")
