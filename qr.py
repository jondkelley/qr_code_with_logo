from PIL import Image
import qrcode
from qrcode.constants import ERROR_CORRECT_H

def make_qr_with_logo(
    data: str,
    logo_path: str,
    out_path: str = "qr_with_logo.png",
    qr_size: int = 1024,
    logo_scale: float = 0.22,   # fraction of QR width (keep ~0.18–0.25)
    border: int = 4,
) -> None:
    # Build QR (high error correction to survive logo occlusion)
    qr = qrcode.QRCode(
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    # Load logo
    logo = Image.open(logo_path).convert("RGBA")

    # Resize logo
    target_w = int(qr_size * logo_scale)
    w, h = logo.size
    scale = target_w / float(w)
    target_h = int(h * scale)
    logo = logo.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # Optional: add a white "plate" behind logo for contrast
    pad = int(qr_size * 0.015)
    plate = Image.new("RGBA", (logo.size[0] + 2 * pad, logo.size[1] + 2 * pad), (255, 255, 255, 255))
    plate_pos = ((plate.size[0] - logo.size[0]) // 2, (plate.size[1] - logo.size[1]) // 2)
    plate.alpha_composite(logo, dest=plate_pos)

    # Center paste
    pos = ((qr_size - plate.size[0]) // 2, (qr_size - plate.size[1]) // 2)
    qr_img.alpha_composite(plate, dest=pos)

    # Save
    qr_img.save(out_path)

if __name__ == "__main__":
    make_qr_with_logo(
        data="https://kzoomakers.org",
        logo_path="logo.png",
        out_path="qr_with_logo.png",
        qr_size=1024,
        logo_scale=0.22,
    )

