import os
import pandas as pd
import cv2
import torch
from ultralytics import YOLO

class VehicleCounter:
    def __init__(self, model_path='yolov8s.pt', device=None):
        self.device = device if device else 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = YOLO(model_path).to(self.device)

    def draw_boxes_and_count(self, img, results, confidence_threshold):
        car_count = 0
        truck_count = 0
        bus_count = 0
        motorcycle_count = 0
        axle_counts = {'2_axles': 0, '3_axles': 0, '4_axles': 0, '5_axles': 0}

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]
                label = result.names[int(box.cls[0])]
                
                if confidence >= confidence_threshold:
                    if label in ['car', 'truck', 'bus', 'motorcycle']:
                        if label == 'car':
                            car_count += 1
                        elif label == 'truck':
                            truck_count += 1
                        elif label == 'bus':
                            bus_count += 1
                        elif label == 'motorcycle':
                            motorcycle_count += 1

                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(img, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    if label in axle_counts:
                        axle_counts[label] += 1
        
        return car_count, truck_count, bus_count, motorcycle_count, axle_counts

    def process_video(self, video_path, output_folder, frame_skip=15, show_video=True, resolution=(640, 480), confidence_threshold=0.5, output_format='xlsx', show_frame=None, update_counts=None):
        total_car_count = 0
        total_truck_count = 0
        total_bus_count = 0
        total_motorcycle_count = 0
        total_axle_counts = {'2_axles': 0, '3_axles': 0, '4_axles': 0, '5_axles': 0}
        
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

        frame_number = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_number += 1
            
            if frame_number % frame_skip != 0:
                continue
            
            results = self.model(frame, device=self.device)
            car_count, truck_count, bus_count, motorcycle_count, axle_counts = self.draw_boxes_and_count(frame, results, confidence_threshold)
            
            total_car_count += car_count
            total_truck_count += truck_count
            total_bus_count += bus_count
            total_motorcycle_count += motorcycle_count
            for key in total_axle_counts:
                total_axle_counts[key] += axle_counts[key]
            
            if show_video and show_frame:
                show_frame(frame)
            if update_counts:
                update_counts(total_car_count, total_truck_count, total_bus_count, total_motorcycle_count)

        cap.release()
        cv2.destroyAllWindows()

        total_vehicles = total_car_count + total_truck_count + total_bus_count + total_motorcycle_count
        final_counts = pd.DataFrame([{
            'Car': total_car_count,
            'Truck': total_truck_count,
            'Bus': total_bus_count,
            'Motorcycle': total_motorcycle_count,
            'Total_Vehicles': total_vehicles,
            '2_Axles': total_axle_counts['2_axles'],
            '3_Axles': total_axle_counts['3_axles'],
            '4_Axles': total_axle_counts['4_axles'],
            '5_Axles': total_axle_counts['5_axles']
        }])

        video_filename = os.path.basename(video_path)
        video_name_without_extension = os.path.splitext(video_filename)[0]
        excel_filename = f"{video_name_without_extension}.{output_format}"
        if output_format == 'xlsx':
            final_counts.to_excel(os.path.join(output_folder, excel_filename), index=False)
        else:
            final_counts.to_csv(os.path.join(output_folder, excel_filename), index=False)

        return excel_filename