# ChinaIC

#Para instalar

  conda env create -f ubuntu.yml

#Para rodar

  conda activate chinaIc
  python run_saved_video.py  (Para rodar num video pré gravado)
  python run_webcam.py (Rodar com um video ao vivo)
  python record_video.py (Para gravar um video para ser usado pelo run_saved_video)

#Caso haja falha em algum import
  pip install cmake
  pip install dlib
  pip install imutils
