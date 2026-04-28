import numpy as np
import matplotlib.pyplot as plt

def cartesian_to_axial(x, y, size):
    q = (np.sqrt(3)/3 * x - 1/3 * y) / size
    r = (2/3 * y) / size
    return q, r

def hex_distance(q, r):
    return (abs(q) + abs(r) + abs(q + r)) / 2

def hexbin_with_hex_clip(x, y, gridsize=40, radius=5, cmap='viridis'):

    # 1. Create hexbin ONCE
    fig, ax = plt.subplots(figsize=(6, 5))
    hb = ax.hexbin(x, y, gridsize=gridsize, cmap=cmap)
    
    centers = hb.get_offsets()
    counts = hb.get_array()

    if len(centers) == 0:
        print("No hexagons created.")
        return

    # 2. Estimate hex size from center spacing
    if len(centers) > 1:
        diffs = centers[1:] - centers[:-1]
        dists = np.linalg.norm(diffs, axis=1)
        hex_size = np.median(dists)
    else:
        hex_size = 1.0

    # 3. Convert centers to axial coords
    q, r = cartesian_to_axial(centers[:, 0], centers[:, 1], hex_size)

    # 4. Compute mask
    mask = hex_distance(q, r) <= radius

    # 5. Apply mask to the EXISTING hexbin
    clipped = counts.copy()
    clipped[~mask] = 0

    # 6. Replace the hexbin's internal data
    hb.set_array(clipped)

    # 7. Redraw
    plt.colorbar(hb, ax=ax, label="Counts")
    ax.set_title(f"Hexbin clipped to radius {radius}")
    plt.tight_layout()
    plt.show()

hexbin_with_hex_clip(np.random.randn(1000), np.random.randn(1000), gridsize=30, radius=3)
