import cv2

bilateralFilter_d = 15
bilateralFilter_sigma_color = 50
bilateralFilter_sigma_space = 50

def image_proc(data):
    data = cv2.resize( # 拡大処理
        data, (data.shape[1]*2, data.shape[0]*2), interpolation=cv2.INTER_LANCZOS4)
    gaussian = cv2.GaussianBlur(data, (0, 0), 10)
    data = cv2.addWeighted(data, 1.5, gaussian, -0.5, 0)
    data = cv2.bilateralFilter(data, 15, 50, 50) # ノイズ除去
    #data = cv2.fastNlMeansDenoisingColored(data, None, h=10, hColor=7, templateWindowSize=5, searchWindowSize=10)
    return data

if __name__ == "__main__":

    config = {}
    with open('config.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            key, value = line.split()
            config[key] = int(value)

    #カメラの設定 デバイスIDは1
    cap = cv2.VideoCapture(config["DEVICE"], cv2.CAP_DSHOW)
    bilateralFilter_d = config["BILATERAL_FILTER_D"]
    bilateralFilter_sigma_color = config["BILATERAL_FILTER_SIGMA_COLOR"]
    bilateralFilter_sigma_space = config["BILATERAL_FILTER_SIGMA_SPACE"]
    COMPARE_MODE = config["COMPARE_MODE"]
    print(COMPARE_MODE)

    #ループ
    while True:

        #カメラからの画像取得
        ret, frame = cap.read()
        h, w = frame.shape[:2]

        if COMPARE_MODE:
            frame2 = frame.copy()
            frame = image_proc(frame)
            h, w = frame.shape[:2]
            half_w = w // 2      # 幅の半分（整数値）

            frame2 = cv2.resize(frame2, (int(frame2.shape[1] * h / frame2.shape[0]), h))
            frame3 = cv2.hconcat([frame2[:, :half_w], frame[:, half_w:]])
            cv2.imshow('RBV2', frame3)
        else:
            frame = image_proc(frame)
            cv2.imshow('RBV2', frame) 

        #繰り返し分から抜けるためのif文
        key = cv2.waitKey(1)
        if key == 27:
            break

        if cv2.getWindowProperty('RBV2', cv2.WND_PROP_VISIBLE) < 1:
            break

    #メモリを解放して終了するためのコマンド
    cap.release()
    cv2.destroyAllWindows()
