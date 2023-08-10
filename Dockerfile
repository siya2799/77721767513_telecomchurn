FROM python
WORKDIR C:\Users\Siya\Desktop\NM_ProjectBootCamp
#COPY requirements.txt C:\Users\Siya\Desktop\NM_ProjectBootCamp
EXPOSE 8000
RUN pip install -r requirements.txt
#COPY . C:\Users\Siya\Desktop\NM_ProjectBootCamp
ENTRYPOINT ["python3"]
CMD ["TelecomchurnApp.py"]
