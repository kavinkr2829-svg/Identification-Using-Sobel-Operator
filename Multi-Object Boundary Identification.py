"""
Project 7 — Multi-Object Boundary Identification
Detects object boundaries using the Sobel operator and analyzes
the effect of Gaussian pre-smoothing.

Requirements:
    pip install opencv-python numpy matplotlib

Usage:
    python sobel_boundary_app.py --image path/to/image.jpg
    python sobel_boundary_app.py --image objects.jpg --sigma 1 2 3 4
"""

import argparse
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# 1. Sobel boundary detection
# ----------------------------------------------------------------------
def sobel_boundaries(gray):
    """
    Compute Sobel gradient magnitude and direction.

    Returns
    -------
    gx, gy : float arrays (horizontal / vertical derivatives)
    magnitude : uint8 array (0-255)
    direction : float array (radians)
    """
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    magnitude = np.sqrt(gx ** 2 + gy ** 2)
    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    magnitude = magnitude.astype(np.uint8)

    direction = np.arctan2(gy, gx)
    return gx, gy, magnitude, direction


# ----------------------------------------------------------------------
# 2. Threshold + morphological cleanup
# ----------------------------------------------------------------------
def clean_boundaries(magnitude, thresh=80, kernel_size=3):
    """
    Threshold the gradient magnitude and clean it morphologically
    so that only significant object boundaries remain.
    """
    _, binary = cv2.threshold(magnitude, thresh, 255, cv2.THRESH_BINARY)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
    return binary, closed


# ----------------------------------------------------------------------
# 3. Quantitative metrics
# ----------------------------------------------------------------------
def edge_density(magnitude, thresh=50):
    """Fraction of pixels above threshold (proxy for edge density)."""
    return float(np.sum(magnitude > thresh)) / magnitude.size


def noise_estimate(magnitude):
    """Mean magnitude in the lowest 20% of pixels — approximates noise."""
    flat = magnitude.flatten()
    cutoff = np.percentile(flat, 20)
    return float(np.mean(flat[flat <= cutoff]))


# ----------------------------------------------------------------------
# 4. Main pipeline
# ----------------------------------------------------------------------
def run_pipeline(image_path,
                 sigmas=(1, 2, 4),
                 thresh=80,
                 save_dir="output"):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    os.makedirs(save_dir, exist_ok=True)

    # --- Load & prepare ---
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Resize for consistent visualization (preserve aspect ratio)
    h, w = img.shape[:2]
    scale = min(800 / w, 600 / h, 1.0)
    img = cv2.resize(img, (int(w * scale), int(h * scale)))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(save_dir, "00_original.png"), img)

    # --- Sobel on raw image ---
    gx_raw, gy_raw, mag_raw, dir_raw = sobel_boundaries(gray)
    bin_raw, clean_raw = clean_boundaries(mag_raw, thresh)

    cv2.imwrite(os.path.join(save_dir, "01_sobel_raw_mag.png"), mag_raw)
    cv2.imwrite(os.path.join(save_dir, "02_sobel_raw_binary.png"), bin_raw)
    cv2.imwrite(os.path.join(save_dir, "03_sobel_raw_clean.png"), clean_raw)

    # --- Gaussian + Sobel for each sigma ---
    results = {}
    for sigma in sigmas:
        blurred = cv2.GaussianBlur(gray, (0, 0), sigma)
        gx_b, gy_b, mag_b, dir_b = sobel_boundaries(blurred)
        bin_b, clean_b = clean_boundaries(mag_b, thresh)

        results[sigma] = {
            "blurred": blurred,
            "gx": gx_b,
            "gy": gy_b,
            "mag": mag_b,
            "dir": dir_b,
            "binary": bin_b,
            "clean": clean_b,
        }

        cv2.imwrite(os.path.join(save_dir, f"04_gauss_s{sigma}_blur.png"), blurred)
        cv2.imwrite(os.path.join(save_dir, f"05_gauss_s{sigma}_mag.png"), mag_b)
        cv2.imwrite(os.path.join(save_dir, f"06_gauss_s{sigma}_binary.png"), bin_b)
        cv2.imwrite(os.path.join(save_dir, f"07_gauss_s{sigma}_clean.png"), clean_b)

    # --- Quantitative report ---
    print("\n========== Quantitative Report ==========")
    print(f"{'Pipeline':<28}{'Edge density':>15}{'Noise est.':>15}")
    print("-" * 58)
    print(f"{'Raw + Sobel':<28}{edge_density(mag_raw):>15.4f}"
          f"{noise_estimate(mag_raw):>15.2f}")
    for sigma in sigmas:
        m = results[sigma]["mag"]
        print(f"{'Gaussian σ=' + str(sigma) + ' + Sobel':<28}"
              f"{edge_density(m):>15.4f}{noise_estimate(m):>15.2f}")
    print("=" * 58 + "\n")

    # ------------------------------------------------------------------
    # 5. Visualization (magnitude comparison)
    # ------------------------------------------------------------------
    cols = 2 + len(sigmas)
    fig, axes = plt.subplots(2, cols, figsize=(4 * cols, 8))

    axes[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title("Original")
    axes[1, 0].axis("off")

    axes[0, 1].imshow(mag_raw, cmap="gray")
    axes[0, 1].set_title("Sobel (raw)")
    axes[1, 1].imshow(clean_raw, cmap="gray")
    axes[1, 1].set_title("Sobel (raw) + cleanup")

    for i, sigma in enumerate(sigmas, start=2):
        axes[0, i].imshow(results[sigma]["mag"], cmap="gray")
        axes[0, i].set_title(f"Gaussian σ={sigma} + Sobel")
        axes[1, i].imshow(results[sigma]["clean"], cmap="gray")
        axes[1, i].set_title(f"σ={sigma} + Sobel + cleanup")

    for ax in axes.ravel():
        ax.axis("off")

    plt.suptitle("Multi-Object Boundary Identification — Sobel vs Gaussian+Sobel",
                 fontsize=14)
    plt.tight_layout()
    out_fig = os.path.join(save_dir, "comparison.png")
    plt.savefig(out_fig, dpi=120)
    plt.show()
    print(f"Visualization saved to: {out_fig}")

    return {
        "original": img,
        "gray": gray,
        "raw": {"gx": gx_raw, "gy": gy_raw, "mag": mag_raw,
                "binary": bin_raw, "clean": clean_raw},
        "gaussian": results,
    }


# ----------------------------------------------------------------------
# 6. CLI
# ----------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(
        description="Multi-Object Boundary Identification with Sobel + Gaussian")
    p.add_argument("--image", required=True, help="Path to input image")
    p.add_argument("--sigma", nargs="+", type=float, default=[1, 2, 4],
                   help="Gaussian sigma values (default: 1 2 4)")
    p.add_argument("--thresh", type=int, default=80,
                   help="Threshold for binary boundary map (default: 80)")
    p.add_argument("--out", default="output",
                   help="Output directory (default: output)")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(
        image_path=args.image,
        sigmas=tuple(args.sigma),
        thresh=args.thresh,
        save_dir=args.out,
    )