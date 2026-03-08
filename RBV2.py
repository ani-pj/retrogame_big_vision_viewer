import cv2
import time
import sys

bilateralFilter_d = 15
bilateralFilter_sigma_color = 50
bilateralFilter_sigma_space = 50

def image_proc(data, RESIZE_INTERPOLATION):
    # t2 = time.time()
    gaussian = cv2.GaussianBlur(data, (0, 0), 10)
    data = cv2.addWeighted(data, 1.5, gaussian, -0.5, 0)
    # t3 = time.time()
    data = cv2.bilateralFilter(data, 15, 50, 50) # ノイズ除去
    # t4 = time.time()
    data = cv2.resize( # 拡大処理
        data, (data.shape[1]*2, data.shape[0]*2), interpolation=RESIZE_INTERPOLATION)
    # t5 = time.time()
    # print("シャープ化処理：", (t3-t2)*1000, "[ms], ノイズ除去：", (t4-t3)*1000, "[ms], 拡大処理：", (t5-t4)*1000, "[ms]")


    return data

if __name__ == "__main__":

    config = {}
    with open('config.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            key, value = line.split()
            try:
                config[key] = int(value)
            except:
                config[key] = str(value)

    print(config)

    prev_time = 0
    fps = 0

    #カメラの設定 デバイスIDは1
    cap = cv2.VideoCapture(config["DEVICE"], cv2.CAP_DSHOW)
    bilateralFilter_d = config["BILATERAL_FILTER_D"]
    bilateralFilter_sigma_color = config["BILATERAL_FILTER_SIGMA_COLOR"]
    bilateralFilter_sigma_space = config["BILATERAL_FILTER_SIGMA_SPACE"]

    COMPARE_MODE = config["COMPARE_MODE"]
    FPS_VIEW = config["FPS_VIEW"]

    RESIZE_INTERPOLATION = None
    if config["RESIZE_INTERPOLATION"] == "INTER_NEAREST":
        RESIZE_INTERPOLATION = cv2.INTER_NEAREST
    elif config["RESIZE_INTERPOLATION"] == "INTER_LINEAR":
        RESIZE_INTERPOLATION = cv2.INTER_LINEAR
    elif config["RESIZE_INTERPOLATION"] == "INTER_CUBIC":
        RESIZE_INTERPOLATION = cv2.INTER_CUBIC
    elif config["RESIZE_INTERPOLATION"] == "INTER_AREA":
        RESIZE_INTERPOLATION = cv2.INTER_AREA
    elif config["RESIZE_INTERPOLATION"] == "INTER_LANCZOS4":
        RESIZE_INTERPOLATION = cv2.INTER_LANCZOS4
    elif config["RESIZE_INTERPOLATION"] == "INTER_LINEAR_EXACT":
        RESIZE_INTERPOLATION = cv2.INTER_LINEAR_EXACT
    elif config["RESIZE_INTERPOLATION"] == "INTER_NEAREST_EXACT":
        RESIZE_INTERPOLATION = cv2.INTER_NEAREST_EXACT
    else:
        RESIZE_INTERPOLATION = cv2.INTER_CUBIC

    #ループ
    while True:
        start_time = time.time()

        #カメラからの画像取得
        ret, frame = cap.read()
        h, w = frame.shape[:2]

        if COMPARE_MODE:
            frame2 = frame.copy()
            frame = image_proc(frame, RESIZE_INTERPOLATION)
            h, w = frame.shape[:2]
            half_w = w // 2      # 幅の半分（整数値）

            frame2 = cv2.resize(frame2, (int(frame2.shape[1] * h / frame2.shape[0]), h))
            display_frame = cv2.hconcat([frame2[:, :half_w], frame[:, half_w:]])

        else:
            display_frame = image_proc(frame, RESIZE_INTERPOLATION)

        if FPS_VIEW:
            current_time = time.time()
            delta_time = current_time - prev_time
            if delta_time > 0:
                fps = 1 / delta_time
            prev_time = current_time
            # 画面にFPSを描画 (テキスト, 座標, フォント, スケール, 色, 太さ)
            cv2.putText(display_frame, f"FPS: {fps:.2f}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

        cv2.imshow('RBV2', display_frame)

        #繰り返し分から抜けるためのif文
        key = cv2.waitKey(1)
        if key == 27:
            break

        if cv2.getWindowProperty('RBV2', cv2.WND_PROP_VISIBLE) < 1:
            break

    #メモリを解放して終了するためのコマンド
    cap.release()
    cv2.destroyAllWindows()
