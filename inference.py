from ultralytics import YOLO


model_path = "/home/weedy/weedy_scripts/models/coco_ncnn_model"
img_path = "/home/weedy/weedy_scripts/test_img/coco1.jpg"

if __name__ == '__main__':
    ncnn_model = YOLO(model_path, task="detect")
    results = ncnn_model(img_path)

    if not results:
        print("No detections found.")
    else:
        result = results[0]
        #results.show()
        result.save()

        for box in result.boxes:
            xyxy = box.xyxy[0].cpu().numpy()  # Get [xmin, ymin, xmax, ymax] format
            conf = box.conf
            cls = box.cls
            print(f"Bounding box coordinates: {xyxy}, Confidence: {conf}, Class: {cls}")