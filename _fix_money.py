"""Add money column cleanup: fill zeros, drop empty, mark for $ format."""

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add cleanup after Auxiliar column is created, before st.success
old_marker = """                    st.success(f\"**{target_file}**"""

new_code = """                    # Columnas monetarias: desde 'No Gravado' en adelante (excluyendo Auxiliar)
                    all_cols = list(df_arca.columns)
                    ng_idx = all_cols.index('No Gravado') if 'No Gravado' in all_cols else None
                    if ng_idx is not None:
                        money_cols = [c for c in all_cols[ng_idx:] if c != 'Auxiliar']
                        for c in money_cols:
                            df_arca[c] = pd.to_numeric(df_arca[c], errors='coerce').fillna(0)
                        # Eliminar columnas monetarias que son todo cero
                        empty_money = [c for c in money_cols if (df_arca[c] == 0).all()]
                        df_arca = df_arca.drop(columns=empty_money)

                    st.success(f\"**{target_file}**"""

if old_marker in content:
    content = content.replace(old_marker, new_code)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done app.py!")
else:
    print("ERROR: marker not found in app.py")
