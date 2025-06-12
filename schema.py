import strawberry
from db import db
import pandas as pd
from typing import List, Optional

# ---------------------
# Tipos para GraphQL
# ---------------------

@strawberry.type
class EficienciaProduccion:
    lote_id: str
    producto: str
    eficiencia: float

@strawberry.type
class MargenBruto:
    producto: str
    margen: float

@strawberry.type
class VentasPorCategoria:
    categoria: str
    total_ventas: float

@strawberry.type
class AnioMes:
    anio: int
    mes: int

# ---------------------
# Query Root
# ---------------------

@strawberry.type
class Query:

    # Eficiencia Producción
    @strawberry.field
    def eficiencia_produccion(
        self,
        anio: Optional[int] = None,
        mes: Optional[int] = None
    ) -> List[EficienciaProduccion]:
        data = list(db.produccion.find())
        df = pd.DataFrame(data)

        if 'cantidad_producida' not in df.columns or 'cantidad_planificada' not in df.columns or 'fecha_produccion' not in df.columns:
            return []

        df['fecha_produccion'] = pd.to_datetime(df['fecha_produccion'])

        if anio is not None:
            df = df[df['fecha_produccion'].dt.year == anio]
        if mes is not None:
            df = df[df['fecha_produccion'].dt.month == mes]

        df['eficiencia'] = (df['cantidad_producida'] / df['cantidad_planificada']) * 100

        return [
            EficienciaProduccion(
                lote_id=row.get('lote_id', ''),
                producto=row.get('producto_id', ''),
                eficiencia=round(row['eficiencia'], 2)
            )
            for _, row in df.iterrows()
        ]

    # Margen Bruto
    @strawberry.field
    def margen_bruto(
        self,
        anio: Optional[int] = None,
        mes: Optional[int] = None
    ) -> List[MargenBruto]:
        data = list(db.finanzas.find())
        df = pd.DataFrame(data)

        if 'precio_venta_unitario' not in df.columns or 'costo_unitario' not in df.columns or 'fecha_venta' not in df.columns:
            return []

        df['fecha_venta'] = pd.to_datetime(df['fecha_venta'])

        if anio is not None:
            df = df[df['fecha_venta'].dt.year == anio]
        if mes is not None:
            df = df[df['fecha_venta'].dt.month == mes]

        df['margen'] = ((df['precio_venta_unitario'] - df['costo_unitario']) / df['precio_venta_unitario']) * 100

        return [
            MargenBruto(
                producto=row.get('producto_id', ''),
                margen=round(row['margen'], 2)
            )
            for _, row in df.iterrows()
        ]

    # Ventas por Categoría
    @strawberry.field
    def ventas_por_categoria(
        self,
        anio: Optional[int] = None,
        mes: Optional[int] = None
    ) -> List[VentasPorCategoria]:
        data = list(db.ventas.find())
        df = pd.DataFrame(data)

        if 'cantidad_vendida' not in df.columns or 'precio_venta_unitario' not in df.columns or 'fecha_venta' not in df.columns:
            return []

        df['fecha_venta'] = pd.to_datetime(df['fecha_venta'])

        if anio is not None:
            df = df[df['fecha_venta'].dt.year == anio]
        if mes is not None:
            df = df[df['fecha_venta'].dt.month == mes]

        df['venta_total'] = df['cantidad_vendida'] * df['precio_venta_unitario']
        group = df.groupby('categoria_producto')['venta_total'].sum().reset_index()

        return [
            VentasPorCategoria(
                categoria=row['categoria_producto'],
                total_ventas=round(row['venta_total'], 2)
            )
            for _, row in group.iterrows()
        ]

    # Años y meses disponibles para Ventas
    @strawberry.field
    def anios_meses_disponibles_ventas(self) -> List[AnioMes]:
        data = list(db.ventas.find())
        df = pd.DataFrame(data)

        if 'fecha_venta' not in df.columns:
            return []

        df['fecha_venta'] = pd.to_datetime(df['fecha_venta'])
        df['anio'] = df['fecha_venta'].dt.year
        df['mes'] = df['fecha_venta'].dt.month

        group = df[['anio', 'mes']].drop_duplicates().sort_values(['anio', 'mes'])

        return [
            AnioMes(anio=row['anio'], mes=row['mes'])
            for _, row in group.iterrows()
        ]

    # Años y meses disponibles para Eficiencia Producción
    @strawberry.field
    def anios_meses_disponibles_eficiencia_produccion(self) -> List[AnioMes]:
        data = list(db.produccion.find())
        df = pd.DataFrame(data)

        if 'fecha_produccion' not in df.columns:
            return []

        df['fecha_produccion'] = pd.to_datetime(df['fecha_produccion'])
        df['anio'] = df['fecha_produccion'].dt.year
        df['mes'] = df['fecha_produccion'].dt.month

        group = df[['anio', 'mes']].drop_duplicates().sort_values(['anio', 'mes'])

        return [
            AnioMes(anio=row['anio'], mes=row['mes'])
            for _, row in group.iterrows()
        ]

    # Años y meses disponibles para Margen Bruto
    @strawberry.field
    def anios_meses_disponibles_margen_bruto(self) -> List[AnioMes]:
        data = list(db.finanzas.find())
        df = pd.DataFrame(data)

        if 'fecha_venta' not in df.columns:
            return []

        df['fecha_venta'] = pd.to_datetime(df['fecha_venta'])
        df['anio'] = df['fecha_venta'].dt.year
        df['mes'] = df['fecha_venta'].dt.month

        group = df[['anio', 'mes']].drop_duplicates().sort_values(['anio', 'mes'])

        return [
            AnioMes(anio=row['anio'], mes=row['mes'])
            for _, row in group.iterrows()
        ]

# ---------------------
# Schema
# ---------------------
schema = strawberry.Schema(query=Query)
