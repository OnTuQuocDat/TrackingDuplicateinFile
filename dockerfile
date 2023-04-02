#Depend on image cơ bản nào
FROM python:3

#Khai bao thu muc lam viec
WORKDIR "D:\Job_Gamma_Detection_Program"

#Copy toàn bộ mã nguồn vào image
COPY . .

#cai thu vien
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN apt-get install libxcb-xinerama0
RUN pip install pandas
RUN pip install PyQt5
# RUN apt install libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0

# RUN apt-get update && apt-get install PyQt5.QtWidgets
# RUN apt-get update && apt-get install PyQt5.QtCore
# RUN apt-get update && apt-get install libgl1
#Thực hiện lệnh chạy
CMD ["python","./main.py"]
