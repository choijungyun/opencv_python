# Tensorflow 기반의 웨딩드레스 추천 시스템 개발

# 프로젝트 명 : 딥러닝/영상처리 및 옷 분석/추천 시스템 #    

# 작품 소개    
웨딩드레스를 구매할 의사가 있는 소비자가 웨딩드레스를 수월하게
착용하도록 도움을 주며 사용자 개인 맞춤형 웨딩드레스 추천 서비스를 제공함
- 사용자가 어플리케이션을 통해 선호하는 디자인의 웨딩드레스 이미지를 입력하면
해당 사진의 의상정보가 파악되고 이에 맞게 추천하는 의상을 출력됨
- 사전에 텐서플로우를 이용하여 의상 이미지를 분석할 때 필요한 기준을 학습시켰고
학습된 내용을 이용하여 입력된 의상 이미지의 정보가 파악됨

# 작품 내용
- 어플리케이션을 통해 사용자가 자신이 선호하는 디자인의 웨딩드레스 이미지를
입력하면 해당 이미지를 분석
- 분석된 결과와 일치하는 특징을 가진 웨딩드레스들이 화면에 출력함
- OpenCV 와 Webcam을 이용하여 사용자가 선택한 이미지를 사용자의 신체 사이즈에
맞게 조절하여 착용한 모습을 출력함
- 사용자가 착용하고자 하는 웨딩드레스를 선택할 수 있으며 이를 선택했을 시 착용한
드레스가 변경됨
- 저장 버튼을 통하여 현재 사용자가 착용한 웨딩드레스의 정보를 데이터베이스에
저장할 수 있음
- 어플리케이션에 사용자가 저장한 웨딩드레스의 정보가 정리되어 있음

# 작품 구성도
![image](https://user-images.githubusercontent.com/25261332/89698208-f0e45000-d95a-11ea-99e5-ef5ad593c69c.png)

어플리케이션을 이용해 사용자가 이미지를 입력.
입력 된 이미지를 분석한 후 결과물을 어플리케이션에서 출력.
분석 결과는 DBMS에 저장됨
분석 결과를 통해 사용자에게 추천할 웨딩드레스 이미지가 선택됨.
추천받은 이미지는 디스플레이를 통해 사용자가 직접 착용한 모습 확인 가능.
현재 디스플레이 부분은 laptop webcam으로 구현.

# 주요 적용 기술
Image Processing
- OpenCV
Webcam을 실행시켜 사용자의 모습을 가져옴.
haarcascade_frontalface_default.xml를 이용하여 사용자의 face를 detect.
frame을 flip시켜 거울을 볼 때와 똑같은 환경 설정.
사용자가 선택한 이미지를 mask화 시켜 착용.
ㅇ Image Classifying
- Tensorflow
Inception V3 모델을 retrain 후 MM4U에서 사용할 기준 설정
android studio에서 사용하기 위해 retrain, optimize 등의 과정을 거쳐 데이터
재가공
ㅇ 실행환경
- 어플리케이션

# 시스템 흐름도
![image](https://user-images.githubusercontent.com/25261332/89698288-56d0d780-d95b-11ea-8c00-95ed30590acf.png)

