from utils.formatters import format_ribuan, extract_roman_order
import pandas as pd

def export_to_html(df_terpilih, df_dapil, selected_party, votes_2024, seats_2024):
    df = df_terpilih.copy()

    # Format kolom utama
    df["Total RAB"] = df["TOTAL_RAB"].fillna(0).apply(format_ribuan)
    df["Target Suara 2029"] = df["TOTAL_TARGET_SUARA_2029"].fillna(0).apply(format_ribuan)
    df["Suara 2024"] = df["SUARA_2024"].fillna(0).apply(format_ribuan)
    df["Target Kursi 2029"] = df["TARGET_TAMBAHAN_KURSI"].fillna(0).astype(int)
    df["Total SP"] = df["SP"].fillna(0).apply(format_ribuan)

    # Merge tambahan kolom GUGUSAN dan PROPINSI
    df = df.merge(df_dapil[["DAPIL", "PROPINSI", "GUGUSAN"]], on="DAPIL", how="left")
    df["ROMAWI_ORDER"] = df["DAPIL"].apply(extract_roman_order)

    # Urutkan berdasarkan Gugusan > Provinsi > Romawi order
    df = df.sort_values(by=["GUGUSAN", "PROPINSI", "ROMAWI_ORDER"])

    # Total Summary Info
    total_suara = format_ribuan(df["TOTAL_TARGET_SUARA_2029"].sum())
    total_kursi = int(df["TARGET_TAMBAHAN_KURSI"].sum())
    total_rab = format_ribuan(df["TOTAL_RAB"].sum())
    suara_2024 = format_ribuan(votes_2024)
    kursi_2024 = format_ribuan(seats_2024)

    # Build Table Rows
    rows_html = ""
    last_propinsi = None

    for _, row in df.iterrows():
        current_propinsi = row["PROPINSI"]

        if current_propinsi != last_propinsi:
            rows_html += f"<tr><th colspan='8' class='propinsi-header'>{current_propinsi}</th></tr>"
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

    # Final HTML Template
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
