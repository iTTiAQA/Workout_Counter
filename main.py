import cv2
from pose_estimator import PoseEstimator
from pushup_counter import PushUpCounter

VIDEO_PATH = "./test1.mp4"

def main():
    cap = cv2.VideoCapture(VIDEO_PATH)

    pose = PoseEstimator()
    counter = PushUpCounter()

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = 0

    # 设置视频保存参数
    output_path = "output_pushup_video.mp4"  # 输出文件路径
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 编码器，保存为mp4格式
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    # out = None  # 如果不需要保存视频，可以将其设置为None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # 关键点检测
        keypoints = pose.get_keypoints(frame)

        if keypoints is not None:
            counter.update(keypoints)

        # 可视化
        pose.draw(frame)
        counter.draw(frame)

        # 保存处理后的帧
        out.write(frame) if out else None

        cv2.imshow("Result", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    out.release() if out else None # 释放视频写入器
    cv2.destroyAllWindows()

    # 输出结果
    total_time = frame_count / fps
    print("====== 结果 ======")
    print(f"俯卧撑次数: {counter.count}")
    print(f"视频时长: {total_time:.2f}s")
    print(f"处理后的视频已保存为: {output_path}")

if __name__ == "__main__":
    main()