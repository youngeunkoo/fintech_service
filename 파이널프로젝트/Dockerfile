# Python 3.10 slim 이미지 사용
FROM python:3.8.20

# 시스템 종속성 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    default-jre \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 복사 및 설치
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY ./moodmap /app/moodmap

# 애플리케이션 실행
CMD ["uvicorn", "moodmap.app:app", "--host", "0.0.0.0", "--port", "7860"]