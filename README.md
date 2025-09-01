GT TEST

가상환경 생성
```
conda env create -f environment.yml
```

가상환경 활성화
```
conda activate gttest_env
```

파일 구조
```
project_folder/gttest_main.py
project_folder/gttest_analysis.py
project_folder/video/테스트할 동영상 파일
```


프로젝트 설명
```
1. 3D skeleton 데이터 추출 및 감지
   -> 입력된 비디오를 프레임 단위로 분석(mediapipe pose라이브러리를 사용하여 3D skeleton데이터를 실시간으로 추출가능(x,y,z좌표 추출)
2. VLM기반 동작분석 및 분류
   -> 핵심 프레임을 선별(이벤트 감지)하여 Gemini로 전송
   -> Gemini가 skeleton 데이터 + RGB이미지에 담긴 실제 시각정보 + 동작 분류 및 설명 텍스트 프롬프트를 결합하여 프레임속 동작을 이해하고 json형식으로 분류결과 반환
3. RoboDK에서 실행시킬 "로봇제어 스크립트 생성"
```
