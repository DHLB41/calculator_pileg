from io import BytesIO
import pandas as pd
from fpdf import FPDF
from pathlib import Path
from utils.formatters import format_ribuan, extract_roman_order


def format_dataframe_for_export(df_terpilih, df_dapil=None):
    df = df_terpilih.copy()

    # Format angka-angka penting
    df["Total RAB"] = df["TOTAL_RAB"].fillna(0).apply(format_ribuan)
    df["Target Suara 2029"] = df["TARGET_SUARA_2029"].fillna(0).apply(format_ribuan)
    df["Suara 2024"] = df["SUARA_2024"].fillna(0).apply(format_ribuan)
    df["Target Kursi 2029"] = df["TARGET_TAMBAHAN_KURSI"].fillna(0).astype(int)
    df["Total SP"] = df["SP"].fillna(0).apply(format_ribuan)

    # Tambahkan PROPINSI dari master df_dapil
    if df_dapil is not None:
        df = df.merge(df_dapil[["DAPIL", "PROPINSI", "GUGUSAN"]], on="DAPIL", how="left")
        df["ROMAWI_ORDER"] = df["DAPIL"].apply(extract_roman_order)
        df = df.sort_values(by=["GUGUSAN", "PROPINSI", "ROMAWI_ORDER"])

    kolom_terpilih = [
        "DAPIL", "PROPINSI", "ALOKASI_KURSI", "KURSI_2024",
        "Target Kursi 2029", "Suara 2024", "Target Suara 2029", "Total SP", "Total RAB"
    ]
    return df[kolom_terpilih]


def export_to_csv(df_terpilih, df_dapil=None):
    df_formatted = format_dataframe_for_export(df_terpilih, df_dapil)
    return df_formatted.to_csv(index=False).encode("utf-8")


def export_to_excel(df_terpilih, df_dapil=None):
    df_formatted = format_dataframe_for_export(df_terpilih, df_dapil)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_formatted.to_excel(writer, sheet_name="Rekap Dapil", index=False)
    return output.getvalue()


def export_to_pdf(df_terpilih, df_dapil=None, title="Ringkasan Kalkulasi Dapil"):
    df = format_dataframe_for_export(df_terpilih, df_dapil)

    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(11, 61, 145)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(2)

    # Header ringkasan
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    # Tabel header
    pdf.set_fill_color(11, 61, 145)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 9)

    headers = ["Dapil", "Alokasi Kursi", "Kursi 2024", "Target Kursi 2029", "Suara 2024", "Target Suara 2029", "Total SP", "Total RAB"]
    col_widths = [60, 25, 25, 30, 35, 35, 35, 40]

    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 10, h, border=1, align="C", fill=True)
    pdf.ln()

    # Isi tabel dengan blok per propinsi
    pdf.set_font("Arial", size=9)
    pdf.set_text_color(0, 0, 0)

    last_propinsi = None
    for _, row in df.iterrows():
        if row["PROPINSI"] != last_propinsi:
            pdf.set_fill_color(240, 244, 255)
            pdf.set_font("Arial", "B", 9)
            pdf.cell(sum(col_widths), 8, row["PROPINSI"], ln=True, fill=True)
            last_propinsi = row["PROPINSI"]
            pdf.set_font("Arial", size=9)

        values = [
            row["DAPIL"], row["ALOKASI_KURSI"], row["KURSI_2024"],
            row["Target Kursi 2029"], row["Suara 2024"],
            row["Target Suara 2029"], row["Total SP"], row["Total RAB"]
        ]

        for i, val in enumerate(values):
            pdf.cell(col_widths[i], 8, str(val), border=1)
        pdf.ln()

    return pdf.output(dest='S').encode('latin1')


