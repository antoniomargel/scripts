import os
import cv2
import numpy as np
from skimage.morphology import skeletonize
from skimage.util import invert

# Define the root path relative to the script location
root_path = os.path.join(os.path.dirname(__file__), 'png_txt')
train_folders = [f"figs_{i}" for i in range(6)]
test_folders = [f"figs_{i}" for i in range(6, 8)]

# Helper functions
def load_image_pairs(folders):
    image_pairs = []
    for folder in folders:
        folder_path = os.path.join(root_path, folder)
        for filename in os.listdir(folder_path):
            if filename.startswith("f") and filename.endswith(".png"):
                pair_id = filename[1:]
                reference_path = os.path.join(folder_path, filename)
                subject_path = os.path.join(folder_path, f"s{pair_id}")
                if os.path.exists(subject_path):
                    image_pairs.append((reference_path, subject_path))
    return image_pairs

def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    binary_image = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    return binary_image

# Updated skeletonize_image function with more debugging
def skeletonize_image(binary_image, output_dir, img_id):
    # Save the binary image for verification
    binary_output_path = os.path.join(output_dir, f"binary_image_{img_id}.png")
    cv2.imwrite(binary_output_path, binary_image)
    
    # Normalize binary image for skeletonization (0 and 1 format)
    normalized_image = (binary_image // 255).astype(np.uint8)
    
    # Try cv2.ximgproc thinning (if available)
    try:
        skeleton = cv2.ximgproc.thinning(normalized_image, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
    except AttributeError:
        print("cv2.ximgproc not available. Switching to skimage skeletonize.")
        skeleton = skeletonize(normalized_image)  # Fallback to skimage
    
    # Convert skeleton back to 255 format for visualization
    skeleton_image = (skeleton * 255).astype('uint8')
    
    # Save the skeletonized image for verification
    skeleton_output_path = os.path.join(output_dir, f"skeleton_image_{img_id}.png")
    cv2.imwrite(skeleton_output_path, skeleton_image)
    
    return skeleton_image

def get_minutiae_points(skeleton):
    minutiae_points = []
    rows, cols = skeleton.shape
    for x in range(1, rows - 1):
        for y in range(1, cols - 1):
            if skeleton[x, y] == 255:
                neighborhood = skeleton[x-1:x+2, y-1:y+2]
                white_pixels = np.sum(neighborhood == 255)
                if white_pixels == 2:
                    minutiae_points.append((x, y, 'ending'))
                elif white_pixels == 4:
                    minutiae_points.append((x, y, 'bifurcation'))
    return minutiae_points

# Main function
def main():
    # Load TRAIN and TEST sets
    train_image_pairs = load_image_pairs(train_folders)
    test_image_pairs = load_image_pairs(test_folders)
    print(f"Loaded {len(train_image_pairs)} TRAIN pairs and {len(test_image_pairs)} TEST pairs.")

    output_dir = "skeletonized_pairs"
    os.makedirs(output_dir, exist_ok=True)

    # Example processing of the TRAIN set
    for i, (ref_path, subj_path) in enumerate(train_image_pairs[:5]):  # limit to 5 pairs for demonstration
        # Preprocess
        ref_binary = preprocess_image(ref_path)
        subj_binary = preprocess_image(subj_path)

        # Save binary images for verification
        binary_output_path = os.path.join(output_dir, f"binary_image_{i+1}.png")
        cv2.imwrite(binary_output_path, ref_binary)

        
        # Skeletonize
        ref_skeleton = skeletonize_image(ref_binary)
        subj_skeleton = skeletonize_image(subj_binary)

        ref_output_path = os.path.join(output_dir, f"ref_skeleton_{i+1}.png")
        subj_output_path = os.path.join(output_dir, f"subj_skeleton_{i+1}.png")

        cv2.imwrite(ref_output_path, ref_skeleton)
        cv2.imwrite(subj_output_path, subj_skeleton)
        
        # Extract minutiae
        # ref_minutiae = get_minutiae_points(ref_skeleton)
        # subj_minutiae = get_minutiae_points(subj_skeleton)
        
        # Output example minutiae counts for debugging
        #print(f"Reference: {ref_path} - Minutiae points: {len(ref_minutiae)}")
        #print(f"Subject: {subj_path} - Minutiae points: {len(subj_minutiae)}\n")

# Entry point for script
if __name__ == "__main__":
    main()
