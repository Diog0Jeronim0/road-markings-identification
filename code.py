import cv2
import numpy as np

input_video = "video4.mp4"

def region_of_interest(image):
    height, width = image.shape[:2]
    polygon = np.array([
        [(0, height), (width, height), (width, int(height * 0.6)), (0, int(height * 0.6))]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, [polygon], 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def process_lines(lines, frame_shape):
    if lines is None:
        return []
    filtered_lines = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            # Filtrar linhas baseadas em inclinação e comprimento
            if abs(y2 - y1) / abs(x2 - x1) > 0.5:
                length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                if length > frame_shape[1] * 0.2:  # linhas devem ter pelo menos 20% da largura da imagem
                    filtered_lines.append(line)
    return filtered_lines

def vid_inf(vid_path):
    cap = cv2.VideoCapture(vid_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_size = (frame_width, frame_height)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output_video = "output_recorded.mp4"
    out = cv2.VideoWriter(output_video, fourcc, fps, frame_size)

    if not cap.isOpened():
        print("Erro ao abrir o arquivo de vídeo")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Filtra por cores para destacar linhas amarelas e brancas
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask_yellow = cv2.inRange(hsv, (20, 100, 100), (30, 255, 255))  # Ajustar conforme necessário
            mask_white = cv2.inRange(hsv, (0, 0, 200), (180, 25, 255))      # Ajustar conforme necessário
            mask_lane = cv2.bitwise_or(mask_yellow, mask_white)
            edges = cv2.Canny(mask_lane, 100, 200)
            roi = region_of_interest(edges)

            lines = cv2.HoughLinesP(roi, 1, np.pi/180, 50, minLineLength=50, maxLineGap=200)
            valid_lines = process_lines(lines, frame.shape)

            frame_out = frame.copy()
            if valid_lines:
                for line in valid_lines:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(frame_out, (x1, y1), (x2, y2), (0, 255, 0), 10)

            out.write(frame_out)
            cv2.imshow("Resultado", frame_out)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

vid_inf(input_video)
