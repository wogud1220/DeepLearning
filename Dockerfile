# 1. Python 3.12 slim 버전 사용
FROM python:3.12-slim

# 2. 컨테이너 내부 작업 디렉토리 지정
WORKDIR /app

# 3. requirements.txt 복사 및 설치 (있을 때만)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt || true

# 4. 코드 복사
COPY . .

# 5. 실행 명령어 (hello.py 실행)
CMD ["python", "hello.py"]