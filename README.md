# 🪔 Auto-Sketching Colorful Ganesh Chaturthi Animation in Python (Pygame) 🌺

An animated, procedural, and colorful digital art experience of **Lord Ganesha (Ganesh Ji)** created using **Python and Pygame** at **1280 × 720** resolution running at **60 FPS**.

Instead of displaying a static image, this project **auto-sketches Lord Ganesha dynamically stroke-by-stroke on your screen** with a glowing golden brush tip and flying sparks, followed by a radiant watercolor bloom of sacred colors!

---

## 🌟 Visual Highlights & Features

- ✍️ **Dynamic Auto-Sketching**: Watch Lord Ganesha get sketched live on screen stroke-by-stroke.
- ✨ **Sparkling Magic Brush**: A glowing white-gold pen tip moves along each curve, spraying micro-sparks and golden embers as it draws.
- 🎨 **Vibrant Sacred Color Palette**: Glowing lines drawn in temple gold, sacred saffron, lotus pink, and vermillion.
- 🌸 **Watercolor Color Bloom**: Once the sketch completes, soft glowing watercolor washes smoothly bloom underneath the sketch lines.
- 🪔 **4 Flickering Brass Diyas**: Traditional oil lamps in bottom corners with 3-tiered organic flickering flames casting dancing light across the floor.
- 🌺 **Falling Flower Petals**: 50+ falling petals (golden marigolds & sacred red roses) with natural 3D tumbling rotation and wind sway.
- 🔔 **Hanging Toran & Swaying Bells**: Festive mango leaves and marigold swags across the top with swinging brass temple bells.
- 🕉️ **Sacred Typography**: Large golden title **"Ganesh Chaturthi"** and **"॥ ॐ गं गणपतये नमः ॥"** with auspicious golden filigree dividers.
- 💫 **Breathing Animation Mode**: After sketching, Lord Ganesha breathes harmoniously with a gentle pulsating zoom ($scale = 1.0 + 0.015 \cdot \sin(t \cdot 1.8)$) and radiant divine sun-rays.

---

## 📁 Project Structure

```
Python DSA/
├── assets/
│   ├── ganesh_sketch.json  # Precomputed vector stroke curves (instant load)
│   └── ganesh.png          # High-resolution Lord Ganesha artwork (source)
├── 1st Lecture/
│   ├── assets/             # Mirrored assets for 1-click execution inside subfolder
│   └── GaneshJi.py         # Direct runner linked to main.py
├── main.py                 # Core auto-sketching engine & visual systems
├── requirements.txt        # Dependencies (pygame, opencv-python, pillow)
└── README.md               # Documentation and user guide
```

---

## 🚀 Quick Start Guide

### Step 1: Run the Project
You can run the animation using either of the following commands:

```powershell
python main.py
```

*Or run from the `1st Lecture` folder:*

```powershell
python "1st Lecture/GaneshJi.py"
```

*(You can also open [`main.py`](file:///e:/Python%20DSA/main.py) or [`1st Lecture/GaneshJi.py`](file:///e:/Python%20DSA/1st%20Lecture/GaneshJi.py) in VS Code and click the **▷ Run** button at the top-right).*

---

## 🎮 Keyboard Controls

| Key | Action |
|:---|:---|
| **`R`** | **Re-sketch**: Restart the auto-drawing animation from the beginning anytime |
| **`SPACE`** | **Pause / Resume** the sketch and animation |
| **`S`** | **Skip**: Finish the sketch instantly and jump straight to the completed artwork |
| **`F`** | **Toggle Fullscreen** mode |
| **`ESC`** | **Exit** the application gracefully |

---

**Ganpati Bappa Morya! मंगल मूर्ति मोरया!** 🌺🪔✨
