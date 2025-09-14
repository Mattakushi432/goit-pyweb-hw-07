FROM ubuntu:latest
LABEL authors="zakrevskyi"
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["/bin/bash"]

ENTRYPOINT ["top", "-b"]





