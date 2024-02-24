import cv2
import mediapipe as mp
import math

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

def _normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int,
    image_height: int):

  x_px = min(math.floor(normalized_x * image_width), image_width - 1)
  y_px = min(math.floor(normalized_y * image_height), image_height - 1)
  return x_px, y_px


def align_face(images):

  ## detect the face in image
  try:
    results_face = []
    with mp_face_detection.FaceDetection(
          model_selection=1, min_detection_confidence=0.5) as face_detection:
      for image in images:
        # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # mp_drawing.draw_detection(image, results.detections[0])
        image_rows, image_cols = image.shape[:-1]
        location = results.detections[0].location_data
        relative_bounding_box = location.relative_bounding_box

        x1, y1 = _normalized_to_pixel_coordinates(
          relative_bounding_box.xmin, relative_bounding_box.ymin, image_cols,
          image_rows)
        x2, y2 = _normalized_to_pixel_coordinates(
          relative_bounding_box.xmin + relative_bounding_box.width,
          relative_bounding_box.ymin + relative_bounding_box.height, image_cols,
          image_rows)
        pady1, pady2, padx1, padx2 = [0, 10, 0, 0]
        # y1 = max(0, y1 - pady1)
        # y2 = min(image.shape[0], y2 + pady2)
        # x1 = max(0, x1 - padx1)
        # x2 = min(image.shape[1], x2 + padx2)
        results_face.append([image[y1:y2, x1:x2], [y1, y2, x1, x2]])

    return results_face
  except Exception as e:
    print("Something went wrong in detecting face", e)
    return []
          
