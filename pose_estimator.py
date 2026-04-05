import cv2
import mediapipe as mp

class PoseEstimator:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def get_keypoints(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(rgb)

        if not self.results.pose_landmarks:
            return None

        keypoints = []
        for lm in self.results.pose_landmarks.landmark:
            keypoints.append((lm.x, lm.y))

        return keypoints

    def draw(self, frame):
        if self.results and self.results.pose_landmarks:
            self.mp_draw.draw_landmarks(
                frame,
                self.results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )
            