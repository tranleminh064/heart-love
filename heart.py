import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap

# ── 1. Parametric heart curve ──────────────────────────────────────────────
t = np.linspace(0, 2 * np.pi, 1000)
x = 16 * np.sin(t) ** 3
y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)

# ── 2. Fill heart with gradient effect using scatter ──────────────────────
# Generate random points inside bounding box, keep those inside the heart
np.random.seed(7)
n_fill = 8000
rx = np.random.uniform(-17, 17, n_fill)
ry = np.random.uniform(-14, 13, n_fill)

# Point-in-heart test via parametric inequality
def in_heart(px, py):
    return (px**2 + (py - (13/16) * px**(2/3))**2) <= 0   # fallback to winding

# Use the fill polygon mask via matplotlib Path
from matplotlib.path import Path
heart_path = Path(np.column_stack([x, y]))
mask = heart_path.contains_points(np.column_stack([rx, ry]))
fx, fy = rx[mask], ry[mask]

# Color by distance from center for gradient effect
dist = np.sqrt(fx**2 + fy**2)
dist_norm = (dist - dist.min()) / (dist.max() - dist.min())

# ── 3. Plot ───────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 6.5))
fig.patch.set_facecolor("#1a0010")
ax.set_facecolor("#1a0010")

# Gradient fill (inner bright → outer deep red)
cmap = LinearSegmentedColormap.from_list(
    "heart", ["#ff6b9d", "#ff1744", "#b71c1c", "#7f0000"]
)
sc = ax.scatter(fx, fy, c=dist_norm, cmap=cmap,
                s=2.5, alpha=0.75, linewidths=0, zorder=2)

# Glowing border — multiple passes with decreasing alpha
for lw, alpha in [(6, 0.15), (3.5, 0.3), (2, 0.7), (1, 1.0)]:
    ax.plot(x, y, color="#ff6b9d", linewidth=lw, alpha=alpha, zorder=3)

# Sparkle dots on the outline
np.random.seed(3)
idx = np.random.choice(len(t), 18, replace=False)
ax.scatter(x[idx], y[idx], color="white", s=18, zorder=5, alpha=0.9)

# Centre highlight
ax.scatter([0], [2], color="white", s=120, alpha=0.25, zorder=4)
ax.scatter([0], [2], color="white", s=30,  alpha=0.6,  zorder=4)

# Text
ax.text(0, -16.5, "♥  Made with Python  ♥",
        ha="center", va="center", fontsize=13,
        color="#ff6b9d", fontfamily="monospace", alpha=0.9)

# Clean up axes
ax.set_xlim(-20, 20)
ax.set_ylim(-18, 15)
ax.set_aspect("equal")
ax.axis("off")

plt.tight_layout()
plt.savefig("heart.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.show()
print("Đã lưu: heart.png")
