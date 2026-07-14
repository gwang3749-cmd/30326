import os
import csv
import random

def generate_mock_data(data_path):
    """
    간단한 mock traffic_hour.csv 생성:
    - 컬럼: hour, region, traffic_count
    - 시간: 0~23, regions: Jungbu-dong, Beomeo-ri
    """
    os.makedirs(data_path, exist_ok=True)
    filename = os.path.join(data_path, "traffic_hour.csv")
    regions = ["Jungbu-dong", "Beomeo-ri"]
    
    with open(filename, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["hour", "region", "traffic_count"])
        for hour in range(24):
            for region in regions:
                # 대충의 교통량 패턴: 출퇴근 시간대 증대
                base = 100
                if 7 <= hour <= 9 or 17 <= hour <= 19:
                    base += 200
                count = base + random.randint(-30, 30) + (50 if region == "Jungbu-dong" else 0)
                writer.writerow([hour, region, max(0, count)])
    return filename
