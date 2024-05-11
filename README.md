## 설치방법

### front

cd front

<!-- 경로 변경 -->

npm i

<!-- 첫 설치할 것들 -->

npm start

<!-- 프론트 실행 -->

### back

cd back

<!-- 경로 변경 -->

conda create --name [이름]

<!-- 아나콘다 가상환경 설정 이름은 아무거나 편한걸로 -->

conda activate 이름

<!-- 가상환경 실행 -->

pip install fastapi
pip install "uvicorn[standard]"
pip install sqlite

<!-- 설치 할 것들 한번만 설치하면 됨 -->

uvicorn main:app --reload

<!-- 서버 실행 -->

conda deactivate

<!-- 가상환경 끄기 -->
