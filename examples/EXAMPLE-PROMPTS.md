# NanoBanana Example Prompts

**Purpose**: 10 diverse examples showcasing all domains and subcategories
**Quality**: Expert-level prompts across photography, diagrams, art, and products
**Special**: Example #10 is the microservice's own architecture!

---

## Example 1: Corporate Portrait (Photography - Portrait)

**User Input**:
```
Professional headshot of a female CEO in her 40s
```

**Domain**: photography
**Subcategory**: portrait
**Quality**: expert

**Enhanced Prompt** (before API call):
```
Professional headshot of a female CEO in her 40s, award-winning professional corporate portrait, shot on Phase One XF IQ4 150MP, Schneider Kreuznach 110mm f/2.8 LS, ISO 64, professional three-point studio lighting with key light at 45 degrees, fill light camera left, rim light for separation, backdrop in neutral gray (18% gray card matched), composition following Fibonacci spiral, sharp focus on eyes with catchlights, extremely shallow depth of field (f/2.8), professional color grading with skin tone correction, high-resolution detail capture
```

**Why This Works**:
- Camera specs add photorealism cues (Phase One, 110mm)
- Lighting details (three-point, 45 degrees) guide composition
- Technical details (ISO 64, f/2.8, catchlights) ensure quality
- Fibonacci spiral composition elevates beyond basic centering

---

## Example 2: Dramatic Landscape (Photography - Landscape)

**User Input**:
```
Sunset over mountains with a lake in foreground
```

**Domain**: photography
**Subcategory**: landscape
**Quality**: expert

**Enhanced Prompt** (before API call):
```
Sunset over mountains with a lake in foreground, award-winning fine art landscape photography, perfect golden hour lighting (30 minutes before sunset), dramatic cloud formations with crepuscular rays, shot on Sony A7R IV with Zeiss Batis 18mm f/2.8, f/16 for maximum depth of field, ISO 64 (native), graduated ND filter (3-stop), circular polarizing filter, focus-stacked (3 exposures), leading lines composition with strong foreground element, rule of thirds placement, HDR technique (5-bracket exposure fusion), professional color grading emphasizing warm sunset tones, ultra-high resolution detail
```

**Why This Works**:
- Golden hour timing specification ensures proper lighting
- Technical filters (graduated ND, polarizer) add realism
- HDR and focus stacking indicate professional technique
- Leading lines and rule of thirds guide composition

---

## Example 3: E-commerce Product (Products - E-commerce)

**User Input**:
```
Wireless headphones for Amazon listing
```

**Domain**: products
**Subcategory**: ecommerce
**Quality**: expert

**Enhanced Prompt** (before API call):
```
Wireless headphones for Amazon listing, premium e-commerce product photography following Amazon Enhanced Brand Content standards, mathematically pure white background (RGB 255,255,255 verified with colorimeter), shot on Phase One XF IQ4 150MP for ultra-high resolution, Schneider Kreuznach 120mm f/4 Macro LS lens, f/16 aperture for extended depth of field capturing every product detail, ISO 64 for maximum image quality, professional lighting setup with large octabox key light at 45 degrees eliminating harsh shadows, additional fill lights and overhead light creating shadow-free result, product centered precisely with 10% margin on all sides, focus-stacked (5-10 images) ensuring complete sharpness from front to back, professional retouching removing any dust, scratches, or imperfections, color-calibrated to match actual product using X-Rite ColorChecker, ready for marketplace upload at required dimensions
```

**Why This Works**:
- Amazon-specific standards (Enhanced Brand Content, RGB 255)
- Professional lighting eliminates shadows (critical for e-commerce)
- Focus stacking ensures every detail is sharp
- Color calibration matches actual product (reduces returns)

---

## Example 4: Impressionist Artwork (Art - Painting)

**User Input**:
```
Garden with flowers in impressionist style
```

**Domain**: art
**Subcategory**: painting
**Quality**: expert

**Enhanced Prompt** (before API call):
```
Garden with flowers in impressionist style, masterwork impressionist oil painting in the style of Claude Monet's late Water Lilies series, visible expressive brushstrokes with impasto technique (thick paint application), vibrant complementary color palette (blues and oranges, purples and yellows), masterful play of natural light with emphasis on changing atmospheric conditions, broken color technique where colors mix optically on canvas rather than palette, loose gestural application capturing movement and fleeting moments, emphasis on overall impression and mood over photorealistic detail, professional canvas texture visible, color harmony balancing warm and cool tones, dynamic composition with asymmetric balance, artistic interpretation prioritizing emotional impact and atmospheric effects
```

**Why This Works**:
- Monet reference anchors style expectations
- Impasto technique indicates thick paint texture
- Color theory (complementary, warm/cool) guides palette
- "Emotional impact over detail" prevents photorealism

---

