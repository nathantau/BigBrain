FROM pytorch/pytorch
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install libgtk2.0-dev -y

# RUN pip install opencv-python
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]