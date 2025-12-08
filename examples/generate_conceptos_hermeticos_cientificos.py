#!/usr/bin/env python3
"""
Generar Suite de Conceptos Herméticos-Científicos (Español)
===========================================================

6 visualizaciones profundas uniendo sabiduría antigua y ciencia moderna:
- H01: LA UNIDAD (Schwaller de Lubicz)
- H02: Servus Fugitivus (Sirviente alquímico)
- H03: Spiritus Domini Ferebatur Super Aquas (Espíritu sobre las aguas)
- H04: Solve et Coagula (Transformación alquímica)
- H05: Porfirinas Elixir Maestro (Activación molecular luz-sonido)
- H06: Equivalencia Computacional Maestro (Principio de Wolfram)

Modelo: Gemini 3 Pro Image (texto perfecto, alta calidad)
Costo: $0.12 por imagen × 6 = $0.72 total
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
    {
        "id": "H01",
        "title": "LA UNIDAD - Conciencia Indivisible",
        "filename": "H01-la-unidad.png",
        "description": "Mandala de geometría sagrada expresando el principio de unidad de Schwaller de Lubicz"
    },
    {
        "id": "H02",
        "title": "Servus Fugitivus - El Sirviente Fugitivo",
        "filename": "H02-servus-fugitivus.png",
        "description": "Mercurio alquímico - el sirviente volátil de la transformación"
    },
    {
        "id": "H03",
        "title": "Spiritus Domini Ferebatur Super Aquas",
        "filename": "H03-spiritus-domini.png",
        "description": "Espíritu divino moviéndose sobre aguas primordiales - visualización del Génesis"
    },
    {
        "id": "H04",
        "title": "Solve et Coagula",
        "filename": "H04-solve-et-coagula.png",
        "description": "Ciclo alquímico de disolución y coagulación"
    },
    {
        "id": "H05",
        "title": "Porfirinas Elixir Maestro",
        "filename": "H05-porfirinas-elixir.png",
        "description": "Sabiduría molecular - activación de luz y sonido de la estructura central de la vida"
    },
    {
        "id": "H06",
        "title": "Equivalencia Computacional Maestro",
        "filename": "H06-equivalencia-computacional.png",
        "description": "Principio de Wolfram - reglas simples alcanzando complejidad universal"
    }
]


async def generate_all():
    """Generate all Hermetic-Scientific concept images in Spanish"""

    # Setup paths
    prompts_dir = Path(__file__).parent / "Conceptos Herméticos-Científicos"
    output_dir = prompts_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("🔮 SUITE DE CONCEPTOS HERMÉTICOS-CIENTÍFICOS")
    print("=" * 70)
    print()
    print("Sabiduría Antigua ∩ Ciencia Moderna")
    print()
    print(f"Modelo: Gemini 3 Pro Image (gemini-3-pro-image-preview)")
    print(f"Conceptos: {len(CONCEPTS)}")
    print(f"Costo Esperado: ${len(CONCEPTS) * 0.12:.2f}")
    print()
    print("=" * 70)
    print()

    async with GeminiClient() as client:
        total_size = 0
        successful = 0
        failed = 0

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
                print(f"    ❌ ERROR: {e}")

            print()

        # Summary
        print("=" * 70)
        print("📊 RESUMEN DE GENERACIÓN")
        print("=" * 70)
        print()
        print(f"✅ Exitosos: {successful}/{len(CONCEPTS)}")
        print(f"❌ Fallidos: {failed}/{len(CONCEPTS)}")
        print(f"📦 Tamaño Total: {total_size:.2f} MB")
        print(f"💰 Costo Real: ${successful * 0.12:.2f}")
        print(f"📂 Salida: {output_dir.relative_to(Path.cwd())}")
        print()

        if successful == len(CONCEPTS):
            print("🎉 ¡ÉXITO COMPLETO - TODOS LOS CONCEPTOS HERMÉTICOS-CIENTÍFICOS GENERADOS!")
        elif successful > 0:
            print(f"⚠️  ÉXITO PARCIAL - {successful} de {len(CONCEPTS)} generados")
        else:
            print("❌ GENERACIÓN FALLIDA - No se crearon imágenes")

        print()
        print("=" * 70)
        print()

        # Concept guide
        if successful > 0:
            print("🔮 GUÍA DE CONCEPTOS HERMÉTICOS-CIENTÍFICOS")
            print("=" * 70)
            print()
            for concept in CONCEPTS:
                print(f"**{concept['title']}**")
                print(f"  {concept['description']}")
                print()


if __name__ == "__main__":
    asyncio.run(generate_all())