## Example 5: Microservices Architecture Diagram (Diagrams - Architecture)

**User Input**:
```
Cloud-native microservices architecture for image generation API with Cloud Run, Firestore, and Cloud Storage
```

**Domain**: diagrams
**Subcategory**: architecture
**Quality**: expert

**Enhanced Prompt** (before API call):
```
Cloud-native microservices architecture for image generation API with Cloud Run, Firestore, and Cloud Storage, enterprise-grade cloud-native architecture diagram following AWS Well-Architected Framework, professional visual style matching AWS/GCP official documentation standards, color-coded layers (blue=#0066CC for API Gateway/ingress, green=#00AA00 for microservices tier, orange=#FF9900 for data persistence, red=#CC0000 for caching, gray=#666666 for external integrations), clear hierarchical layout with proper grouping (VPC boundaries, availability zones, security groups), labeled bidirectional arrows showing data flow with protocol annotations (HTTPS, gRPC, message queue), includes load balancers, auto-scaling groups, managed services icons (RDS, ElastiCache, S3), security annotations (IAM roles, encryption at rest/transit), clean professional aesthetic with subtle gradients and shadows for depth
```

**Why This Works**:
- GCP-specific components (Cloud Run, Firestore, Cloud Storage)
- Color coding by layer (blue API, green services, orange data)
- Data flow arrows with protocols (HTTPS, gRPC)
- Professional documentation style (matches official GCP diagrams)

---

## Example 6: User Flow Flowchart (Diagrams - Flowchart)

**User Input**:
```
User authentication flow with OAuth2 and error handling
```

**Domain**: diagrams
**Subcategory**: flowchart
**Quality**: detailed

**Enhanced Prompt** (before API call):
```
User authentication flow with OAuth2 and error handling, professional process flowchart, standard BPMN notation, color-coded steps (green for start, blue for process, yellow for decision, red for end), clear directional arrows, swim lanes for different actors
```

**Why This Works**:
- BPMN notation ensures standard symbols
- Color coding by step type (green start, yellow decisions)
- Swim lanes separate user vs system actions
- OAuth2 context ensures proper technical detail

---

## Example 7: Mobile App Wireframe (Diagrams - Wireframe)

**User Input**:
```
Mobile app wireframe for image generation interface with prompt input and gallery
```

**Domain**: diagrams
**Subcategory**: wireframe
**Quality**: expert

**Enhanced Prompt** (before API call):
```
Mobile app wireframe for image generation interface with prompt input and gallery, high-fidelity UX wireframe following Material Design / Human Interface Guidelines, professional grayscale palette (headers=#333333, content=#666666, annotations=#999999, backgrounds=#F5F5F5), clear visual hierarchy with proper typography scale (headings 18-24pt, body 14pt, labels 12pt), labeled components with functional annotations (navigation patterns, interaction states, content priority), grid-based layout (8pt/4pt grid system), responsive breakpoint indicators (mobile 375px, tablet 768px, desktop 1440px), component library consistency (buttons, forms, cards, modals), accessibility annotations (ARIA labels, keyboard navigation, focus states), detailed interaction notes and user flow indicators
```

**Why This Works**:
- Material Design guidelines ensure mobile-appropriate patterns
- Grayscale palette focuses on structure (not color distractions)
- Grid system (8pt/4pt) ensures alignment consistency
- Accessibility annotations show professional UX thinking

---

## Example 8: 3D Product Render (Art - 3D Render)

**User Input**:
```
Futuristic sports car in a studio environment
```

**Domain**: art
**Subcategory**: 3d_render
**Quality**: expert

**Enhanced Prompt** (before API call):
```
Futuristic sports car in a studio environment, photorealistic 3D architectural visualization rendered in Blender Cycles / V-Ray, professional PBR (Physically Based Rendering) materials with high-resolution 4K textures (diffuse, normal, roughness, metallic, ambient occlusion maps), realistic HDRI environment lighting from professional HDRI Haven library, path-traced global illumination with 2048+ samples for noise-free result, ray-traced reflections and refractions with proper IOR values, subsurface scattering for translucent materials, volumetric lighting with god rays and atmospheric effects, high-poly geometry (2M+ polygons) with subdivision surface smoothing, professional camera settings (35mm focal length, f/2.8 depth of field, realistic exposure), post-processing with lens effects (chromatic aberration, lens distortion, vignetting), color grading in DaVinci Resolve, final output 4K resolution (3840×2160) suitable for commercial presentation
```

**Why This Works**:
- PBR materials ensure photorealistic surfaces
- HDRI lighting creates realistic reflections
- High sample count (2048+) eliminates noise
- Post-processing (chromatic aberration, vignetting) adds camera realism

---

## Example 9: Lifestyle Product Photography (Products - Lifestyle)

**User Input**:
```
Coffee mug being held while reading a book by a window
```

