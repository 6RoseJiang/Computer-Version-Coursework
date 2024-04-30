import cv2

def stitch_frames(frames):
    # Use OpenCV's Stitcher class
    stitcher = cv2.Stitcher_create()
    status, stitched = stitcher.stitch(frames)

    if status == cv2.Stitcher_OK:
        return True, stitched
    else:
        return False, None

# Implement white balance
def auto_white_balance(img):
    result = cv2.xphoto.createSimpleWB().balanceWhite(img)
    return result

# Enhance contrast
def enhance_contrast(img):
    # Convert to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # Apply CLAHE to the L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)

    # Merge channels
    lab = cv2.merge((l, a, b))
    enhanced_img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    return enhanced_img

# Process each frame for white balance and contrast enhancement
def process_frame(frame):
    wb_frame = auto_white_balance(frame)
    enhanced_frame = enhance_contrast(wb_frame)
    return enhanced_frame

# Crop the center of the image
def crop_center(img, percent=0.7):
    # Ensure the cropping percentage is reasonable
    if percent <= 0 or percent > 1:
        return img

    height, width = img.shape[:2]
    new_width = int(width * percent)
    new_height = int(height * percent)

    # Calculate the starting points for cropping
    start_x = (width - new_width) // 2
    start_y = (height - new_height) // 2

    # Crop the image
    cropped_img = img[start_y:start_y + new_height, start_x:start_x + new_width]

    return cropped_img

def main(video_path, frame_ratio=0.1):
    cap = cv2.VideoCapture(video_path)
    frames = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_step = max(1, int(total_frames * frame_ratio))

    print(f"Total frames: {total_frames}, Frame step: {frame_step}")

    current_frame = 0
    while current_frame < total_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        ret, frame = cap.read()
        if not ret:
            break
        processed_frame = process_frame(frame)
        frames.append(processed_frame)
        current_frame += frame_step

    success, panorama = stitch_frames(frames)
    if success:
        # Crop the center 70% of the image
        cropped_panorama = crop_center(panorama, percent=0.7)

        # Save the cropped panorama
        cv2.imwrite('panorama.jpg', cropped_panorama)
        print("The panorama has been saved as 'panorama.jpg'")

if __name__ == "__main__":
    #Here to change the video
    main("video1.mp4")
