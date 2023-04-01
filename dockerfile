#Depend on image cơ bản nào
FROM python:3

#Khai bao thu muc lam viec
WORKDIR "D:\Job_Gamma_Detection_Program"

#Copy toàn bộ mã nguồn vào image
COPY . .

#cai thu vien
RUN pip install pandas

#Thực hiện lệnh chạy
CMD ["python","./main.py"]
