# QR Code Generator with Embedded Logo

This repository contains a small Python utility for generating high-resolution QR codes with an embedded center logo. It uses **high error correction** so the QR code remains scannable even with a logo overlay.

The script is intended for generating print-quality or web-ready QR codes for URLs, links, or identifiers where branding is required.

---

## Features

* High-resolution QR output (default: 1024×1024)
* Embedded center logo with automatic scaling
* Optional white backing plate behind the logo for contrast
* High error correction (`ERROR_CORRECT_H`) to preserve scannability
* Simple, dependency-light implementation

---

## Requirements

* Python 3.9+
* Dependencies:

  * `qrcode[pil] >= 7.4`
  * `Pillow >= 10.0`

Install dependencies with:

```bash
pip install -r requirements.txt
```

or directly:

```bash
pip install qrcode[pil] Pillow
```

---

## Files

* `make_qr_with_logo.py`
  Main script that generates the QR code.
* `logo.png`
  Logo image to embed in the QR code (not included).
* `qr_with_logo.png`
  Output image (generated).
* `requirements.txt`
  Python dependencies.

---

## Usage

### Basic Example

```bash
python make_qr_with_logo.py
```

By default, this generates a QR code pointing to:

```
https://kzoomakers.org
```

and saves it as:

```
qr_with_logo.png
```

You must provide a `logo.png` file in the same directory (or update the path).

---

## Script Overview

```python
make_qr_with_logo(
    data="https://example.com",
    logo_path="logo.png",
    out_path="qr_with_logo.png",
    qr_size=1024,
    logo_scale=0.22,
)
```

### Parameters

| Parameter    | Description                                                   |
| ------------ | ------------------------------------------------------------- |
| `data`       | String encoded into the QR code                               |
| `logo_path`  | Path to logo image (PNG recommended, RGBA supported)          |
| `out_path`   | Output file name                                              |
| `qr_size`    | Final image size in pixels (square)                           |
| `logo_scale` | Logo width as a fraction of QR width (recommended: 0.18–0.25) |
| `border`     | QR quiet zone size (default: 4)                               |

---

## Design Notes

* **Error Correction**: Uses `ERROR_CORRECT_H` to tolerate logo occlusion.
* **Resampling**: Uses Lanczos resampling for clean scaling.
* **Contrast Plate**: A white background plate is added behind the logo to ensure readability against dense QR modules.
* **Center Placement**: Logo is always centered to minimize interference with finder patterns.

---

## Best Practices

* Keep the logo under ~25% of QR width.
* Use high-contrast logos (or rely on the white plate).
* Test scans on multiple devices before printing.
* Avoid placing logos near QR finder corners.

---

## License

MIT License.
Use freely, modify as needed, no warranty implied.

