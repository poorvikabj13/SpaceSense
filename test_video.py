import cv2
import glob
import numpy as np

# Path to UCSD frames
image_folder = r"C:\Users\poorv\OneDrive\Desktop\SpaceSense\dataset\UCSD_Anomaly_Dataset.v1p2\UCSDped1\Train\Train001\*"

images = sorted(glob.glob(image_folder))
print("Total frames found:", len(images))

# Background subtractor
bg = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=25)

for img_path in images:
    frame = cv2.imread(img_path)
    if frame is None:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fg_mask = bg.apply(gray)

    # Clean mask
    fg_mask = cv2.medianBlur(fg_mask, 5)

    contours, _ = cv2.findContours(
        fg_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    anomaly_score = 0

    for c in contours:
        area = cv2.contourArea(c)

        # Ignore small noise
        if area > 200:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Score proportional to abnormal motion size
            anomaly_score += int(area / 100)

    # Cap score for readability
    anomaly_score = min(anomaly_score, 100)

    # Display score
    cv2.putText(
        frame,
        f"Anomaly Score: {anomaly_score}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    cv2.imshow("SpaceSense – Crowd Anomaly Detection", frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
