# 前端打包
npm run build 
将dist文件夹下的 static和index.html 拷贝到后端resource目录下
# 打包命令
pyinstaller --add-data=resource;resource --specpath=./ -F main.py
