from utils import calculate_angle

class PushUpCounter:
    def __init__(self):
        self.count = 0
        self.state = "UP"  # 初始状态
        self.last_angle = 180

    def update(self, keypoints):
        # MediaPipe关键点索引（右臂）
        shoulder = keypoints[12]
        elbow = keypoints[14]
        wrist = keypoints[16]

        angle = calculate_angle(shoulder, elbow, wrist)

        # 状态机
        if angle < 90:
            self.state = "DOWN"

        if angle > 160 and self.state == "DOWN":
            self.state = "UP"
            self.count += 1

        self.last_angle = angle

    def draw(self, frame):
        import cv2
        cv2.putText(frame, f"PushUps: {self.count}",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)

        cv2.putText(frame, f"State: {self.state}",
                    (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 2)
        