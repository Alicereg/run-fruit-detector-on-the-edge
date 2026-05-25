import time
import cv2
import requests
from tkinter import Tk
from tkinter.filedialog import askopenfilename

URL = "http://localhost/image"

# ==========================================
# DISPLAY NAMES
# ==========================================

display_names = {
    "ripebanana": "Ripe Banana",
    "unripebanana": "Unripe Banana",
    "rottenbanana": "Rotten Banana",

    "ripeorange": "Ripe Orange",
    "unripeorange": "Unripe Orange",
    "rottenorange": "Rotten Orange",

    "ripeoranges": "Ripe Orange",
    "unripeoranges": "Unripe Orange",
    "rottenoranges": "Rotten Orange"
}

# ==========================================
# COLOR FUNCTION
# ==========================================

def get_color(tag):

    tag = tag.lower()

    if "rotten" in tag:
        return (0, 0, 255)      # Red

    elif "unripe" in tag:
        return (0, 255, 255)    # Yellow

    elif "ripe" in tag:
        return (0, 255, 0)      # Green

    return (255, 255, 255)

# ==========================================
# MENU
# ==========================================

print("=== Fruit Detector Edge AI ===")
print("1. Use Webcam")
print("2. Use Image File")

choice = input("Choose option (1 or 2): ")

# ==========================================
# OPTION 1 - WEBCAM
# ==========================================

if choice == "1":

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    prediction_text = "Press S to Scan"

    text_color = (255, 255, 255)

    print("Press S to scan fruit")
    print("Press Q to quit")

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        # Show prediction text
        cv2.putText(
            frame,
            prediction_text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            text_color,
            2
        )

        cv2.imshow("Fruit Detector", frame)

        key = cv2.waitKey(1)

        # ======================================
        # PRESS S TO SCAN
        # ======================================

        if key == ord('s'):

            image_path = "capture.jpg"

            cv2.imwrite(image_path, frame)

            with open(image_path, "rb") as img:

                start = time.time()

                response = requests.post(
                    URL,
                    data=img,
                    headers={"Content-Type": "image/jpeg"}
                )

                end = time.time()

            prediction_time = round(end - start, 3)

            result = response.json()

            predictions = result["predictions"]

            best_prediction = max(
                predictions,
                key=lambda x: x["probability"]
            )

            raw_tag = best_prediction["tagName"]
            probability = best_prediction["probability"]

            # Pretty name
            tag = display_names.get(raw_tag, raw_tag)

            # Threshold
            if probability < 0.70:

                prediction_text = "Uncertain Prediction"

                text_color = (0, 165, 255)

            else:

                prediction_text = (
                    f"{tag}: {probability:.2%} "
                    f"| Edge: {prediction_time}s"
                )

                text_color = get_color(raw_tag)

            print(prediction_text)

        # ======================================
        # PRESS Q TO QUIT
        # ======================================

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# ==========================================
# OPTION 2 - IMAGE FILE
# ==========================================

elif choice == "2":

    # Hide tkinter window
    Tk().withdraw()

    # Open file explorer
    file_path = askopenfilename(
        title="Select fruit image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

    if not file_path:
        print("No image selected")
        exit()

    # Send image to model
    with open(file_path, "rb") as img:

        start = time.time()

        response = requests.post(
            URL,
            data=img,
            headers={"Content-Type": "image/jpeg"}
        )

        end = time.time()

    prediction_time = round(end - start, 3)

    result = response.json()

    predictions = result["predictions"]

    best_prediction = max(
        predictions,
        key=lambda x: x["probability"]
    )

    raw_tag = best_prediction["tagName"]
    probability = best_prediction["probability"]

    # Pretty label
    tag = display_names.get(raw_tag, raw_tag)

    # Threshold
    if probability < 0.70:

        prediction_text = "Uncertain Prediction"

        text_color = (0, 165, 255)

    else:

        prediction_text = (
            f"{tag}: {probability:.2%} "
            f"| Edge: {prediction_time}s"
        )

        text_color = get_color(raw_tag)

    # Terminal output
    print("\nPrediction Result")
    print("-------------------")
    print(f"Class: {tag}")
    print(f"Confidence: {probability:.2%}")
    print(f"Edge Prediction Time: {prediction_time}s")

    # Show image
    image = cv2.imread(file_path)

    cv2.putText(
        image,
        prediction_text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        text_color,
        2
    )

    cv2.imshow("Prediction", image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# ==========================================
# INVALID OPTION
# ==========================================

else:
    print("Invalid option")
