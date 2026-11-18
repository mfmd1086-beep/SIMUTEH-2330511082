"""praproses.py: rangkaian praproses SIMUTEH."""
import json
import cv2
import numpy as np

PARAM_BAWAAN = {"lebar": 640, "gamma": "auto", "clahe_clip": 1.0, "clahe_tile": 4,
    "clahe_otomatis": True, "batas_tidak_rata": 0.65, "penapis": "median",
    "kernel": 3, "sigma": 1.0, "tajam_k": 0.0}

def gamma_otomatis(img_bgr):
    v = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)[:, :, 2]
    if v.mean() > 210:
        return 1.6
    if v.std() < 20:
        return 1.0
    if np.percentile(v, 95) < 200:
        return 0.6
    return 1.0

def indeks_tidak_rata(img_bgr):
    v = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)[:, :, 2].astype(float)
    h, w = v.shape
    blok = [np.percentile(v[i*h//4:(i+1)*h//4, j*w//4:(j+1)*w//4], 90)
            for i in range(4) for j in range(4)]
    return (max(blok) - min(blok)) / np.mean(blok)

def praproses(img_bgr, p=None):
    p = {**PARAM_BAWAAN, **(p or {})}
    h, w = img_bgr.shape[:2]
    img = cv2.resize(img_bgr, (p["lebar"], int(round(h * p["lebar"] / w))), interpolation=cv2.INTER_AREA)
    g = gamma_otomatis(img) if p["gamma"] == "auto" else float(p["gamma"])
    if g != 1.0:
        lut = np.array([255 * (i / 255) ** g for i in range(256)])
        img = cv2.LUT(img, lut.clip(0, 255).astype(np.uint8))
    pakai_clahe = p["clahe_clip"] > 0
    if pakai_clahe and p["clahe_otomatis"]:
        pakai_clahe = indeks_tidak_rata(img) > p["batas_tidak_rata"]
    if pakai_clahe:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        clahe = cv2.createCLAHE(clipLimit=p["clahe_clip"], tileGridSize=(p["clahe_tile"], p["clahe_tile"]))
        hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    k = p["kernel"]
    if p["penapis"] == "rerata":
        img = cv2.blur(img, (k, k))
    elif p["penapis"] == "gaussian":
        img = cv2.GaussianBlur(img, (k, k), p["sigma"])
    elif p["penapis"] == "median":
        img = cv2.medianBlur(img, k)
    if p["tajam_k"] > 0:
        blur = cv2.GaussianBlur(img, (5, 5), 1.0)
        img = cv2.addWeighted(img, 1 + p["tajam_k"], blur, -p["tajam_k"], 0)
    return img

def simpan_param(p, path="../hasil/param_praproses.json"):
    with open(path, "w") as f:
        json.dump({**PARAM_BAWAAN, **p}, f, indent=2)
