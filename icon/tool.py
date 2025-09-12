from PIL import Image

# 打开用户上传的图像
img = Image.open("icon_dark.png")

# 创建不同尺寸的图标
sizes = [(256, 256)]
ico_path = "memento_dark.ico"

# 保存为多分辨率的 .ico 文件
img.save(ico_path, format="ICO", sizes=sizes)

