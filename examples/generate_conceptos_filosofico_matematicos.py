#!/usr/bin/env python3
"""
Generar Suite de Conceptos Filosófico-Matemáticos (Español)
===========================================================

22 visualizaciones profundas abarcando sabiduría antigua hasta ciencia moderna:
P01: LA UNIDAD (Schwaller de Lubicz)
P02: Servus Fugitivus (Sirviente fugitivo alquímico)
P03: Spiritus Domini (Espíritu sobre las aguas)
P04: Solve et Coagula (Transformación alquímica)
P05: Porfirinas Elixir Maestro (Activación molecular luz-sonido)
P06: Equivalencia Computacional Maestro (Principio de Wolfram)
P07: Programas Simples Subyacen Complejidad
P08: Materia de Quarks y Porfirinas (Partículas a vida)
P09: Paradoja Cuántica Maestro (Superposición, observación)
P10: Φ+1 Concentración (Convergencia de razón áurea)
P11: Φ-1 Dispersión (Expansión de razón áurea)
P12: Génesis de Φ+1 (Nacimiento de la media áurea)
P13: (√5+1)/2 (Fórmula de razón áurea)
P14: Contar (Primera forma de conciencia)
P15: Escisión Original (Polarización de energía)
P16: Glándulas del Encéfalo (Pineal, pituitaria, hipotálamo)
P17: Acción Numerante de Φ (Phi como generador)
P18: Síntesis Continua (Discreto a continuo)
P19: Superficie Limita (Definición de forma)
P20: Primera Limitación (Sistema de eje ternario)
P21: 1:1/Φ:Φ² (Tríada de razón áurea)
P22: Línea Numérica es Movimiento (Génesis geométrica)

Modelo: Gemini 3 Pro Image (texto perfecto, alta calidad)
Costo: $0.12 por imagen × 22 = $2.64 total
Tasa de Éxito Esperada: 100% (basado en rendimiento previo del modelo Pro)
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from src.gemini_client import GeminiClient


# Concept definitions
CONCEPTS = [
    {"id": "P01", "title": "LA UNIDAD - Conciencia Cósmica Indivisible", "filename": "P01-la-unidad.png"},
    {"id": "P02", "title": "Servus Fugitivus - El Sirviente Fugitivo", "filename": "P02-servus-fugitivus.png"},
    {"id": "P03", "title": "Spiritus Domini Ferebatur Super Aquas", "filename": "P03-spiritus-domini.png"},
    {"id": "P04", "title": "Solve et Coagula", "filename": "P04-solve-et-coagula.png"},
    {"id": "P05", "title": "Porfirinas Elixir Maestro", "filename": "P05-porfirinas-elixir.png"},
    {"id": "P06", "title": "Equivalencia Computacional Maestro", "filename": "P06-equivalencia-computacional.png"},
    {"id": "P07", "title": "Programas Simples Subyacen Complejidad", "filename": "P07-programas-simples-complejidad.png"},
    {"id": "P08", "title": "Materia de Quarks y Porfirinas Elixir Maestro", "filename": "P08-quarks-porfirinas.png"},
    {"id": "P09", "title": "Paradoja Cuántica Maestro", "filename": "P09-paradoja-cuantica.png"},
    {"id": "P10", "title": "Φ+1 Concentración", "filename": "P10-phi-mas-1-concentracion.png"},
    {"id": "P11", "title": "Φ-1 Dispersión", "filename": "P11-phi-menos-1-dispersion.png"},
    {"id": "P12", "title": "Génesis de Φ+1", "filename": "P12-genesis-phi-mas-1.png"},
    {"id": "P13", "title": "(√5+1)/2 - La Fórmula de la Razón Áurea", "filename": "P13-formula-razon-aurea.png"},
    {"id": "P14", "title": "Contar - Primera Forma Innata de Conciencia", "filename": "P14-contar-conciencia.png"},
    {"id": "P15", "title": "La Escisión Original - Polarización de Energía", "filename": "P15-escision-original.png"},
    {"id": "P16", "title": "Glándulas del Encéfalo", "filename": "P16-glandulas-encefalo.png"},
    {"id": "P17", "title": "La Acción Numerante de Φ", "filename": "P17-accion-numerante-phi.png"},
    {"id": "P18", "title": "Síntesis Continua", "filename": "P18-sintesis-continua.png"},
    {"id": "P19", "title": "Superficie Limita Definición de Tamaño", "filename": "P19-superficie-limita.png"},
    {"id": "P20", "title": "Primera Limitación - Sistema de Eje Ternario", "filename": "P20-sistema-eje-ternario.png"},
    {"id": "P21", "title": "1:1/Φ:Φ² - Tríada de Razón Áurea", "filename": "P21-triada-razon-aurea.png"},
    {"id": "P22", "title": "La Línea Numérica Es Movimiento", "filename": "P22-linea-numerica-movimiento.png"},
]


async def generate_all():
    """Generate all Philosophical-Mathematical concept images in Spanish"""

    # Setup paths
    prompts_dir = Path(__file__).parent / "Conceptos Filosófico-Matemáticos"
    output_dir = prompts_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("🔮 SUITE DE CONCEPTOS FILOSÓFICO-MATEMÁTICOS")
    print("=" * 80)
    print()
    print("Sabiduría Antigua → Ciencia Moderna → Filosofía Matemática")
    print()
    print(f"Modelo: Gemini 3 Pro Image (gemini-3-pro-image-preview)")
    print(f"Conceptos: {len(CONCEPTS)}")
    print(f"Costo Esperado: ${len(CONCEPTS) * 0.12:.2f}")
    print()
    print("=" * 80)
    print()

    async with GeminiClient() as client:
        total_size = 0
        successful = 0
        failed = 0
        failed_list = []

        for i, concept in enumerate(CONCEPTS, 1):
            concept_id = concept["id"]
            title = concept["title"]
            filename = concept["filename"]

            print(f"[{i}/{len(CONCEPTS)}] Generando: {title}")
            print(f"    ID: {concept_id}")

            # Read prompt
            prompt_file = prompts_dir / f"{concept_id}-prompt.txt"
            if not prompt_file.exists():
                print(f"    ❌ ERROR: Archivo de prompt no encontrado: {prompt_file}")
                failed += 1
                failed_list.append(f"{concept_id}: Archivo de prompt faltante")
                print()
                continue

            prompt = prompt_file.read_text()

            # Generate image
            try:
                result = await client.generate_image(prompt, model="pro")

                # Save image
                output_path = output_dir / filename
                with open(output_path, 'wb') as f:
                    f.write(result["image_data"])

                size_mb = len(result["image_data"]) / (1024 * 1024)
                total_size += size_mb
                successful += 1

                print(f"    ✅ ¡Éxito! {size_mb:.2f} MB")
                print(f"    📁 {output_path.relative_to(Path.cwd())}")

            except Exception as e:
                failed += 1
                failed_list.append(f"{concept_id}: {str(e)[:50]}")
                print(f"    ❌ ERROR: {e}")

            print()

        # Summary
        print("=" * 80)
        print("📊 RESUMEN DE GENERACIÓN")
        print("=" * 80)
        print()
        print(f"✅ Exitosos: {successful}/{len(CONCEPTS)}")
        print(f"❌ Fallidos: {failed}/{len(CONCEPTS)}")
        if failed_list:
            print("\nConceptos fallidos:")
            for fail in failed_list:
                print(f"  - {fail}")
        print(f"\n📦 Tamaño Total: {total_size:.2f} MB")
        print(f"💰 Costo Real: ${successful * 0.12:.2f}")
        print(f"📂 Salida: {output_dir.relative_to(Path.cwd())}")
        print()

        if successful == len(CONCEPTS):
            print("🎉 ¡ÉXITO COMPLETO - TODOS LOS CONCEPTOS FILOSÓFICO-MATEMÁTICOS GENERADOS!")
        elif successful > 0:
            print(f"⚠️  ÉXITO PARCIAL - {successful} de {len(CONCEPTS)} generados")
        else:
            print("❌ GENERACIÓN FALLIDA - No se crearon imágenes")

        print()
        print("=" * 80)
        print()

        # Concept guide preview
        if successful > 0:
            print("🔮 CATEGORÍAS DE CONCEPTOS")
            print("=" * 80)
            print()
            print("**Sabiduría Antigua** (P01-P04):")
            print("  Unidad, Alquimia, Génesis, Transformación")
            print()
            print("**Molecular y Cuántico** (P05-P09):")
            print("  Porfirinas, Equivalencia Computacional, Complejidad, Paradojas Cuánticas")
            print()
            print("**Filosofía de Razón Áurea** (P10-P13, P17, P21):")
            print("  Φ concentración/dispersión, Génesis, Fórmula, Acción Numerante, Tríada")
            print()
            print("**Conciencia y Número** (P14-P15, P18, P22):")
            print("  Contar, Escisión, Síntesis, Número como Movimiento")
            print()
            print("**Filosofía Espacial** (P16, P19-P20):")
            print("  Glándulas, Límites de Superficie, Sistema de Eje Ternario")
            print()


if __name__ == "__main__":
    asyncio.run(generate_all())