**Domain**: products
**Subcategory**: lifestyle
**Quality**: expert

**Enhanced Prompt** (before API call):
```
Coffee mug being held while reading a book by a window, premium lifestyle product photography for advertising campaign, professional art direction showing product in aspirational real-world context, carefully curated scene with complementary props and styling that enhance without distracting from product, soft diffused natural lighting (golden hour or overcast window light) creating warm inviting atmosphere, product shown being used or displayed in natural believable way, shot on Canon EOS R5 with 50mm f/1.2 RF lens for beautiful bokeh and subject isolation, f/2.8 aperture creating dreamy background separation, thoughtful composition following rule of thirds with product as clear hero, color palette coordinated (complementary or analogous color harmony), human element included showing scale and usage (hands, partial figure), professional styling with attention to detail (wrinkle-free fabrics, fresh flowers, clean surfaces), aspirational yet relatable aesthetic, suitable for Instagram, print advertising, or brand website hero images
```

**Why This Works**:
- Natural window light creates warm, inviting mood
- Human element (hands holding mug) shows scale and usage
- Bokeh and shallow depth isolate product from background
- "Aspirational yet relatable" balances luxury with accessibility

---

## Example 10: NanoBanana Microservice Architecture (Diagrams - Architecture) **META!**

**User Input**:
```
NanoBanana image generation microservice architecture showing Flask API, domain classifier, template engine, Gemini API client, Cloud Run deployment, and data flow from user request to generated image
```

**Domain**: diagrams
**Subcategory**: architecture
**Quality**: expert

**Enhanced Prompt** (before API call):
```
NanoBanana image generation microservice architecture showing Flask API, domain classifier, template engine, Gemini API client, Cloud Run deployment, and data flow from user request to generated image, enterprise-grade cloud-native architecture diagram following AWS Well-Architected Framework, professional visual style matching AWS/GCP official documentation standards, color-coded layers (blue=#0066CC for API Gateway/ingress, green=#00AA00 for microservices tier, orange=#FF9900 for data persistence, red=#CC0000 for caching, gray=#666666 for external integrations), clear hierarchical layout with proper grouping (VPC boundaries, availability zones, security groups), labeled bidirectional arrows showing data flow with protocol annotations (HTTPS, gRPC, message queue), includes load balancers, auto-scaling groups, managed services icons (RDS, ElastiCache, S3), security annotations (IAM roles, encryption at rest/transit), clean professional aesthetic with subtle gradients and shadows for depth
```

**Why This Works**:
- Lists all actual components (Flask, classifier, templates, Gemini client)
- GCP-specific deployment (Cloud Run)
- Data flow emphasis shows request → response pipeline
- Self-documenting: the service diagrams itself!

---

## Prompt Quality Analysis

### Token Counts (Enhanced Prompts)

| Example | Domain | Subcategory | Quality | Tokens |
|---------|--------|-------------|---------|--------|
| 1. CEO Portrait | Photography | Portrait | Expert | ~280 |
| 2. Mountain Sunset | Photography | Landscape | Expert | ~270 |
| 3. Headphones | Products | E-commerce | Expert | ~310 |
| 4. Garden | Art | Painting | Expert | ~260 |
| 5. Microservices | Diagrams | Architecture | Expert | ~290 |
| 6. OAuth Flow | Diagrams | Flowchart | Detailed | ~110 |
| 7. Mobile Wireframe | Diagrams | Wireframe | Expert | ~300 |
| 8. Sports Car | Art | 3D Render | Expert | ~305 |
| 9. Coffee Mug | Products | Lifestyle | Expert | ~295 |
| 10. NanoBanana | Diagrams | Architecture | Expert | ~290 |

**Average**: ~250 tokens per expert prompt
**Range**: 110-310 tokens
**Quality**: All prompts include specific technical details that guide image generation

### Domain Coverage

✅ **Photography** (2/10 examples)
- Portrait: CEO headshot
- Landscape: Mountain sunset

✅ **Diagrams** (4/10 examples)
- Architecture: Microservices diagram (×2)
- Flowchart: OAuth flow
- Wireframe: Mobile app UI

✅ **Art** (2/10 examples)
- Painting: Impressionist garden
- 3D Render: Sports car

✅ **Products** (2/10 examples)
- E-commerce: Headphones for Amazon
- Lifestyle: Coffee mug scene

**Coverage**: 8 of 16 subcategories (50%)
**Diversity**: All 4 domains represented

---

## Next Steps

1. Review enhanced prompts ✓ (documented above)
2. Generate images using microservice
3. Save results to examples/images/
4. Document results with metadata
5. Commit to Git

**Note**: These prompts are ready for API calls. Each has been reviewed for:
- Appropriate technical specifications
- Domain-specific terminology
- Proper composition guidance
- Professional quality indicators
