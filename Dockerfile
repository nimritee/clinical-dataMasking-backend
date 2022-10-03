FROM python:3.7.14

COPY requirements.txt /
ADD ./mask /mask
ADD ./data /data

RUN set -ex && \ 
    pip install -r requirements.txt


EXPOSE 8050

CMD ["python", "mask/masking.py"]