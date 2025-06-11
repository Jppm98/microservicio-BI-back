from kpi import cargar_csv_en_mongo

print(cargar_csv_en_mongo("data/produccion.csv", "produccion"))
print(cargar_csv_en_mongo("data/finanzas.csv", "finanzas"))
print(cargar_csv_en_mongo("data/ventas.csv", "ventas"))
