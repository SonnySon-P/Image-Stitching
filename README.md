# Image Stitching for openCV

一、目標： 以下程式碼旨在實現多張影像的自動拼接功能。

二、使用語言： Python

三、相依套件： openCV

四、開發IDE： Visual Studio Code

五、程式碼說明：
1. main1.py: 使用openCV的stitcher進行影像拼接
2. main2.py: 使用openCV獲取特徵點，並運用Homography Matrix計算

六、成果展示：
<br>
<div align="center">
	<img src="./截圖.png" alt="Editor" width="500">
</div>
<br>
   
七、未來規劃： 本次實作是以同一張影像進行切割，模擬多張照片進行影像拼接。然而在實際應用中，通常是透過鏡頭於不同時間與角度拍攝多張照片，進行拼接的情境將更為複雜。因此，未來可進一步挑戰真實環境下的影像拼接，作為進階實作的發展方向。
