## NewAlbum   

### 앨범 웹앱 제작  
   
   
   ### 필수 설치 - requirements.txt
   
   ```python
   -f https://download.pytorch.org/whl/cpu/torch_stable.html
   python == 3.8.12 
   torch == 1.10.2+cpu
   heroku
   flask
   gunicorn
   ```
   
   ### 주의사항
   ```
   1. Heroku 용량이 작아 cpu로만 진행 (Heroku 용량 = 500MB, Torch-gpu = 1GB)   
     - Heroku 이미지파일을 임시로 저장 불가능 하기에   
     - 로컬에 저장 한 후 모델을 돌리고 return 진행   
     - 로그아웃 할 시에 사진 os.remove     
   
   
   2. gunicorn --timeout 60 으로 늘려 진행    
    -만약 timeout을 적지 않으면 h13오류  
    
    
   3. 서버 자체 용량이 작아 웹앱이 불안정
   ```
![Mar-31-2022 16-16-08](https://user-images.githubusercontent.com/81940655/160999205-e3d54793-539f-487f-93a9-6bde6cf24c42.gif)