def export_to_html(df_terpilih, df_dapil, selected_party, votes_2024, seats_2024):
    df = format_dataframe_for_export(df_terpilih, df_dapil)

    total_suara = format_ribuan(df_terpilih["TARGET_SUARA_2029"].sum())
    total_kursi = int(df_terpilih["TARGET_TAMBAHAN_KURSI"].sum())
    total_rab = format_ribuan(df_terpilih["TOTAL_RAB"].sum())
    suara_2024 = format_ribuan(votes_2024)
    kursi_2024 = format_ribuan(seats_2024)

    rows_html = ""
    last_propinsi = None

    for _, row in df.iterrows():
        current_propinsi = row["PROPINSI"]
        if current_propinsi != last_propinsi:
            rows_html += f"<tr><th colspan='9' class='propinsi-header'>{current_propinsi}</th></tr>"
            last_propinsi = current_propinsi

        rows_html += f"""
        <tr>
            <td>{row['DAPIL']}</td>
            <td>{row['ALOKASI_KURSI']}</td>
            <td>{row['KURSI_2024']}</td>
            <td>{row['Target Kursi 2029']}</td>
            <td style='text-align:right'>{row['Suara 2024']}</td>
            <td style='text-align:right'>{row['Target Suara 2029']}</td>
            <td style='text-align:right'>{row['Total SP']}</td>
            <td style='text-align:right'>{row['Total RAB']}</td>
        </tr>
        """

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Rangkuman Kalkulasi Pemilu 2029</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; padding: 40px; background: #fff; color: #222; }}
            h1 {{ font-size: 26px; color: #0b3d91; margin-bottom: 1rem; }}
            h2 {{ font-size: 20px; color: #333; margin-top: 2.5rem; margin-bottom: 0.8rem; }}
            .info-box {{ margin-bottom: 30px; font-size: 16px; }}
            .info-box div {{ margin-bottom: 6px; }}
            .info-box strong {{ display: inline-block; width: 220px; }}
            table {{ border-collapse: collapse; width: 100%; font-size: 14px; margin-top: 10px; }}
            th, td {{ border: 1px solid #ccc; padding: 10px 8px; text-align: center; }}
            th {{ background-color: #0b3d91; color: #fff; font-size: 14px; }}
            td {{ vertical-align: middle; }}
            td:nth-child(1) {{ text-align: left; width: 25%; }}
            td:nth-child(5), td:nth-child(6), td:nth-child(7), td:nth-child(8) {{ text-align: right; }}
            .propinsi-header {{ background-color: #f0f4ff; text-align: left; font-weight: bold; padding: 10px 12px; font-size: 15px; color: #0b3d91; border-top: 2px solid #0b3d91; }}
            tr:hover td {{ background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <h1>Rangkuman Hasil Akhir Kalkulasi Pemilu 2029</h1>
        <div class="info-box">
            <div><strong>Partai:</strong> {selected_party}</div>
            <div><strong>Perolehan Suara 2024:</strong> {suara_2024}</div>
            <div><strong>Perolehan Kursi 2024:</strong> {kursi_2024}</div>
            <div><strong>Total Target Suara 2029:</strong> {total_suara}</div>
            <div><strong>Total Target Kursi 2029:</strong> {total_kursi}</div>
            <div><strong>Total RAB (Rp):</strong> {total_rab}</div>
        </div>

        <h2>Persebaran Dapil Potensial</h2>
        <table>
            <tr>
                <th>Dapil</th>
                <th>Alokasi Kursi</th>
                <th>Kursi 2024</th>
                <th>Target Kursi 2029</th>
                <th>Suara 2024</th>
                <th>Target Suara 2029</th>
                <th>Total SP</th>
                <th>Total RAB</th>
            </tr>
            {rows_html}
        </table>
    </body>
    </html>
    """

    return html_template

def export_dapil_simulasi_to_html(row, nama_file="rangkuman_simulasi.html"):
    from utils.formatters import format_ribuan

    def format_val(val):
        return format_ribuan(val) if isinstance(val, (int, float)) else val

    partai_k2_label = f"{row['PARTAI_K2_TERENDAH']} ({format_ribuan(row['SUARA_K2'])})"

    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Simulasi {row['DAPIL']}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                margin: 0;
                padding: 2rem;
                color: #212529;
            }}
            h1 {{
                text-align: center;
                color: #003366;
                margin-bottom: 2rem;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: #fff;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            }}
            .grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem 2rem;
            }}
            .label {{
                font-weight: bold;
                color: #555;
            }}
            .value {{
                background: #f1f3f5;
                padding: 0.5rem;
                border-radius: 6px;
                word-wrap: break-word;
            }}
        </style>
    </head>
    <body>
        <h1>Rangkuman Simulasi Pencalonan Legislatif Pemilu 2029<br>Dapil {row['DAPIL'].upper()}</h1>
        <div class="container">
            <div class="grid">
                <div class="label">Partai:</div> <div class="value">{row['PARTAI']}</div>
                <div class="label">Alokasi Kursi:</div> <div class="value">{row['ALOKASI KURSI']}</div>
                <div class="label">Kursi 2024:</div> <div class="value">{row['KURSI_2024']}</div>
                <div class="label">Suara 2024:</div> <div class="value">{format_val(row['SUARA_2024'])}</div>
                <div class="label">Target Kursi 2029:</div> <div class="value">{row['TARGET_TAMBAHAN_KURSI']}</div>
                <div class="label">Target Suara 2029:</div> <div class="value">{format_val(row['TARGET_SUARA_2029'])}</div>
                <div class="label">Partai K2 Terendah:</div> <div class="value">{partai_k2_label}</div>
                <div class="label">SP:</div> <div class="value">{format_val(row['SP'])}</div>
                <div class="label">RAB SP + Manajemen:</div> <div class="value">{format_val(row['BIAYA_KAMPANYE'])}</div>
                <div class="label">Biaya Pendampingan:</div> <div class="value">{format_val(row['BIAYA_PENDAMPINGAN'])}</div>
                <div class="label">Total RAB:</div> <div class="value">{format_val(row['TOTAL_RAB'])}</div>
            </div>
        </div>
    </body>
    </html>
    """
    return html