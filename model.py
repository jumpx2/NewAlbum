import torch 

model2 = torch.hub.load('ultralytics/yolov5', 'yolov5m', pretrained=True)
model =model2.eval()