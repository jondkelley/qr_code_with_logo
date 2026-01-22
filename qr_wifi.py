from PIL import Image
import qrcode
from qrcode.constants import ERROR_CORRECT_H


def _escape_wifi_value(value: str) -> str:
    """
    Escape characters required by the Wi-Fi QR spec.
    Characters to escape: \ ; , : "
    """
    if value is None:
        return ""
    for ch in ["\\", ";", ",", ":", '"']:
        value = value.replace(ch, f"\\{ch}")
    return value


def make_wifi_qr_with_logo(
    ssid: str,
    password: str | None = None,
    security: str = "WPA",     # WPA, WEP, or nopass
    hidden: bool = False,
    logo_path: str = "logo.png",
    out_path: str = "wifi_qr_with_logo.png",
    qr_size: int = 1024,
    logo_scale: float = 0.22,  # keep ~0.18–0.25
    border: int = 4,
) -> None:
    """
    Generate a Wi-Fi QR code with a centered logo.

    security:
      - "WPA"  (covers WPA/WPA2/WPA3)
      - "WEP"
      - "nopass" (open networks)
    """

    sec = security.upper()
    if sec not in {"WPA", "WEP", "NOPASS"}:
        raise ValueError("security must be 'WPA', 'WEP', or 'nopass'")

    ssid_esc = _escape_wifi_value(ssid)
    pwd_esc = _escape_wifi_value(password) if sec != "NOPASS" else ""

    wifi_payload = f"WIFI:T:{sec};S:{ssid_esc};"
    if sec != "NOPASS":
        wifi_payload += f"P:{pwd_esc};"
    if hidden:
        wifi_payload += "H:true;"
    wifi_payload += ";"

    # Build QR (high error correction to survive logo occlusion)
    qr = qrcode.QRCode(
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=border,
    )
    qr.add_data(wifi_payload)
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color="black",
        back_color="white"
    ).convert("RGBA")
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    # Load and resize logo
    logo = Image.open(logo_path).convert("RGBA")
    target_w = int(qr_size * logo_scale)
    w, h = logo.size
    scale = target_w / float(w)
    target_h = int(h * scale)
    logo = logo.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # White plate for contrast
    pad = int(qr_size * 0.015)
    plate = Image.new(
        "RGBA",
        (logo.size[0] + 2 * pad, logo.size[1] + 2 * pad),
        (255, 255, 255, 255),
    )
    plate_pos = (
        (plate.size[0] - logo.size[0]) // 2,
        (plate.size[1] - logo.size[1]) // 2,
    )
    plate.alpha_composite(logo, dest=plate_pos)

    # Center overlay
    pos = (
        (qr_size - plate.size[0]) // 2,
        (qr_size - plate.size[1]) // 2,
    )
    qr_img.alpha_composite(plate, dest=pos)

    qr_img.save(out_path)


if __name__ == "__main__":
    # Example: WPA/WPA2/WPA3
    make_wifi_qr_with_logo(
        ssid="KzooMakers-WiFi",
        password="correct-horse-battery-staple",
        security="WPA",
        hidden=False,
        logo_path="logo.png",
        out_path="wifi_qr_wpa.png",
    )

    # Example: Open network
    make_wifi_qr_with_logo(
        ssid="KzooMakers-Guest",
        security="nopass",
        logo_path="logo.png",
        out_path="wifi_qr_open.png",
    )

    # Example: WEP (legacy)
    make_wifi_qr_with_logo(
        ssid="LegacyNet",
        password="wepkey123",
        security="WEP",
        logo_path="logo.png",
        out_path="wifi_qr_wep.png",
    )

