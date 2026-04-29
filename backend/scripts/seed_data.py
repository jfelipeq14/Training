#!/usr/bin/env python3
"""
Script para crear datos de prueba en la base de datos - Grandma's Food
"""

import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from decimal import Decimal
from uuid import uuid4
from datetime import datetime, timezone

# Añadir el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from config.config import settings
from app.customers.model import Customer
from app.meals.model import Meal, CategoryEnum
from app.orders.model import Order

def create_sample_data():
    """Crear datos de ejemplo para testing"""
    
    # Conectar a la base de datos
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("🗄️  Creando datos de prueba para Grandma's Food")
        print("=" * 50)
        
        # 1. Limpiar datos existentes en orden correcto (orders -> meals -> customers)
        print("\n🗑️  Limpiando datos existentes...")
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        
        # Eliminar en orden inverso a las dependencias de FK
        if 'orders' in table_names:
            db.query(Order).delete()
            print("✅ Pedidos eliminados")
        else:
            print("ℹ️  Tabla 'orders' no existe, omitiendo limpieza")
            
        if 'meals' in table_names:
            db.query(Meal).delete()
            print("✅ Combos eliminados")
        else:
            print("ℹ️  Tabla 'meals' no existe, omitiendo limpieza")
            
        if 'customers' in table_names:
            db.query(Customer).delete()
            print("✅ Clientes eliminados")
        else:
            print("ℹ️  Tabla 'customers' no existe, omitiendo limpieza")
            
        db.commit()
        print("✅ Datos anteriores eliminados")
        
        # 2. Crear clientes de prueba
        print("\n👥 Creando clientes...")
        customers_data = [
            Customer(
                document_number='CC-12345678',
                full_name='Juan Pérez González',
                email='juan.perez@email.com',
                phone_number='3001234567',
                address='Calle 123 #45-67, Bogotá'
            ),
            Customer(
                document_number='CE-87654321',
                full_name='María Rodríguez López',
                email='maria.rodriguez@email.com',
                phone_number='3109876543',
                address='Avenida 78 #90-12, Bogotá'
            ),
            Customer(
                document_number='CC-11223344',
                full_name='Carlos Martínez Silva',
                email='carlos.martinez@email.com',
                phone_number='3505557777',
                address='Carrera 15 #32-10, Bogotá'
            ),
            Customer(
                document_number='P-55667788',
                full_name='Ana Sofía Gómez',
                email='ana.gomez@email.com',
                phone_number='3112223333',
                address='Diagonal 44 #55-66, Bogotá'
            ),
            Customer(
                document_number='CC-99887766',
                full_name='Luis Fernando Torres',
                email='luis.torres@email.com',
                phone_number='3154445555',
                address='Calle 100 #20-30, Bogotá'
            )
        ]
        
        for customer in customers_data:
            db.add(customer)
        db.commit()
        print(f"✅ {len(customers_data)} clientes creados")
        
        # 3. Crear combos de prueba con UUIDs
        print("\n🍔 Creando combos...")
        meals_data = [
            Meal(
                uuid=uuid4(),
                name='COMBO SUPER CHEESE BURGER DOBLE',
                category=CategoryEnum.HAMBURGERS_AND_HOTDOGS,
                description='Hamburguesa pan de ajonjolí, doble carne de 200gr, queso cheddar extra, papas fritas y gaseosa de 350ml',
                price_without_iva=Decimal('25000.00'),
                is_available=True
            ),
            Meal(
                uuid=uuid4(),
                name='COMBO CLÁSICO POLLO FRITO',
                category=CategoryEnum.CHICKEN,
                description='8 piezas de pollo frito crujiente, papas a la francesa, ensalada de repollo y gaseosa de 350ml',
                price_without_iva=Decimal('22000.00'),
                is_available=True
            ),
            Meal(
                uuid=uuid4(),
                name='COMBO FILETE DE PESCADO',
                category=CategoryEnum.FISH,
                description='Filete de tilapia empanizado, arroz con coco, patacón pisaíto y limonada natural',
                price_without_iva=Decimal('28000.00'),
                is_available=True
            ),
            Meal(
                uuid=uuid4(),
                name='COMBO PARRILLA ESPECIAL',
                category=CategoryEnum.MEATS,
                description='Chuleta de res 300gr, arepa boyacense, casuela de frijoles y jugo de lulo',
                price_without_iva=Decimal('35000.00'),
                is_available=True
            ),
            Meal(
                uuid=uuid4(),
                name='COMBO CHEESECAKE DELUXE',
                category=CategoryEnum.DESSERTS,
                description='Porción generosa de cheesecake con salsa de frutos rojos, helado de vainilla y café',
                price_without_iva=Decimal('15000.00'),
                is_available=True
            ),
            Meal(
                uuid=uuid4(),
                name='COMPO BOWL VEGANO POWER',
                category=CategoryEnum.VEGAN_FOOD,
                description='Quinoa con vegetales salteados, aguacate, semillas de chía y aderezo de cilantro',
                price_without_iva=Decimal('20000.00'),
                is_available=True
            ),
            Meal(
                uuid=uuid4(),
                name='COMBO NIÑOS FELICES',
                category=CategoryEnum.KIDS_MEALS,
                description='Mini hamburguesa, papas fritas pequeñas, nuggets de pollo y jugo de naranja',
                price_without_iva=Decimal('18000.00'),
                is_available=True
            ),
            Meal(
                uuid=uuid4(),
                name='COMBO HOT DOG EXTREMO',
                category=CategoryEnum.HAMBURGERS_AND_HOTDOGS,
                description='Perro caliente con salchicha premium, tocineta, queso fundido, cebolla caramelizada y papas',
                price_without_iva=Decimal('19000.00'),
                is_available=True
            ),
            Meal(
                uuid=uuid4(),
                name='COMBO ALAS DE BUFFALO',
                category=CategoryEnum.CHICKEN,
                description='12 piezas de alas de pollo con salsa buffalo, apio, zanahoria y ranch dressing',
                price_without_iva=Decimal('24000.00'),
                is_available=False  # No disponible temporalmente
            ),
            Meal(
                uuid=uuid4(),
                name='COMBO TIRITAS DE POLLO CRUJIENTES',
                category=CategoryEnum.CHICKEN,
                description='Tiritas de pollo empanizadas, salsa BBQ, papas gajo y gaseosa de 350ml',
                price_without_iva=Decimal('21000.00'),
                is_available=True
            )
        ]
        
        for meal in meals_data:
            db.add(meal)
        db.commit()
        print(f"✅ {len(meals_data)} combos creados")
        
        # 4. Obtener IDs y UUIDs reales de los meals creados
        print("\n🔍 Obteniendo IDs y UUIDs de combos...")
        created_meals = db.query(Meal).order_by(Meal.id).all()
        meal_uuids = {meal.name: str(meal.uuid) for meal in created_meals}
        meal_ids = {meal.name: meal.id for meal in created_meals}
        
        print("✅ UUIDs de combos obtenidos:")
        for name, meal_uuid in meal_uuids.items():
            print(f"   {name}: UUID {meal_uuid}")
        
        # 5. Crear pedidos de prueba usando UUIDs reales
        print("\n📦 Creando pedidos...")
        orders_data = [
            Order(
                uuid=str(uuid4()),
                customer_document='CC-12345678',
                meal_id=meal_ids['COMBO SUPER CHEESE BURGER DOBLE'],
                combo_uuid=meal_uuids['COMBO SUPER CHEESE BURGER DOBLE'],
                quantity=2,
                additional_info='Hamburguesa sin cebolla, extra queso',
                subtotal_without_iva=Decimal('50000.00'),
                iva_amount=Decimal('9500.00'),
                total_with_iva=Decimal('59500.00'),
                is_delivered=True,
                delivery_date=datetime.now(timezone.utc)
            ),
            Order(
                uuid=str(uuid4()),
                customer_document='CE-87654321',
                meal_id=meal_ids['COMBO CLÁSICO POLLO FRITO'],
                combo_uuid=meal_uuids['COMBO CLÁSICO POLLO FRITO'],
                quantity=1,
                additional_info='Con papas fritas',
                subtotal_without_iva=Decimal('22000.00'),
                iva_amount=Decimal('4180.00'),
                total_with_iva=Decimal('26180.00'),
                is_delivered=False
            ),
            Order(
                uuid=str(uuid4()),
                customer_document='CC-11223344',
                meal_id=meal_ids['COMBO FILETE DE PESCADO'],
                combo_uuid=meal_uuids['COMBO FILETE DE PESCADO'],
                quantity=3,
                additional_info='Filete con arroz y ensalada',
                subtotal_without_iva=Decimal('66000.00'),
                iva_amount=Decimal('12540.00'),
                total_with_iva=Decimal('78540.00'),
                is_delivered=False
            ),
            Order(
                uuid=str(uuid4()),
                customer_document='P-55667788',
                meal_id=meal_ids['COMBO PARRILLA ESPECIAL'],
                combo_uuid=meal_uuids['COMBO PARRILLA ESPECIAL'],
                quantity=2,
                additional_info='Con jugo de limón',
                subtotal_without_iva=Decimal('48000.00'),
                iva_amount=Decimal('9120.00'),
                total_with_iva=Decimal('57120.00'),
                is_delivered=False
            ),
            Order(
                uuid=str(uuid4()),
                customer_document='CC-99887766',
                meal_id=meal_ids['COMBO NIÑOS FELICES'],
                combo_uuid=meal_uuids['COMBO NIÑOS FELICES'],
                quantity=1,
                additional_info='Con jugo y zanahoria',
                subtotal_without_iva=Decimal('18000.00'),
                iva_amount=Decimal('3420.00'),
                total_with_iva=Decimal('21420.00'),
                is_delivered=False
            )
        ]
        
        for order in orders_data:
            db.add(order)
        db.commit()
        print(f"✅ {len(orders_data)} pedidos creados")
        
        # 6. Estadísticas finales
        total_customers = db.query(Customer).count()
        total_meals = db.query(Meal).count()
        total_orders = db.query(Order).count()
        delivered_orders = db.query(Order).filter(Order.is_delivered == True).count()
        pending_orders = db.query(Order).filter(Order.is_delivered == False).count()
        
        print(f"\n📊 Resumen final:")
        print(f"   👥 Clientes: {total_customers}")
        print(f"   🍔 Combos: {total_meals}")
        print(f"   📦 Pedidos: {total_orders}")
        print(f"   ✅ Pedidos entregados: {delivered_orders}")
        print(f"   ⏳ Pedidos pendientes: {pending_orders}")
        
        print(f"\n🎉 ¡Datos de prueba creados exitosamente!")
        print(f"\n🚀 API lista para probar en:")
        print(f"   http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Error creando datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
