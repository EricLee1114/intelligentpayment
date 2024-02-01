from tensorflow.keras.models import load_model
import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input

labels = {0: '50% FIFTY PERCENT', 1: '幸福搖搖Blissful Shake', 2: '松屋', 3: '樂聲影城LUX CINEMA',
  4: '櫻桃爺爺CherryGrandFather', 5: 'Color108', 6: 'CROCS', 7: 'FOURPICS', 8: 'JINART', 9: 'LENS',
  10: 'ROBINMAY', 11: '手信坊', 12: '老天祿滷味', 13: '快車肉乾', 14: '維格餅家', 15: '豬帽子', 16: '水水生活'}

# 指定图片所在文件夹
folder_path = '/Users/macbookair/Library/CloudStorage/GoogleDrive-imailliching@gmail.com/我的雲端硬碟/驗證用(每類別留10張)'
model = load_model('/Users/macbookair/venv-metal/TF/IRNV2.h5')
correct = 0  # 初始化正确次数计数器
image_count = 0  # 初始化图片计数器

for img_name in os.listdir(folder_path):
    img_path = os.path.join(folder_path, img_name)
    if img_path.lower().endswith(('.png', '.jpg', '.jpeg')):  # 确保是图片文件
        image_count += 1  # 图片计数器增加
        img = load_img(img_path, target_size=(299, 299))
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        prediction = model.predict(x)
        top_3_indices = np.argsort(prediction[0])[-3:][::-1]
        top_3_probabilities = prediction[0][top_3_indices]

        prefix = img_name.split('_')[0]  # 提取前缀
        correct_label = None
        if prefix.isdigit():
            prefix_num = int(prefix)
            if prefix_num in labels:
                correct_label = labels[prefix_num]

        print(f'第{image_count}筆')
        print(f"Image: {img_name}")
        if correct_label:
            print(f"正確答案: {correct_label}")
        else:
            print("未能辨識")
        print("預測結果 Top 3:")
        for i, index in enumerate(top_3_indices):
            print(f"{i+1}: {labels[index]} (概率: {top_3_probabilities[i]*100:.2f}%)")
            if i == 0 and correct_label == labels[index]:
                correct += 1
                print("測試正確")
                
        print("\n")
if image_count > 0:
    accuracy = correct / image_count * 100
else:
    accuracy = 0
print(f'測試資料共{image_count}筆')
print(f'測試正確有{correct}筆')
print(f'模型正確率: {accuracy}%')

print(f'')
print("\n")
print("\n")

