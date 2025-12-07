# Google Gemini & Imagen Image Generation Models - Comprehensive Analysis

**Research Date**: December 7, 2025
**Target**: nanobanana-repo project
**Focus**: Technical diagram generation with accurate text rendering

---

## Executive Summary

Google offers three primary image generation models via the Gemini API, each with distinct capabilities and trade-offs. For technical diagram generation with accurate text rendering, **Gemini 3 Pro Image (Nano Banana Pro)** delivers state-of-the-art performance at 2K-4K resolution, while **Gemini 2.5 Flash Image (Nano Banana)** provides a fast, cost-effective alternative ranked #1 on LMArena benchmarks. Imagen 3 remains a specialized text-to-image model focused on photorealistic quality.

### Quick Model Selection Guide

| Use Case | Recommended Model | Why |
|----------|------------------|-----|
| Technical diagrams with text | **Gemini 3 Pro Image** | State-of-the-art text rendering, 2K-4K resolution |
| Fast diagram prototyping | **Gemini 2.5 Flash Image** | 3x cheaper, ranked #1 on benchmarks, good text quality |
| Photorealistic images | **Imagen 3** | Specialized for photorealism, not conversational |
| Iterative refinement workflows | **Gemini 3 Pro Image** | Multi-turn support, up to 14 reference images |
| Budget-conscious production | **Gemini 2.5 Flash Image** | $0.039/image vs $0.12/image for Pro |

---

## Table of Contents

- [Available Models](#available-models)
- [Model Capabilities Comparison](#model-capabilities-comparison)
- [Technical Diagram Generation](#technical-diagram-generation)
- [API Endpoints & Integration](#api-endpoints--integration)
- [Pricing Analysis](#pricing-analysis)
- [Prompt Engineering Best Practices](#prompt-engineering-best-practices)
- [Model Selection Decision Matrix](#model-selection-decision-matrix)
- [Implementation Examples](#implementation-examples)
- [Known Limitations](#known-limitations)
- [Troubleshooting Guide](#troubleshooting-guide)
- [References](#references)

---

## Available Models

### 1. Gemini 2.5 Flash Image (Nano Banana)

**Model ID**: `gemini-2.5-flash-image`
**Codename**: "Nano Banana"
**Status**: Production-ready (October 2025)
**Best for**: Fast, cost-effective image generation with good text rendering

#### Key Specifications

| Feature | Value |
|---------|-------|
| Input Token Limit | 65,536 tokens |
| Output Token Limit | 32,768 tokens |
| Tokens per Image | 1,290 tokens |
| Input Modalities | Text, Images |
| Output Modalities | Text, Images (must include both) |
| Latest Update | October 2025 |

#### Capabilities

- **Text-to-image generation**: Create images from descriptive prompts
- **Image editing**: Targeted transformations using natural language
- **Character consistency**: Maintain same subject across multiple generations
- **Multi-image fusion**: Blend multiple images seamlessly
- **Conversational refinement**: Iterative improvements over multiple turns
- **Aspect ratio control**: 10 ratios (1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9)
- **SynthID watermarking**: Invisible digital signature on all outputs

#### Performance Benchmarks

- **LMArena Ranking**: #1 for Text-to-Image and Image Editing (as of August 25, 2025)
- **Text Rendering**: 8 of 12 prompts correct in strict text-to-image tests
- **Quality**: Approaches Imagen and gpt-image-1 in benchmarks
- **Speed**: 3-5 seconds per generation (typical)

#### Pricing

- **Token-based**: $30.00 per 1 million output tokens
- **Per image**: ~$0.039 per 1 megapixel image (1024x1024)
- **Comparison**: ~4.4x cheaper than gpt-image-1 ($0.17/image)

---

### 2. Gemini 3 Pro Image (Nano Banana Pro)

**Model ID**: `gemini-3-pro-image-preview`
**Codename**: "Nano Banana Pro"
**Status**: Preview (November 2025)
**Best for**: Professional-grade technical diagrams, high-resolution output

#### Key Specifications

| Feature | Value |
|---------|-------|
| Input Token Limit | 65,536 tokens |
| Output Token Limit | 32,768 tokens |
| Input Modalities | Text, Images |
| Output Modalities | Text, Images |
| Maximum Resolution | 4K (4096px) |
| Reference Images | Up to 14 images |
| Latest Update | November 2025 |

#### Capabilities

- **State-of-the-art text rendering**: Clear, accurate text integrated in images
- **High-resolution output**: Native 1K, 2K, 4K generation
- **Multi-turn workflows**: Conversational image refinement
- **Long-context prompts**: Support for complex, detailed instructions
- **Google Search grounding**: Real-time data integration for fact-based imagery
- **Thinking mode**: Shows interim image generation process
- **Advanced editing**: Precise local transformations

#### Advanced Features

1. **Professional Asset Production**
   - Product mockups with accurate branding
   - Logos with legible, stylized text
   - Infographics with data visualization
   - Storyboards with consistent characters

2. **Technical Precision**
   - Biological diagrams with labeled components
   - Historical maps with accurate text
   - Architectural drawings with annotations
   - Engineering schematics with specifications

3. **Robust World Knowledge**
   - Built on Gemini 3 Pro's reasoning capabilities
   - Factual accuracy in data-driven visuals
   - Contextual understanding of domain-specific terminology

#### Pricing

- **Per image**: ~$0.12 per image (starts at this baseline)
- **Comparison**: ~20% cheaper than official Google pricing via some API providers
- **Premium tier**: Higher cost reflects advanced capabilities

---

### 3. Imagen 3

**Model ID**: `imagen-3.0-generate-002`
**Status**: Stable (February 2025 update)
**Best for**: Photorealistic image generation, single-shot quality

#### Key Specifications

| Feature | Value |
|---------|-------|
| Input Prompt Limit | 480 tokens |
| Images per Generation | Up to 4 images |
| Aspect Ratios | 1:1, 3:4, 4:3, 9:16, 16:9 |
| Watermarking | SynthID included |
| API Access | Via Gemini API |

#### Capabilities

- **High-fidelity photorealism**: Unparalleled realistic image generation
- **Text-in-image**: Can generate text within images (with limitations)
- **Multiple outputs**: Generate up to 4 variations per request
- **Photography styles**: Supports various lens types, focal lengths, techniques
- **Art styles**: Historical and contemporary artistic rendering
- **Aspect ratio control**: 5 standard ratios supported

#### Key Differences from Gemini Models

| Feature | Imagen 3 | Gemini Models |
|---------|----------|---------------|
| **Primary Focus** | Photorealistic single-shot generation | Conversational, iterative refinement |
| **Multi-turn Support** | No | Yes |
| **Reference Images** | No | Yes (up to 14 for Pro) |
| **Text Rendering** | Limited | Advanced (especially Pro) |
| **Resolution** | Standard | Up to 4K (Pro model) |
| **Google Search Grounding** | No | Yes (Pro model) |
| **Best Use Case** | Final photorealistic renders | Technical diagrams, iterative workflows |

#### Pricing

- **Per image**: ~$0.03 per image
- **Control**: Aspect ratio and number of outputs
- **Note**: Separate pricing from Gemini models

---

### 4. Gemini 2.0 Flash Image (DEPRECATED - Legacy Preview)

**Model ID**: `gemini-2.0-flash-preview-image-generation`
**Status**: ⚠️ **DEPRECATED** - Use `gemini-2.5-flash-image` instead
**Geographic Restrictions**: Not supported in many European, Middle Eastern, and African countries

> **Migration Note**: This model is deprecated. New projects should use `gemini-2.5-flash-image` (Flash) or `gemini-3-pro-image-preview` (Pro) for production quality. The 2.0 model has lower token limits and reduced text rendering accuracy compared to current models.

#### Key Specifications

| Feature | Value |
|---------|-------|
| Input Token Limit | 32,768 tokens (lower than 2.5) |
| Output Token Limit | 8,192 tokens (lower than 2.5) |
| Input Modalities | Audio, Images, Video, Text |
| Output Modalities | Text, Images |

#### Why Choose Newer Models Instead

- **Lower token limits**: Half the capacity of Gemini 2.5 Flash Image
- **Geographic restrictions**: Limited availability
- **Superseded**: Gemini 2.5 Flash Image offers superior performance
- **Benchmark comparison**: Internal benchmarks show 2.5 has stronger text rendering

---

## Model Capabilities Comparison

### Text Rendering Quality

| Model | Text Rendering Quality | Best Use Case |
|-------|----------------------|---------------|
| **Gemini 3 Pro Image** | ★★★★★ State-of-the-art | Complex technical diagrams, multi-line labels, small text |
| **Gemini 2.5 Flash Image** | ★★★★☆ Excellent | Short labels, titles, simple diagrams |
| **Imagen 3** | ★★★☆☆ Good | Limited text, decorative elements |
| **Gemini 2.0 Flash Image** | ★★☆☆☆ Fair | Avoid for text-heavy content |

#### Text Rendering Benchmark Results

**Gemini 3 Pro Image**:
- Sharp, legible text at 2K-4K resolution
- Accurate rendering of long text strings
- Minimal spelling errors or formatting issues
- Suitable for professional documentation

**Gemini 2.5 Flash Image**:
- 8 of 12 strict text prompts correct in benchmarks
- Significantly improved over 2.0 Flash
- Approaches best-in-class models (Imagen, gpt-image-1)
- Good for most technical diagram needs

**Known Text Rendering Challenges** (all models):
- Long sequences of text may have formatting issues
- Small font sizes can become illegible
- Complex mathematical notation requires careful prompting
- Multiple text blocks increase error probability

### Technical Diagram Capabilities

#### Supported Diagram Types

| Diagram Type | Gemini 3 Pro | Gemini 2.5 Flash | Imagen 3 | Notes |
|--------------|--------------|------------------|----------|-------|
| **Infographics** | Excellent | Very Good | Good | Pro handles complex data viz better |
| **Flowcharts** | Excellent | Good | Fair | Pro maintains better structure |
| **Architecture Diagrams** | Excellent | Good | Fair | Pro handles technical detail |
| **Biological Diagrams** | Excellent | Good | Good | Pro provides more accurate labels |
| **Network Diagrams** | Very Good | Good | Fair | Complex connections favor Pro |
| **UI Mockups** | Excellent | Very Good | Good | Pro handles pixel-perfect detail |
| **Logos** | Excellent | Very Good | Very Good | All models handle well |
| **Posters** | Excellent | Very Good | Excellent | Imagen excels at artistic posters |
| **Maps** | Excellent | Good | Good | Pro handles labeling better |
| **Engineering Schematics** | Excellent | Good | Fair | Pro essential for precision |

#### Feature Comparison Matrix

```
┌─────────────────────────────┬──────────────┬──────────────┬──────────┐
│ Feature                     │ 3 Pro Image  │ 2.5 Flash    │ Imagen 3 │
├─────────────────────────────┼──────────────┼──────────────┼──────────┤
│ Multi-turn Refinement       │ ✓ Excellent  │ ✓ Good       │ ✗        │
│ Reference Image Support     │ ✓ Up to 14   │ ✓ Multiple   │ ✗        │
│ High-Res Output (4K)        │ ✓            │ ✗ (1K max)   │ ✗        │
│ Text Rendering Quality      │ ★★★★★        │ ★★★★☆        │ ★★★☆☆    │
│ Google Search Grounding     │ ✓            │ ✗            │ ✗        │
│ Thinking Mode               │ ✓            │ ✗            │ ✗        │
│ Character Consistency       │ ✓ Excellent  │ ✓ Good       │ ✗        │
│ Multi-image Fusion          │ ✓            │ ✓            │ ✗        │
│ Aspect Ratio Options        │ 10 ratios    │ 10 ratios    │ 5 ratios │
│ Generation Speed            │ Slower       │ Fast         │ Medium   │
│ Cost per Image              │ $0.12        │ $0.039       │ $0.03    │
│ Best for Technical Diagrams │ ✓            │ ✓            │ ✗        │
└─────────────────────────────┴──────────────┴──────────────┴──────────┘
```

---

## Technical Diagram Generation

### Text Rendering Best Practices

#### Why Text Rendering Matters

Most image generation models struggle with accurate text rendering, resulting in:
- Poorly formatted characters
- Spelling errors and gibberish
- Illegible small text
- Inconsistent font styles
- Text running off image boundaries

**Gemini models address this** through:
1. **Advanced language understanding**: Built on Gemini 3 Pro's reasoning
2. **High-resolution output**: Native 2K-4K for sharp text (Pro)
3. **Iterative refinement**: Fix text issues conversationally
4. **Photographic precision**: Control text placement and styling

#### Prompt Engineering for Text Clarity

**Basic Template**:
```
Create a [image type] for [brand/concept] with the text '[exact text]'
in a [font style] font, [additional design context]
```

**Example - Technical Diagram**:
```
Create a system architecture diagram showing the nanobanana-repo
microservices architecture. Include the following labeled components:

1. "API Gateway" (top, blue box)
2. "Image Service" (middle-left, green box)
3. "Storage Service" (middle-right, orange box)
4. "Database" (bottom, gray cylinder)

Use a clean, professional style with sans-serif labels in black text.
Include arrows showing data flow between components.
```

**Example - Infographic**:
```
Design a vertical infographic explaining "The Image Generation Pipeline".
Include these exact text sections:

Title: "Image Generation Pipeline" (bold, top)
Step 1: "Prompt Engineering" - Write detailed descriptions
Step 2: "Model Selection" - Choose appropriate AI model
Step 3: "Generation" - Create initial image
Step 4: "Refinement" - Iterative improvements

Use a modern gradient background (blue to purple) with white text
and circular icons for each step.
```

#### Common Text Rendering Issues & Solutions

| Issue | Symptom | Solution |
|-------|---------|----------|
| **Misspelled words** | Text contains errors | Explicitly state "spelled correctly as '[exact text]'" |
| **Text overflow** | Text runs off image | Specify "ensure all text fits within image boundaries" |
| **Illegible small text** | Can't read labels | Request "large, legible text" or increase image size |
| **Inconsistent fonts** | Mixed font styles | Specify exact font: "sans-serif font throughout" |
| **Poor contrast** | Text hard to read | Request "high contrast between text and background" |
| **Misplaced text** | Labels in wrong position | Use spatial language: "text positioned at top-center" |

### Diagram-Specific Prompting Strategies

#### 1. System Architecture Diagrams

**Prompt Structure**:
```
Create a [style] system architecture diagram showing [system name].

Components (with exact labels):
- [Component 1 name]: [description, position, color]
- [Component 2 name]: [description, position, color]
- [Component 3 name]: [description, position, color]

Connections:
- [Component 1] → [Component 2]: [label, arrow style]
- [Component 2] → [Component 3]: [label, arrow style]

Style: [design specifications]
Text: [font and size requirements]
Layout: [horizontal/vertical, spacing]
```

**Example**:
```
Create a clean, professional system architecture diagram showing
the "Nanobanana Image Generation System".

Components (with exact labels in sans-serif font):
- "Client App" (top-left, light blue rounded rectangle)
- "Gemini API" (top-right, green rounded rectangle)
- "Image Storage" (bottom-center, orange cylinder)
- "CDN" (bottom-right, purple cloud shape)

Connections (with black arrows):
- "Client App" → "Gemini API": labeled "HTTP Request"
- "Gemini API" → "Image Storage": labeled "Save Image"
- "Image Storage" → "CDN": labeled "Distribute"
- "CDN" → "Client App": labeled "Deliver Image" (dashed line)

Style: Minimalist with subtle shadows, white background
Text: All labels in 14pt sans-serif, black color
Layout: Hierarchical top-to-bottom flow with equal spacing
```

#### 2. Flowcharts

**Prompt Structure**:
```
Create a [orientation] flowchart showing [process name].

Steps (with exact labels):
- Start: [label, shape]
- Step 1: [label, shape, condition if any]
- Step 2: [label, shape, condition if any]
- End: [label, shape]

Decision points:
- [Question]: [yes/no branches]

Style: [color scheme, connector style]
```

**Example**:
```
Create a vertical flowchart showing "Image Generation Decision Flow".

Steps (with exact labels in bold):
- Start: "Receive Image Request" (green rounded rectangle)
- Decision: "Text rendering required?" (yellow diamond)
  - Yes → "Use Gemini 3 Pro Image" (blue rectangle)
  - No → "Check budget constraints" (yellow diamond)
    - High quality → "Use Gemini 3 Pro Image" (blue rectangle)
    - Cost-effective → "Use Gemini 2.5 Flash" (blue rectangle)
- End: "Generate Image" (green rounded rectangle)

Style: Clean business flowchart with consistent spacing
Connectors: Black arrows with clear yes/no labels
Background: Light gray gradient
```

#### 3. Infographics

**Prompt Structure**:
```
Design a [orientation] infographic titled "[exact title]"
about [topic].

Sections:
1. [Section 1 title]: [content, visual elements]
2. [Section 2 title]: [content, visual elements]
3. [Section 3 title]: [content, visual elements]

Visual style: [color scheme, iconography, typography]
Layout: [grid, flow, hierarchy]
```

**Example**:
```
Design a vertical infographic titled "Gemini Model Comparison"
about choosing the right image generation model.

Sections:
1. Header: "Gemini Model Comparison" (bold, 24pt, centered)
2. "Gemini 2.5 Flash" (left column):
   - Icon: Lightning bolt
   - "Fast & Affordable" (subheading)
   - "$0.039/image" (large number)
   - "Best for: Prototypes" (small text)
3. "Gemini 3 Pro" (right column):
   - Icon: Star
   - "Professional Quality" (subheading)
   - "$0.12/image" (large number)
   - "Best for: Production" (small text)
4. Footer: "Choose based on your needs" (italic, 12pt)

Visual style: Modern gradient (blue to purple), white text
Layout: Two-column comparison with centered header/footer
Icons: Simple line icons in white
```

#### 4. Network Diagrams

**Prompt Structure**:
```
Create a network diagram showing [network name/topology].

Nodes:
- [Node 1]: [type, position, label]
- [Node 2]: [type, position, label]

Connections:
- [Node 1] ↔ [Node 2]: [connection type, label]

Labels: [specific text requirements]
Legend: [symbol explanations]
```

### Resolution and Aspect Ratio Selection

#### Recommended Settings by Diagram Type

| Diagram Type | Aspect Ratio | Resolution | Model |
|--------------|--------------|------------|-------|
| **System Architecture** | 16:9 or 4:3 | 2K-4K | Gemini 3 Pro |
| **Flowchart** | 2:3 or 3:4 (portrait) | 2K | Gemini 3 Pro or 2.5 Flash |
| **Infographic** | 2:3 or 9:16 (portrait) | 4K | Gemini 3 Pro |
| **Logo** | 1:1 | 2K | Any model |
| **Banner** | 16:9 or 21:9 | 2K-4K | Gemini 3 Pro |
| **Social Media Post** | 1:1 or 4:5 | 1K-2K | Gemini 2.5 Flash |
| **Presentation Slide** | 16:9 | 2K | Gemini 2.5 Flash |

#### Aspect Ratio Support

**All Gemini Models** (2.5 Flash, 3 Pro):
- 1:1 (square)
- 3:2, 2:3 (classic photo)
- 3:4, 4:3 (standard display)
- 4:5, 5:4 (social media)
- 9:16, 16:9 (widescreen)
- 21:9 (ultra-wide)

**Imagen 3**:
- 1:1, 3:4, 4:3, 9:16, 16:9

### Iterative Refinement Workflow

One of Gemini's key advantages is **multi-turn conversational refinement**:

#### Example Workflow

**Turn 1 - Initial Generation**:
```
User: Create a system architecture diagram for a microservices
application with API Gateway, User Service, and Database.
```

**Turn 2 - Add Details**:
```
User: Add labels to the arrows showing HTTP requests between components.
```

**Turn 3 - Style Adjustment**:
```
User: Make the text larger and use a blue color scheme for the boxes.
```

**Turn 4 - Final Polish**:
```
User: Add a title "Microservices Architecture" at the top in bold.
```

#### Best Practices for Refinement

1. **Start broad, refine narrow**: Initial prompt with overall structure, then specific adjustments
2. **One change per turn**: Easier to track and undo if needed
3. **Be specific about changes**: "Make text larger" vs "Increase font size to 18pt"
4. **Use reference images**: Upload existing diagrams to maintain consistency
5. **Verify text accuracy**: Check each iteration for spelling/formatting issues

---

## API Endpoints & Integration

### Gemini API Structure

**Base URL**:
```
https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent
```

**Available Models** (substitute for `{model}`):
- `gemini-2.5-flash-image` (production)
- `gemini-3-pro-image-preview` (preview)
- `gemini-2.0-flash-preview-image-generation` (legacy)

### Authentication

**API Key Required**: Obtain from [Google AI Studio](https://aistudio.google.com)

**Environment Variable**:
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

### Request Structure

#### Required Parameters

1. **responseModalities**: Must include both `TEXT` and `IMAGE`
   ```json
   {
     "responseModalities": ["TEXT", "IMAGE"]
   }
   ```
   **Note**: Image-only output is NOT supported

2. **contents**: Your prompt text
   ```json
   {
     "contents": [
       {
         "parts": [
           {"text": "Create a diagram showing..."}
         ]
       }
     ]
   }
   ```

3. **generationConfig**: Optional settings
   ```json
   {
     "generationConfig": {
       "imageConfig": {
         "aspectRatio": "16:9",
         "imageSize": "2K"
       }
     }
   }
   ```

### Implementation Examples

#### Python (Official SDK)

```python
import google.generativeai as genai
from google.generativeai.types import GenerateContentConfig, Modality

# Configure API
genai.configure(api_key="YOUR_API_KEY")

# Create model instance
model = genai.GenerativeModel("gemini-2.5-flash-image")

# Generate image
response = model.generate_content(
    "Create a technical diagram showing a REST API architecture "
    "with labeled components: 'Client', 'API Gateway', 'Backend Service', 'Database'",
    config=GenerateContentConfig(
        response_modalities=[Modality.TEXT, Modality.IMAGE],
        generation_config={
            "imageConfig": {
                "aspectRatio": "16:9",
                "imageSize": "2K"
            }
        }
    )
)

# Access generated image
for part in response.parts:
    if part.inline_data:
        # Save image
        with open("diagram.png", "wb") as f:
            f.write(part.inline_data.data)
    elif part.text:
        print(f"Model response: {part.text}")
```

#### Python (REST API)

```python
import requests
import base64
import json

API_KEY = "YOUR_API_KEY"
MODEL = "gemini-2.5-flash-image"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Create a flowchart showing the image generation process "
                            "with steps: 'Prompt' → 'Model' → 'Generation' → 'Output'"
                }
            ]
        }
    ],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"],
        "imageConfig": {
            "aspectRatio": "3:4",
            "imageSize": "2K"
        }
    }
}

response = requests.post(URL, json=payload)
result = response.json()

# Extract image data
for candidate in result.get("candidates", []):
    for part in candidate.get("content", {}).get("parts", []):
        if "inlineData" in part:
            # Decode base64 image
            image_data = base64.b64decode(part["inlineData"]["data"])
            with open("flowchart.png", "wb") as f:
                f.write(image_data)
        elif "text" in part:
            print(part["text"])
```

#### JavaScript/TypeScript (Node.js)

```typescript
import { GoogleGenerativeAI } from "@google/generative-ai";
import fs from "fs";

const genAI = new GoogleGenerativeAI("YOUR_API_KEY");
const model = genAI.getGenerativeModel({
  model: "gemini-2.5-flash-image"
});

async function generateDiagram() {
  const result = await model.generateContent({
    contents: [
      {
        parts: [
          {
            text: "Create an infographic titled 'API Request Flow' showing: "
                  + "'User Request' → 'Authentication' → 'Rate Limiting' → 'API Handler'"
          }
        ]
      }
    ],
    generationConfig: {
      responseModalities: ["TEXT", "IMAGE"],
      imageConfig: {
        aspectRatio: "16:9",
        imageSize: "2K"
      }
    }
  });

  const response = await result.response;

  for (const part of response.candidates[0].content.parts) {
    if (part.inlineData) {
      // Save image
      const buffer = Buffer.from(part.inlineData.data, "base64");
      fs.writeFileSync("infographic.png", buffer);
    } else if (part.text) {
      console.log("Model response:", part.text);
    }
  }
}

generateDiagram();
```

#### cURL (REST API)

```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Create a network diagram showing nodes labeled \"Server A\", \"Server B\", and \"Load Balancer\" with connecting lines"
          }
        ]
      }
    ],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "imageConfig": {
        "aspectRatio": "4:3",
        "imageSize": "2K"
      }
    }
  }' | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 -d > network_diagram.png
```

### Multi-turn Refinement API Pattern

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-3-pro-image-preview")

# Start chat session for iterative refinement
chat = model.start_chat(
    config=genai.GenerateContentConfig(
        response_modalities=[genai.Modality.TEXT, genai.Modality.IMAGE]
    )
)

# Turn 1: Initial generation
response1 = chat.send_message(
    "Create a simple architecture diagram with boxes labeled 'Frontend' and 'Backend'"
)

# Save initial image
for part in response1.parts:
    if part.inline_data:
        with open("diagram_v1.png", "wb") as f:
            f.write(part.inline_data.data)

# Turn 2: Refine
response2 = chat.send_message(
    "Add a 'Database' box below 'Backend' with a connecting arrow"
)

# Save refined image
for part in response2.parts:
    if part.inline_data:
        with open("diagram_v2.png", "wb") as f:
            f.write(part.inline_data.data)

# Turn 3: Final polish
response3 = chat.send_message(
    "Make all text larger and use a blue color scheme"
)

# Save final image
for part in response3.parts:
    if part.inline_data:
        with open("diagram_final.png", "wb") as f:
            f.write(part.inline_data.data)
```

### Imagen 3 API (Separate Endpoint)

**Model ID**: `imagen-3.0-generate-002`

**Key Differences**:
- Generates up to 4 images per request
- No multi-turn support
- Simpler configuration

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

# Use Imagen model
response = genai.ImageGenerationModel("imagen-3.0-generate-002").generate_images(
    prompt="A photorealistic image of a modern data center with server racks",
    number_of_images=4,
    aspect_ratio="16:9"
)

# Access multiple generated images
for i, image in enumerate(response.images):
    image.save(f"datacenter_{i}.png")
```

### Configuration Options

#### Image Configuration Parameters

```json
{
  "imageConfig": {
    "aspectRatio": "16:9",      // Options: 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
    "imageSize": "2K"           // Options: "1K", "2K", "4K" (Pro only)
  }
}
```

#### Response Modalities (Required)

```json
{
  "responseModalities": ["TEXT", "IMAGE"]  // Both required, image-only not supported
}
```

#### Safety Settings (Optional)

```json
{
  "safetySettings": [
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
  ]
}
```

---

## Pricing Analysis

### Cost Comparison

| Model | Pricing Model | Per Image Cost | Best Value For |
|-------|--------------|----------------|----------------|
| **Gemini 2.5 Flash Image** | $30/1M output tokens | ~$0.039 | Production workflows, high volume |
| **Gemini 3 Pro Image** | Per-image pricing | ~$0.12 | High-quality final outputs |
| **Imagen 3** | Per-image pricing | ~$0.03 | Photorealistic single-shots |
| **gpt-image-1** (comparison) | Per-image pricing | ~$0.17 | N/A (competitor reference) |

### Cost Breakdown Details

#### Gemini 2.5 Flash Image

- **Pricing**: $30.00 per 1 million output tokens
- **Tokens per image**: 1,290 tokens
- **Calculation**: (1,290 / 1,000,000) × $30 = **$0.0387 per image**
- **Rounded**: ~$0.039 per 1 megapixel image

**Example Usage Costs**:
- 100 images/month: $3.90
- 1,000 images/month: $39.00
- 10,000 images/month: $390.00

**Cost-saving tip**: Use for iterative development and prototyping before final production

#### Gemini 3 Pro Image

- **Pricing**: ~$0.12 per image (baseline, may vary by provider)
- **Premium features**: 4K output, advanced text rendering, multi-turn support
- **Calculation**: 3x cost of 2.5 Flash Image

**Example Usage Costs**:
- 100 images/month: $12.00
- 1,000 images/month: $120.00
- 10,000 images/month: $1,200.00

**Cost-saving tip**: Use selectively for final production assets where quality is critical

#### Imagen 3

- **Pricing**: ~$0.03 per image
- **Control**: Can generate up to 4 images per request
- **Cost for 4 images**: ~$0.12 total

**Example Usage Costs** (single images):
- 100 images/month: $3.00
- 1,000 images/month: $30.00
- 10,000 images/month: $300.00

### ROI Analysis: When to Use Which Model

#### Scenario 1: Technical Documentation Project

**Requirements**: 50 technical diagrams for documentation

| Approach | Model | Cost | Quality | Total Cost |
|----------|-------|------|---------|------------|
| **Budget** | Gemini 2.5 Flash × 50 | $0.039 | Good | $1.95 |
| **Mixed** | 2.5 Flash × 40 + 3 Pro × 10 | $0.039 + $0.12 | Excellent | $2.76 |
| **Premium** | Gemini 3 Pro × 50 | $0.12 | Excellent | $6.00 |

**Recommendation**: Mixed approach - use 2.5 Flash for drafts, 3 Pro for final key diagrams

#### Scenario 2: Marketing Campaign

**Requirements**: 20 high-quality images for social media

| Approach | Model | Cost | Quality | Total Cost |
|----------|-------|------|---------|------------|
| **Fast** | Gemini 2.5 Flash × 20 | $0.039 | Good | $0.78 |
| **Photorealistic** | Imagen 3 × 20 (4 each = 5 requests) | $0.03 × 4 | Excellent | $0.60 |
| **Professional** | Gemini 3 Pro × 20 | $0.12 | Excellent | $2.40 |

**Recommendation**: Imagen 3 for photorealistic scenes, Gemini 3 Pro for text-heavy content

#### Scenario 3: Rapid Prototyping

**Requirements**: 200 iterations during design exploration

| Approach | Model | Cost | Quality | Total Cost |
|----------|-------|------|---------|------------|
| **Cost-effective** | Gemini 2.5 Flash × 200 | $0.039 | Good | $7.80 |
| **Premium** | Gemini 3 Pro × 200 | $0.12 | Excellent | $24.00 |

**Recommendation**: Use 2.5 Flash for exploration, switch to 3 Pro only for final candidates

### Cost Optimization Strategies

1. **Tiered Workflow**:
   - Draft: Gemini 2.5 Flash ($0.039)
   - Review: Select top 20%
   - Refine: Gemini 3 Pro ($0.12) for selected candidates
   - **Savings**: ~70% vs all-Pro approach

2. **Batch Generation**:
   - Use Imagen 3's 4-image generation for variations
   - **Cost**: $0.12 for 4 images = $0.03 per image
   - **Best for**: Photorealistic variations, not technical diagrams

3. **Iterative Refinement**:
   - Use multi-turn chat with same model
   - **Cost**: Same per-image cost, but fewer new generations
   - **Savings**: ~50% vs generating completely new images

4. **Prompt Engineering Investment**:
   - Spend time perfecting prompts with 2.5 Flash (~$0.039 × 10 = $0.39)
   - Use refined prompt for final 3 Pro generation (~$0.12 × 1 = $0.12)
   - **Total**: $0.51 vs $1.20 (10 × 3 Pro attempts)
   - **Savings**: 57%

---

## Prompt Engineering Best Practices

### Core Principle

**"Describe the scene, don't just list keywords"**

A narrative, descriptive paragraph almost always produces better, more coherent images than a simple list of disconnected words.

### Prompt Structure Framework

#### The 5 Elements of Effective Prompts

1. **Subject**: What is being depicted
2. **Composition**: Layout and arrangement
3. **Action**: What's happening (if applicable)
4. **Location/Context**: Where and surrounding elements
5. **Style**: Visual treatment and aesthetic

#### Template

```
[Subject] [doing action] in [location/context],
[composition details], [style specifications]
```

**Example**:
```
A system architecture diagram showing three microservices
(User Service, Order Service, Payment Service) connected through
an API Gateway, arranged horizontally with labeled arrows showing
data flow, in a clean minimalist style with blue boxes and
sans-serif labels
```

### Advanced Prompt Engineering Techniques

#### 1. Photographic Language for Control

Use camera and photography terminology to control composition:

| Term | Effect |
|------|--------|
| **Wide-angle shot** | Broader view, more context |
| **Macro shot** | Extreme close-up, detail focus |
| **Low-angle perspective** | Looking up at subject |
| **High-angle perspective** | Looking down at subject |
| **85mm portrait lens** | Slight compression, flattering |
| **Dutch angle** | Tilted perspective |
| **Shallow depth of field** | Blurred background |
| **Golden hour lighting** | Warm, soft light |

**Example for Diagrams**:
```
A top-down perspective view of a network topology diagram,
wide-angle composition showing the entire infrastructure,
with sharp focus on all elements (no depth of field blur)
```

#### 2. Text Integration Specifications

For technical diagrams requiring accurate text:

**Template**:
```
[Diagram type] with the following text labels spelled correctly:

- "[Exact text 1]": [position, styling]
- "[Exact text 2]": [position, styling]
- "[Exact text 3]": [position, styling]

Ensure all text is:
- Legible at [size specification]
- In [font style] font
- [Color] color
- High contrast against background
```

**Example**:
```
A flowchart with the following text labels spelled correctly:

- "User Authentication": top box, bold sans-serif
- "Validate Credentials": middle-left box, regular weight
- "Grant Access Token": middle-right box, regular weight
- "Access Granted": bottom box, bold sans-serif

Ensure all text is:
- Legible at minimum 14pt size
- In clean sans-serif font (Arial/Helvetica style)
- Black color
- High contrast against white/light gray boxes
```

#### 3. Iterative Refinement Strategy

**Generate → Inspect → Constrain → Iterate**

**Step 1: Generate (Initial)**
```
Generate 1-2 candidates with broad prompt
```

**Step 2: Inspect**
- Evaluate against requirements
- Note failures: text errors, layout issues, style mismatches

**Step 3: Constrain/Isolate**
- Change ONE variable per iteration
- Focus on specific problem: "Fix text spelling in top box"

**Step 4: Iterate**
- Apply fix with narrow prompt
- Repeat inspection

**Example Iteration**:
```
Turn 1: "Create a system diagram with three components"
→ Result: Text is misspelled, layout is cramped

Turn 2: "Fix the spelling of 'Authentication Server' in the top box"
→ Result: Text fixed, but still cramped

Turn 3: "Increase spacing between all boxes to 50px"
→ Result: Better layout, ready for final review
```

#### 4. Style Consistency Patterns

**Color Scheme Specification**:
```
Use the following color palette:
- Primary: #2196F3 (blue)
- Secondary: #4CAF50 (green)
- Accent: #FF9800 (orange)
- Text: #212121 (dark gray)
- Background: #FAFAFA (light gray)
```

**Typography Specification**:
```
Typography rules:
- Headings: 24pt bold sans-serif
- Labels: 14pt regular sans-serif
- Body text: 12pt regular sans-serif
- All text should be left-aligned unless centered for titles
```

**Layout Grid**:
```
Use a 12-column grid layout with:
- 20px gutter between elements
- 40px margins on all sides
- Vertical rhythm with 8px baseline grid
```

#### 5. Factual Constraints for Diagrams

When creating data-driven visuals, always include:

```
Important factual constraints:
- Verify all numerical data is accurate
- Cross-check component relationships
- Ensure technical terminology is correct
- Validate process flow logic

Data to verify:
- [Specific data point 1]: [source]
- [Specific data point 2]: [source]
```

**Example**:
```
Create an infographic showing "Global API Usage Statistics 2025"

Important factual constraints:
- Verify all percentages sum to 100%
- Use only data from provided sources
- Clearly label data source in footer

Data to display:
- REST API: 68% (source: State of API Report 2025)
- GraphQL: 22% (source: State of API Report 2025)
- gRPC: 10% (source: State of API Report 2025)
```

### Domain-Specific Prompt Patterns

#### Technical Diagrams

```
Create a [diagram type] showing [system/process name] with the following
specifications:

Technical components:
1. [Component 1]: [type, function, position]
2. [Component 2]: [type, function, position]
3. [Component 3]: [type, function, position]

Connections:
- [Component 1] → [Component 2]: [relationship, protocol]
- [Component 2] → [Component 3]: [relationship, protocol]

Labels must include:
- All component names spelled correctly
- Connection protocols (HTTP, gRPC, etc.)
- Data flow directions (arrows)

Style: Professional technical documentation style with:
- Sans-serif font for all text
- Consistent icon style (line/filled)
- Color-coding by component type
- High contrast for readability
```

#### Infographics

```
Design a [orientation] infographic titled "[exact title]"
explaining [topic] to [target audience].

Content structure:
1. Header: "[title]" ([font size], [styling])
2. Introduction: "[text]" ([position], [styling])
3. Main sections:
   - Section 1: "[heading]" - [content] ([visual element])
   - Section 2: "[heading]" - [content] ([visual element])
   - Section 3: "[heading]" - [content] ([visual element])
4. Footer: "[text]" ([position], [styling])

Visual hierarchy:
- Title: Largest, bold, [color]
- Headings: Medium, bold, [color]
- Body: Smallest, regular, [color]

Color scheme: [specific colors or palette description]
Iconography: [style description]
Layout: [grid/flow description]
```

#### Logos & Branding

```
Create a logo for "[brand name]" with the following specifications:

Brand name text: "[exact spelling]"
Tagline (if any): "[exact text]"

Design requirements:
- Style: [modern/classic/minimalist/etc.]
- Icon/symbol: [description if needed]
- Color palette: [primary color], [secondary color], [accent color]
- Font style: [serif/sans-serif/script/etc.]
- Mood: [professional/playful/serious/etc.]

Technical requirements:
- Format: Vector-style appearance
- Scalability: Should look good at various sizes
- Versatility: Works on light and dark backgrounds
- Simplicity: Clear and recognizable

Text rendering: Ensure "[brand name]" is spelled correctly
and is the focal point
```

### Common Prompt Anti-Patterns (Avoid)

| Anti-Pattern | Why It Fails | Better Approach |
|--------------|--------------|-----------------|
| **Keyword salad** | "diagram, boxes, arrows, blue, professional" | "Create a system architecture diagram with blue boxes connected by labeled arrows in a professional style" |
| **Vague adjectives** | "Make it look nice" | "Use a minimalist design with high contrast, clean sans-serif typography, and subtle shadows" |
| **No text specification** | "Add labels" | "Add these exact labels: 'Frontend', 'Backend', 'Database' in 14pt sans-serif font" |
| **Ambiguous layout** | "Put components together" | "Arrange components horizontally with 50px spacing, centered vertically" |
| **Missing style context** | "Create a flowchart" | "Create a business process flowchart using standard BPMN notation with rounded rectangles and diamond decision points" |

### Prompt Testing Workflow

1. **Start Simple**: Basic prompt with core requirements
2. **Generate**: Create 1-2 candidates
3. **Evaluate**: Check against requirements checklist
4. **Refine Prompt**: Add specific constraints for failed areas
5. **Re-generate**: Test refined prompt
6. **Document Success**: Save working prompts for reuse

**Example Evolution**:

**V1 (Simple)**:
```
Create a system diagram
```
→ Result: Too vague, unclear what to include

**V2 (Structured)**:
```
Create a system architecture diagram showing Frontend, Backend, and Database
```
→ Result: Components present but layout is poor

**V3 (Detailed)**:
```
Create a system architecture diagram showing three components arranged horizontally:
- "Frontend" (blue box, left)
- "Backend" (green box, center)
- "Database" (gray cylinder, right)
With labeled arrows showing data flow
```
→ Result: Good structure but text is small

**V4 (Refined - Final)**:
```
Create a system architecture diagram showing three components arranged horizontally:
- "Frontend" (blue rounded rectangle, left)
- "Backend" (green rounded rectangle, center)
- "Database" (gray cylinder, right)

With labeled arrows:
- "Frontend" → "Backend": "API Request"
- "Backend" → "Database": "Query"

Style: Professional technical documentation
Text: All labels in 16pt sans-serif, high contrast
Layout: Equal spacing (60px) between components
Background: White with subtle grid pattern
```
→ Result: Production-ready diagram

---

## Model Selection Decision Matrix

### Quick Decision Tree

```
START
│
├─ Need photorealistic image?
│  ├─ YES → Use Imagen 3
│  └─ NO → Continue
│
├─ Need text rendering in image?
│  ├─ YES
│  │  ├─ Complex/long text? → Use Gemini 3 Pro Image
│  │  └─ Simple/short text? → Use Gemini 2.5 Flash Image
│  └─ NO → Continue
│
├─ Need 4K resolution?
│  ├─ YES → Use Gemini 3 Pro Image
│  └─ NO → Continue
│
├─ Need multi-turn refinement?
│  ├─ YES → Use Gemini 2.5 Flash or 3 Pro Image
│  └─ NO → Consider Imagen 3
│
├─ Budget constrained?
│  ├─ YES → Use Gemini 2.5 Flash Image
│  └─ NO → Use Gemini 3 Pro Image for best quality
│
└─ END
```

### Detailed Selection Criteria

#### Choose Gemini 2.5 Flash Image When:

✓ **Fast iteration required**: Prototyping, testing concepts
✓ **Budget is primary concern**: $0.039/image is most cost-effective
✓ **Good-enough quality**: Production quality not critical
✓ **Simple to moderate text rendering**: Labels, titles, short phrases
✓ **High volume generation**: Thousands of images/month
✓ **Social media content**: 1:1, 4:5 aspect ratios at standard resolution

**Example Use Cases**:
- Blog post illustrations
- Internal documentation diagrams
- Prototype mockups
- Social media graphics
- Educational materials
- Presentation slides (non-executive)

#### Choose Gemini 3 Pro Image When:

✓ **Professional output required**: Client-facing, executive presentations
✓ **Complex text rendering**: Multi-line labels, detailed annotations
✓ **High-resolution output**: 2K-4K for print or large displays
✓ **Multi-turn workflows**: Iterative refinement with reference images
✓ **Technical precision**: Engineering diagrams, architectural drawings
✓ **Consistent character/style**: Multi-image projects requiring uniformity
✓ **Factual accuracy critical**: Google Search grounding for real-time data

**Example Use Cases**:
- Technical documentation (official)
- Marketing materials (high-end)
- Product packaging mockups
- Architectural visualizations
- Medical/scientific diagrams
- Legal/compliance documentation
- Brand assets (logos, style guides)

#### Choose Imagen 3 When:

✓ **Photorealism is paramount**: Product photography, realistic scenes
✓ **Single-shot quality**: No need for iterative refinement
✓ **Artistic rendering**: Photography styles, art historical references
✓ **Multiple variations desired**: Generate 4 candidates at once
✓ **No text required**: Or minimal decorative text

**Example Use Cases**:
- Stock photography replacement
- Realistic product backgrounds
- Lifestyle imagery
- Concept art (photorealistic)
- Environmental/scene visualization
- Character portraits (realistic)

### Comparison Matrix

| Criteria | Gemini 2.5 Flash | Gemini 3 Pro | Imagen 3 |
|----------|-----------------|--------------|----------|
| **Cost** | ★★★★★ ($0.039) | ★★★☆☆ ($0.12) | ★★★★☆ ($0.03) |
| **Speed** | ★★★★★ (Fast) | ★★★☆☆ (Slower) | ★★★★☆ (Medium) |
| **Text Quality** | ★★★★☆ (Excellent) | ★★★★★ (Best) | ★★★☆☆ (Good) |
| **Resolution** | ★★★☆☆ (1K-2K) | ★★★★★ (4K) | ★★★☆☆ (Standard) |
| **Photorealism** | ★★★☆☆ (Good) | ★★★★☆ (Excellent) | ★★★★★ (Best) |
| **Multi-turn** | ★★★★★ (Yes) | ★★★★★ (Yes) | ★☆☆☆☆ (No) |
| **Technical Diagrams** | ★★★★☆ (Excellent) | ★★★★★ (Best) | ★★☆☆☆ (Fair) |
| **Versatility** | ★★★★★ (High) | ★★★★★ (High) | ★★★☆☆ (Medium) |

### Budget-Based Recommendations

#### Startup/Small Business ($0-100/month budget)

**Strategy**: Use Gemini 2.5 Flash Image for everything, upgrade selectively

- **Baseline**: 2.5 Flash for all assets (~2,500 images/month at $97.50)
- **Premium**: Upgrade critical 10% to 3 Pro (~$25 for 208 images)
- **Total**: $122.50/month, but scale down to budget

**Recommended Split**:
- 90% → Gemini 2.5 Flash
- 10% → Gemini 3 Pro (client-facing only)

#### Mid-Market ($100-1,000/month budget)

**Strategy**: Tiered approach based on asset importance

- **Tier 1** (Internal docs): 2.5 Flash - $0.039/image
- **Tier 2** (Marketing): 3 Pro or Imagen 3 - $0.03-$0.12/image
- **Tier 3** (Executive/Client): 3 Pro - $0.12/image

**Example Allocation** ($500/month):
- 5,000 images @ $0.039 (2.5 Flash) = $195
- 1,000 images @ $0.12 (3 Pro) = $120
- 6,166 images @ $0.03 (Imagen 3) = $185
- **Total**: $500, ~12,166 images

#### Enterprise ($1,000+/month budget)

**Strategy**: Quality-first with cost optimization through workflow

- **Default to 3 Pro** for consistent high quality
- **Use 2.5 Flash for rapid prototyping** before final 3 Pro generation
- **Use Imagen 3 for photorealistic campaigns**

**Recommended Workflow**:
1. Prototype with 2.5 Flash (~10 iterations @ $0.039 = $0.39)
2. Refine prompt based on learnings
3. Generate final with 3 Pro (~1 iteration @ $0.12 = $0.12)
4. **Total**: $0.51 vs $1.20 (10 × 3 Pro iterations)
5. **Savings**: 57% while maintaining final quality

### Use Case Scenarios

#### Scenario 1: Technical Blog Post

**Requirements**:
- 5 diagrams illustrating API concepts
- Moderate text (API endpoint labels)
- Internal audience (developers)

**Recommendation**: Gemini 2.5 Flash Image
- **Cost**: 5 × $0.039 = $0.195
- **Rationale**: Good text quality, cost-effective, fast iteration

#### Scenario 2: Product Documentation

**Requirements**:
- 25 detailed architecture diagrams
- Complex text (multi-line annotations)
- External audience (enterprise clients)

**Recommendation**: Gemini 3 Pro Image
- **Cost**: 25 × $0.12 = $3.00
- **Rationale**: Professional quality, excellent text rendering, 4K output

#### Scenario 3: Marketing Campaign

**Requirements**:
- 10 hero images for landing pages
- Photorealistic product in lifestyle settings
- No text in images (overlay in HTML)

**Recommendation**: Imagen 3
- **Cost**: 3 requests × 4 images each = 12 images @ $0.09 total
- **Rationale**: Best photorealism, multiple variations, low cost

#### Scenario 4: Educational Course

**Requirements**:
- 100 infographics with text and icons
- Moderate quality acceptable
- Student audience (internal)

**Recommendation**: Mixed approach
- **Draft**: 2.5 Flash for all 100 @ $3.90
- **Upgrade**: Top 20 to 3 Pro @ $2.40
- **Total**: $6.30 for high-quality outcome

#### Scenario 5: Enterprise Presentation

**Requirements**:
- 15 slides with custom diagrams
- Complex data visualizations
- C-level audience (external)

**Recommendation**: Gemini 3 Pro Image
- **Cost**: 15 × $0.12 = $1.80
- **Rationale**: 4K for large displays, impeccable text, professional polish

---

## Implementation Examples

### Example 1: nanobanana-repo Integration

**Scenario**: Generate technical architecture diagrams for nanobanana-repo documentation

#### Step 1: Setup

```python
# requirements.txt
google-generativeai>=0.3.0

# .env
GOOGLE_API_KEY=your_api_key_here
```

#### Step 2: Basic Diagram Generator

```python
# diagram_generator.py
import google.generativeai as genai
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configure API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class DiagramGenerator:
    def __init__(self, model_name="gemini-2.5-flash-image"):
        self.model = genai.GenerativeModel(model_name)

    def generate_diagram(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        image_size: str = "2K",
        output_path: str = "diagram.png"
    ):
        """Generate a technical diagram from a prompt."""

        config = genai.GenerateContentConfig(
            response_modalities=[genai.Modality.TEXT, genai.Modality.IMAGE],
            generation_config={
                "imageConfig": {
                    "aspectRatio": aspect_ratio,
                    "imageSize": image_size
                }
            }
        )

        response = self.model.generate_content(prompt, config=config)

        # Extract and save image
        for part in response.parts:
            if part.inline_data:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(part.inline_data.data)
                print(f"✓ Diagram saved to {output_path}")
            elif part.text:
                print(f"Model response: {part.text}")

        return response

# Usage
generator = DiagramGenerator()

# Generate architecture diagram
prompt = """
Create a system architecture diagram for the nanobanana-repo image generation service.

Components (with exact labels in sans-serif font):
- "Client Application" (top-left, light blue rounded rectangle)
- "Gemini API Gateway" (top-right, green rounded rectangle)
- "Image Storage" (bottom-center, orange cylinder)
- "CDN" (bottom-right, purple cloud shape)

Connections (with black arrows and labels):
- "Client Application" → "Gemini API Gateway": "POST /generate"
- "Gemini API Gateway" → "Image Storage": "Save PNG"
- "Image Storage" → "CDN": "Distribute"
- "CDN" → "Client Application": "Serve Image" (dashed line)

Style: Professional technical documentation with subtle shadows
Text: All labels in 14pt sans-serif, dark gray color
Layout: Hierarchical top-to-bottom flow with 60px spacing
Background: White with light grid pattern
"""

generator.generate_diagram(
    prompt=prompt,
    aspect_ratio="16:9",
    image_size="2K",
    output_path="docs/diagrams/architecture.png"
)
```

#### Step 3: Batch Diagram Generation

```python
# batch_generator.py
from diagram_generator import DiagramGenerator
from typing import List, Dict

class BatchDiagramGenerator:
    def __init__(self, model_name="gemini-2.5-flash-image"):
        self.generator = DiagramGenerator(model_name)

    def generate_batch(self, diagram_specs: List[Dict]):
        """Generate multiple diagrams from specifications."""

        results = []

        for i, spec in enumerate(diagram_specs, 1):
            print(f"\n[{i}/{len(diagram_specs)}] Generating {spec['name']}...")

            try:
                response = self.generator.generate_diagram(
                    prompt=spec['prompt'],
                    aspect_ratio=spec.get('aspect_ratio', '16:9'),
                    image_size=spec.get('image_size', '2K'),
                    output_path=spec['output_path']
                )
                results.append({
                    'name': spec['name'],
                    'status': 'success',
                    'path': spec['output_path']
                })
            except Exception as e:
                print(f"✗ Error: {e}")
                results.append({
                    'name': spec['name'],
                    'status': 'error',
                    'error': str(e)
                })

        return results

# Define diagram specifications
diagrams = [
    {
        'name': 'Architecture Overview',
        'prompt': 'Create a high-level architecture diagram...',
        'output_path': 'docs/diagrams/architecture-overview.png',
        'aspect_ratio': '16:9',
        'image_size': '2K'
    },
    {
        'name': 'API Request Flow',
        'prompt': 'Create a sequence diagram showing API request flow...',
        'output_path': 'docs/diagrams/api-flow.png',
        'aspect_ratio': '3:4',
        'image_size': '2K'
    },
    {
        'name': 'Data Model',
        'prompt': 'Create an entity-relationship diagram...',
        'output_path': 'docs/diagrams/data-model.png',
        'aspect_ratio': '4:3',
        'image_size': '2K'
    }
]

# Generate all diagrams
batch_gen = BatchDiagramGenerator()
results = batch_gen.generate_batch(diagrams)

# Print summary
print("\n=== Generation Summary ===")
for result in results:
    status_icon = "✓" if result['status'] == 'success' else "✗"
    print(f"{status_icon} {result['name']}: {result.get('path', result.get('error'))}")
```

#### Step 4: Iterative Refinement

```python
# iterative_refiner.py
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class IterativeDiagramRefiner:
    def __init__(self, model_name="gemini-3-pro-image-preview"):
        self.model = genai.GenerativeModel(model_name)
        self.chat = None
        self.iteration = 0

    def start_session(self):
        """Start a new refinement session."""
        self.chat = self.model.start_chat(
            config=genai.GenerateContentConfig(
                response_modalities=[genai.Modality.TEXT, genai.Modality.IMAGE]
            )
        )
        self.iteration = 0
        print("✓ Refinement session started")

    def refine(self, prompt: str, save_as: str = None):
        """Send refinement prompt and optionally save result."""
        if not self.chat:
            raise Exception("Session not started. Call start_session() first.")

        self.iteration += 1
        print(f"\n[Iteration {self.iteration}] {prompt[:50]}...")

        response = self.chat.send_message(prompt)

        # Save image if path provided
        for part in response.parts:
            if part.inline_data and save_as:
                output_path = save_as.replace(".png", f"_v{self.iteration}.png")
                with open(output_path, "wb") as f:
                    f.write(part.inline_data.data)
                print(f"✓ Saved to {output_path}")
            elif part.text:
                print(f"Model: {part.text}")

        return response

# Usage: Iteratively refine a complex diagram
refiner = IterativeDiagramRefiner(model_name="gemini-3-pro-image-preview")
refiner.start_session()

# Iteration 1: Initial generation
refiner.refine(
    "Create a microservices architecture diagram with API Gateway, User Service, and Order Service",
    save_as="docs/diagrams/microservices.png"
)

# Iteration 2: Add detail
refiner.refine(
    "Add a Database component below Order Service with a connecting arrow labeled 'SQL Query'",
    save_as="docs/diagrams/microservices.png"
)

# Iteration 3: Improve text
refiner.refine(
    "Make all component labels larger (18pt) and use a blue color scheme for service boxes",
    save_as="docs/diagrams/microservices.png"
)

# Iteration 4: Final polish
refiner.refine(
    "Add a title 'Microservices Architecture' at the top in bold 24pt font",
    save_as="docs/diagrams/microservices.png"
)

print(f"\n✓ Refinement complete after {refiner.iteration} iterations")
```

### Example 2: CLI Tool for Diagram Generation

```python
# diagram_cli.py
import click
import google.generativeai as genai
import os
from pathlib import Path

@click.group()
def cli():
    """Gemini Diagram Generator CLI"""
    pass

@cli.command()
@click.option('--prompt', '-p', required=True, help='Generation prompt')
@click.option('--output', '-o', default='diagram.png', help='Output file path')
@click.option('--model', '-m', default='gemini-2.5-flash-image',
              type=click.Choice(['gemini-2.5-flash-image', 'gemini-3-pro-image-preview']))
@click.option('--aspect-ratio', '-a', default='16:9',
              type=click.Choice(['1:1', '3:2', '2:3', '3:4', '4:3', '4:5', '5:4', '9:16', '16:9', '21:9']))
@click.option('--size', '-s', default='2K', type=click.Choice(['1K', '2K', '4K']))
def generate(prompt, output, model, aspect_ratio, size):
    """Generate a diagram from a text prompt."""

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model_instance = genai.GenerativeModel(model)

    click.echo(f"Generating diagram with {model}...")

    config = genai.GenerateContentConfig(
        response_modalities=[genai.Modality.TEXT, genai.Modality.IMAGE],
        generation_config={
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": size
            }
        }
    )

    response = model_instance.generate_content(prompt, config=config)

    for part in response.parts:
        if part.inline_data:
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            with open(output, "wb") as f:
                f.write(part.inline_data.data)
            click.echo(f"✓ Diagram saved to {output}")
        elif part.text:
            click.echo(f"Model response: {part.text}")

@cli.command()
@click.option('--template', '-t', required=True,
              type=click.Choice(['architecture', 'flowchart', 'infographic', 'network']))
@click.option('--output', '-o', default='diagram.png')
def template(template, output):
    """Generate diagram from a predefined template."""

    templates = {
        'architecture': """
Create a clean system architecture diagram with:
- "Frontend" (blue box, left)
- "Backend" (green box, center)
- "Database" (gray cylinder, right)
With labeled arrows showing data flow, professional style
        """,
        'flowchart': """
Create a vertical flowchart with:
- Start: "Begin Process" (green rounded rectangle)
- Step 1: "Process Data" (blue rectangle)
- Decision: "Valid?" (yellow diamond)
  - Yes → "Save" (blue rectangle)
  - No → "Error" (red rectangle)
- End: "Complete" (green rounded rectangle)
        """,
        'infographic': """
Design a vertical infographic titled "3 Steps to Success":
1. "Plan" - Set clear goals
2. "Execute" - Take action
3. "Review" - Measure results
Modern gradient background, white text
        """,
        'network': """
Create a network topology diagram with:
- "Router" (center, gray hexagon)
- "Server A" (top-left, blue box)
- "Server B" (top-right, blue box)
- "Firewall" (bottom, red box)
With connection lines showing network links
        """
    }

    ctx = click.get_current_context()
    ctx.invoke(generate, prompt=templates[template].strip(), output=output)

if __name__ == '__main__':
    cli()
```

**Usage**:
```bash
# Generate from custom prompt
python diagram_cli.py generate \
  --prompt "Create an API architecture diagram" \
  --output docs/api.png \
  --model gemini-3-pro-image-preview \
  --aspect-ratio 16:9 \
  --size 4K

# Generate from template
python diagram_cli.py template \
  --template architecture \
  --output docs/arch.png
```

---

## Known Limitations

### General Image Generation Limitations

#### 1. Text Rendering Challenges

**Issue**: Even with advanced models, text rendering can be imperfect

**Symptoms**:
- Occasional misspellings (e.g., "Sevrer" instead of "Server")
- Character substitutions (e.g., "Authent1cation" with number instead of 'i')
- Word truncation in long text strings
- Inconsistent font rendering across labels

**Mitigation Strategies**:
- ✓ **Explicitly spell out text**: "spelled correctly as 'Authentication'"
- ✓ **Use iterative refinement**: Fix errors in subsequent turns
- ✓ **Keep text short**: Prefer "Auth" over "Authentication Service v2.1"
- ✓ **Use high-resolution**: 2K-4K reduces character distortion
- ✓ **Verify each generation**: Manual QA for critical text
- ✓ **Use Gemini 3 Pro for critical text**: Better than 2.5 Flash

**Best Practices**:
```python
# Good: Explicit spelling
prompt = "Create a diagram with the label 'Database' spelled correctly"

# Better: Include common mistakes to avoid
prompt = "Create a diagram with the label 'Database' (not 'Databse' or 'Datbase')"

# Best: Use iterative refinement
# Turn 1: Generate diagram
# Turn 2: "Fix spelling: change 'Databse' to 'Database' in the bottom box"
```

#### 2. Complex Layouts

**Issue**: Intricate multi-component layouts may not align perfectly

**Symptoms**:
- Uneven spacing between elements
- Misaligned text labels
- Overlapping components
- Inconsistent sizing

**Mitigation Strategies**:
- ✓ **Specify exact spacing**: "60px between each box"
- ✓ **Use grid language**: "Arrange in a 3×2 grid"
- ✓ **Describe alignment**: "All labels centered vertically"
- ✓ **Simplify when possible**: Break complex diagrams into multiple simpler ones
- ✓ **Use reference images**: Upload example layouts

**Example**:
```python
# Vague (poor results)
prompt = "Create a diagram with lots of components"

# Specific (better results)
prompt = """
Create a diagram with 6 components arranged in a 2×3 grid:
- Row 1: Component A, Component B, Component C
- Row 2: Component D, Component E, Component F
Equal spacing (50px) horizontally and vertically
All components same size (200px × 100px)
"""
```

#### 3. Factual Accuracy

**Issue**: Models may generate plausible-looking but incorrect data

**Symptoms**:
- Incorrect statistics in infographics
- Wrong dates or names
- Inaccurate technical specifications
- Misleading visual representations

**Mitigation Strategies**:
- ✓ **Always verify data**: Manual fact-checking required
- ✓ **Provide explicit data**: Include exact numbers in prompt
- ✓ **Use Google Search grounding** (Gemini 3 Pro only)
- ✓ **Include data sources**: "According to [source], the value is X"
- ✓ **Review before publishing**: Human validation essential

**Important Note**:
```
⚠️ CRITICAL: Always verify the factual accuracy of data-driven
visuals like diagrams and infographics. AI models can generate
convincing but incorrect information.
```

#### 4. Hands and Fine Details (Photorealistic Images)

**Issue**: Human hands and intricate details can be distorted

**Symptoms**:
- Extra/missing fingers
- Unnatural hand positions
- Distorted facial features (less common)
- Garbled fine patterns

**Mitigation Strategies**:
- ✓ **Avoid showing hands** if not critical
- ✓ **Use Imagen 3** for photorealistic scenes (better hand rendering)
- ✓ **Zoom out**: Hands less detailed from distance
- ✓ **Generate multiple variations**: Select best result
- ✓ **Use reference images**: Upload examples of desired hand positions

**Note**: This is less relevant for technical diagrams but important for lifestyle/marketing imagery

#### 5. Consistency Across Generations

**Issue**: Generating the "same" image twice may yield different results

**Symptoms**:
- Different color tones
- Slightly different layouts
- Varying text styles
- Changed component shapes

**Mitigation Strategies**:
- ✓ **Use multi-turn refinement** within same session
- ✓ **Upload reference images**: "Match the style of this image"
- ✓ **Be extremely specific**: Detailed prompts reduce variance
- ✓ **Use character consistency features** (Gemini models)
- ✓ **Save successful prompts**: Reuse exact wording

**Example Workflow**:
```python
# Instead of generating 5 separate images:
for i in range(5):
    generate("Create a logo...")  # Each will differ

# Use multi-turn refinement in one session:
chat = model.start_chat(...)
chat.send_message("Create a logo...")
chat.send_message("Generate 4 more variations with same style")
# Better consistency
```

### Model-Specific Limitations

#### Gemini 2.5 Flash Image

| Limitation | Impact | Workaround |
|------------|--------|------------|
| **Maximum 2K resolution** | Cannot generate 4K images | Use Gemini 3 Pro for high-res needs |
| **Text rendering quality** | 8/12 benchmark (good, not perfect) | Use 3 Pro for complex text |
| **No thinking mode** | Can't see interim generation steps | Preview with 3 Pro if needed |
| **Limited reference images** | Fewer than 3 Pro's 14 images | Simplify reference requirements |

#### Gemini 3 Pro Image

| Limitation | Impact | Workaround |
|------------|--------|------------|
| **Higher cost** | $0.12 vs $0.039 per image | Use 2.5 Flash for prototyping |
| **Slower generation** | Takes longer than 2.5 Flash | Plan for longer timelines |
| **Preview status** | May have occasional API changes | Monitor release notes |
| **Geographic restrictions** | Not available in all regions | Check API availability |

#### Imagen 3

| Limitation | Impact | Workaround |
|------------|--------|------------|
| **No multi-turn refinement** | Single-shot generation only | Use Gemini models for iteration |
| **Limited text rendering** | Not designed for text-heavy images | Use Gemini for technical diagrams |
| **No reference image support** | Can't upload style guides | Use Gemini models instead |
| **Fixed aspect ratios** | Only 5 ratios vs Gemini's 10 | Use Gemini for custom ratios |

### API and Technical Limitations

#### 1. Image-Only Output Not Supported

**Issue**: Must request both TEXT and IMAGE modalities

```python
# This will FAIL:
config = {
    "responseModalities": ["IMAGE"]  # ✗ Not allowed
}

# This will WORK:
config = {
    "responseModalities": ["TEXT", "IMAGE"]  # ✓ Required
}
```

#### 2. Rate Limits

**Issue**: API has request rate limits (exact limits vary by tier)

**Mitigation**:
- ✓ Implement exponential backoff
- ✓ Batch requests appropriately
- ✓ Monitor quota usage
- ✓ Upgrade API tier if needed

**Example**:
```python
import time
from google.api_core import retry

@retry.Retry(predicate=retry.if_exception_type(Exception))
def generate_with_retry(model, prompt, config):
    try:
        return model.generate_content(prompt, config=config)
    except Exception as e:
        if "429" in str(e):  # Rate limit
            time.sleep(60)  # Wait 1 minute
            raise  # Retry will handle
        else:
            raise
```

#### 3. Token Limits

**Issue**: Maximum input/output token constraints

| Model | Input Limit | Output Limit |
|-------|-------------|--------------|
| Gemini 2.5 Flash Image | 65,536 | 32,768 |
| Gemini 3 Pro Image | 65,536 | 32,768 |
| Gemini 2.0 Flash Image | 32,768 | 8,192 |
| Imagen 3 | 480 (prompt) | N/A |

**Mitigation**:
- ✓ Keep prompts concise but specific
- ✓ Use Gemini models for long prompts (not Imagen)
- ✓ Split very complex diagrams into multiple requests

#### 4. SynthID Watermarking

**Issue**: All generated images include invisible SynthID watermark

**Impact**:
- Cannot be removed
- Detectable by SynthID detection tools
- Permanent marker of AI generation

**Note**: This is by design for responsible AI use, not a bug

#### 5. Safety Filters

**Issue**: Content may be blocked by safety filters

**Symptoms**:
- Request rejected
- Empty response
- Safety warning message

**Mitigation**:
- ✓ Avoid sensitive topics
- ✓ Adjust safety settings (if allowed)
- ✓ Rephrase prompt to be less ambiguous
- ✓ Review content policy guidelines

---

## Troubleshooting Guide

### Common Issues and Solutions

#### Issue 1: Text is Misspelled or Garbled

**Symptoms**:
- Labels show "Databse" instead of "Database"
- Characters replaced with symbols or numbers
- Text completely illegible

**Diagnostics**:
```
✓ Check prompt for typos (model may replicate)
✓ Verify text is explicitly stated in prompt
✓ Check if text is too long for model capacity
```

**Solutions**:

**A. Explicit Spelling**
```python
# Before
prompt = "Create a diagram with a database component"

# After
prompt = "Create a diagram with a component labeled 'Database' (spelled correctly)"
```

**B. Iterative Fix**
```python
# Turn 1: Generate initial diagram
chat.send_message("Create system diagram with database")

# Turn 2: Fix spelling
chat.send_message("Fix spelling: change 'Databse' to 'Database' in bottom-right component")
```

**C. Upgrade Model**
```python
# If using 2.5 Flash with issues
model = genai.GenerativeModel("gemini-2.5-flash-image")

# Upgrade to 3 Pro for better text
model = genai.GenerativeModel("gemini-3-pro-image-preview")
```

**D. Simplify Text**
```python
# Before (complex)
prompt = "Label: 'Authentication Service v2.1 (Production)'"

# After (simplified)
prompt = "Label: 'Auth Service'"
```

---

#### Issue 2: Layout is Misaligned or Cluttered

**Symptoms**:
- Components overlap
- Uneven spacing
- Text outside boundaries
- Asymmetric arrangement

**Diagnostics**:
```
✓ Check if prompt specifies layout clearly
✓ Verify component count isn't too high
✓ Check aspect ratio matches layout (portrait vs landscape)
```

**Solutions**:

**A. Explicit Spacing**
```python
# Before
prompt = "Create diagram with Frontend, Backend, Database"

# After
prompt = """
Create diagram with three components arranged horizontally:
- 'Frontend' (left)
- 'Backend' (center, 80px from Frontend)
- 'Database' (right, 80px from Backend)
All components vertically centered
"""
```

**B. Grid Layout**
```python
prompt = """
Arrange 6 components in a 2×3 grid:
Row 1: A, B, C
Row 2: D, E, F
Equal spacing: 60px horizontal, 40px vertical
All components same size: 180px × 100px
"""
```

**C. Simplify**
```python
# If 10-component diagram is cluttered, split into two:

# Diagram 1: Frontend tier (4 components)
# Diagram 2: Backend tier (6 components)
```

**D. Use Reference Image**
```python
# Upload existing well-laid-out diagram
with open("reference_layout.png", "rb") as f:
    reference = f.read()

prompt = "Create a similar layout to the reference image, but with these new components..."
```

---

#### Issue 3: "responseModalities must include TEXT and IMAGE" Error

**Symptoms**:
```
Error: Invalid generation config: responseModalities must include both TEXT and IMAGE
```

**Cause**: Trying to generate image-only output (not supported)

**Solution**:
```python
# ✗ WRONG (image-only)
config = genai.GenerateContentConfig(
    response_modalities=[genai.Modality.IMAGE]
)

# ✓ CORRECT (both required)
config = genai.GenerateContentConfig(
    response_modalities=[genai.Modality.TEXT, genai.Modality.IMAGE]
)
```

---

#### Issue 4: Rate Limit / Quota Exceeded

**Symptoms**:
```
Error 429: Resource has been exhausted (e.g., check quota)
```

**Diagnostics**:
```
✓ Check API quota in Google AI Studio
✓ Verify number of requests per minute
✓ Check if daily/monthly limit reached
```

**Solutions**:

**A. Implement Retry with Backoff**
```python
import time
from google.api_core import retry, exceptions

@retry.Retry(
    predicate=retry.if_exception_type(exceptions.ResourceExhausted),
    initial=1.0,
    maximum=60.0,
    multiplier=2.0,
    deadline=300.0
)
def generate_with_retry(model, prompt, config):
    return model.generate_content(prompt, config=config)

# Usage
try:
    response = generate_with_retry(model, prompt, config)
except exceptions.RetryError:
    print("Max retries exceeded. Please try again later.")
```

**B. Add Request Delay**
```python
import time

for prompt in prompts:
    response = model.generate_content(prompt, config=config)
    time.sleep(2)  # 2-second delay between requests
```

**C. Batch Appropriately**
```python
# Instead of 100 rapid requests:
for i in range(100):
    generate(prompt)

# Batch into smaller groups with delays:
batch_size = 10
for i in range(0, len(prompts), batch_size):
    batch = prompts[i:i+batch_size]
    for prompt in batch:
        generate(prompt)
    time.sleep(60)  # 1-minute delay between batches
```

**D. Upgrade API Tier**
- Visit Google AI Studio
- Request quota increase
- Consider Vertex AI for higher limits

---

#### Issue 5: Blank or Empty Image Generated

**Symptoms**:
- Response contains image data, but file is blank/corrupted
- No visible content in output image

**Diagnostics**:
```
✓ Check if prompt is too vague
✓ Verify image data is being saved correctly
✓ Check if safety filters blocked content
```

**Solutions**:

**A. Make Prompt More Specific**
```python
# Before (too vague)
prompt = "Create a diagram"

# After (specific)
prompt = "Create a system architecture diagram with blue boxes labeled 'Frontend' and 'Backend'"
```

**B. Verify Image Saving**
```python
# Check image data exists
for part in response.parts:
    if part.inline_data:
        print(f"Image data size: {len(part.inline_data.data)} bytes")
        if len(part.inline_data.data) < 1000:
            print("Warning: Image data is very small, may be corrupted")
```

**C. Check Safety Filters**
```python
# Add safety settings
config = genai.GenerateContentConfig(
    response_modalities=[genai.Modality.TEXT, genai.Modality.IMAGE],
    safety_settings={
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_ONLY_HIGH"
    }
)
```

---

#### Issue 6: Inconsistent Results Across Multiple Generations

**Symptoms**:
- Same prompt produces wildly different images
- Colors/style vary significantly
- Layout changes unexpectedly

**Cause**: Stochastic nature of generative models

**Solutions**:

**A. Use Multi-turn Chat for Consistency**
```python
# Instead of separate calls
for i in range(5):
    model.generate_content("Create logo...")

# Use chat session
chat = model.start_chat(config=config)
chat.send_message("Create a logo with blue color scheme")
chat.send_message("Generate 4 more variations maintaining the same blue color and style")
```

**B. Upload Reference Image**
```python
# Upload style reference
with open("style_guide.png", "rb") as f:
    reference_image = f.read()

prompt = "Create a new diagram matching the exact style, colors, and typography of the reference image"
# Include reference image in request
```

**C. Be Extremely Specific**
```python
# Vague (high variance)
prompt = "Create a modern logo"

# Specific (low variance)
prompt = """
Create a logo with these exact specifications:
- Color: #2196F3 (blue) only
- Font: Sans-serif, bold
- Shape: Circle
- Size: 512×512px
- Background: White
- Text: 'LOGO' centered in circle
"""
```

---

#### Issue 7: Text Too Small to Read

**Symptoms**:
- Labels are illegible
- Text appears pixelated
- Can't read diagram annotations

**Solutions**:

**A. Specify Text Size**
```python
prompt = """
Create diagram with large, legible text:
- All labels minimum 16pt font size
- Title in 24pt bold
- Use high contrast (black text on white background)
"""
```

**B. Increase Image Resolution**
```python
# Before (1K)
config = {
    "imageConfig": {"imageSize": "1K"}
}

# After (4K, requires Gemini 3 Pro)
config = {
    "imageConfig": {"imageSize": "4K"}
}
```

**C. Simplify Layout**
```python
# Before: 10 components with small labels in 1024×1024

# After: 4 components with large labels in same resolution
# or: Split into 2 diagrams
```

---

#### Issue 8: API Authentication Errors

**Symptoms**:
```
Error 401: Request is missing required authentication credential
Error 403: API key not valid
```

**Diagnostics**:
```bash
# Check if API key is set
echo $GOOGLE_API_KEY

# Verify key in Google AI Studio
# https://aistudio.google.com/app/apikey
```

**Solutions**:

**A. Set Environment Variable**
```bash
export GOOGLE_API_KEY="your_api_key_here"

# Verify
python -c "import os; print(os.getenv('GOOGLE_API_KEY'))"
```

**B. Load from .env File**
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment")

genai.configure(api_key=api_key)
```

**C. Hardcode (Not Recommended for Production)**
```python
# Only for local testing
genai.configure(api_key="AIza...")
```

---

### Debugging Workflow

#### Step-by-step Debugging Process

```python
# debug_generation.py
import google.generativeai as genai
import os

def debug_generation(prompt, model_name="gemini-2.5-flash-image"):
    """Debug image generation with detailed logging."""

    print("=== DEBUG IMAGE GENERATION ===\n")

    # 1. Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("✗ GOOGLE_API_KEY not found")
        return
    print(f"✓ API key found (length: {len(api_key)})")

    # 2. Configure API
    try:
        genai.configure(api_key=api_key)
        print("✓ API configured")
    except Exception as e:
        print(f"✗ Configuration failed: {e}")
        return

    # 3. Create model
    try:
        model = genai.GenerativeModel(model_name)
        print(f"✓ Model created: {model_name}")
    except Exception as e:
        print(f"✗ Model creation failed: {e}")
        return

    # 4. Prepare config
    config = genai.GenerateContentConfig(
        response_modalities=[genai.Modality.TEXT, genai.Modality.IMAGE],
        generation_config={
            "imageConfig": {
                "aspectRatio": "16:9",
                "imageSize": "2K"
            }
        }
    )
    print("✓ Config prepared")

    # 5. Generate content
    print(f"\nPrompt: {prompt[:100]}...")
    try:
        response = model.generate_content(prompt, config=config)
        print("✓ Generation successful")
    except Exception as e:
        print(f"✗ Generation failed: {e}")
        return

    # 6. Analyze response
    has_text = False
    has_image = False
    image_size = 0

    for part in response.parts:
        if part.text:
            has_text = True
            print(f"✓ Text response: {part.text[:100]}...")
        if part.inline_data:
            has_image = True
            image_size = len(part.inline_data.data)
            print(f"✓ Image data: {image_size:,} bytes")

    # 7. Validate
    if not has_text:
        print("⚠ Warning: No text in response")
    if not has_image:
        print("✗ Error: No image in response")
    elif image_size < 1000:
        print("⚠ Warning: Image data is very small, may be corrupted")

    # 8. Save if valid
    if has_image and image_size >= 1000:
        output_path = "debug_output.png"
        for part in response.parts:
            if part.inline_data:
                with open(output_path, "wb") as f:
                    f.write(part.inline_data.data)
        print(f"✓ Image saved to {output_path}")

    print("\n=== DEBUG COMPLETE ===")

# Usage
debug_generation("Create a simple diagram with two boxes labeled 'A' and 'B'")
```

---

## References

### Official Documentation

1. **Gemini API - Image Generation**
   https://ai.google.dev/gemini-api/docs/image-generation
   Comprehensive guide to Nano Banana and Nano Banana Pro

2. **Gemini API - Imagen 3**
   https://ai.google.dev/gemini-api/docs/imagen
   Imagen 3 integration with Gemini API

3. **Gemini Models Reference**
   https://ai.google.dev/gemini-api/docs/models
   Complete model specifications and capabilities

4. **Generating Content**
   https://ai.google.dev/api/generate-content
   API reference for generateContent endpoint

5. **Prompt Design Strategies**
   https://ai.google.dev/gemini-api/docs/prompting-strategies
   Best practices for effective prompting

### Blog Posts & Announcements

6. **Introducing Gemini 2.5 Flash Image**
   https://developers.googleblog.com/en/introducing-gemini-2-5-flash-image/
   Official announcement with capabilities overview

7. **How to Prompt Gemini 2.5 Flash Image**
   https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/
   Detailed prompt engineering guide

8. **Gemini 2.5 Flash Image Production Ready**
   https://developers.googleblog.com/en/gemini-2-5-flash-image-now-ready-for-production-with-new-aspect-ratios/
   Production status and new features

9. **Imagen 3 Arrives in Gemini API**
   https://developers.googleblog.com/en/imagen-3-arrives-in-the-gemini-api/
   Imagen 3 integration announcement

10. **Build with Nano Banana Pro (Gemini 3 Pro Image)**
    https://blog.google/technology/developers/gemini-3-pro-image-developers/
    Advanced features and use cases

### Community Resources

11. **Comparing Google's Image Generation Models**
    https://www.raymondcamden.com/2025/04/08/comparing-googles-image-generation-models
    Third-party comparison of Gemini vs Imagen

12. **Nano Banana Prompt Engineering Best Practices**
    https://skywork.ai/blog/nano-banana-gemini-prompt-engineering-best-practices-2025/
    Community-driven prompt engineering guide

13. **gemimg - Lightweight Python Wrapper**
    https://github.com/minimaxir/gemimg
    Simplified Python SDK by Max Woolf

14. **Nano Banana Nuanced Prompting**
    https://minimaxir.com/2025/11/nano-banana-prompts/
    Advanced prompt engineering techniques

15. **Gemini Image Prompting Handbook**
    https://github.com/pauhu/gemini-image-prompting-handbook
    Open-source JSON schema for structured prompts

### DeepMind Model Pages

16. **Gemini 2.5 Flash Image (Nano Banana)**
    https://deepmind.google/models/gemini-image/flash/
    Official DeepMind model card

17. **Gemini 3 Pro Image (Nano Banana Pro)**
    https://deepmind.google/models/gemini-image/pro/
    Official DeepMind model card

18. **Gemini Image Models Overview**
    https://deepmind.google/models/gemini-image/
    Family overview and capabilities

### Google Cloud / Vertex AI

19. **Gemini 2.5 Flash on Vertex AI**
    https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash
    Enterprise deployment guide

20. **Generate and Edit Images with Gemini**
    https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-generation
    Vertex AI image generation documentation

21. **Use Gemini 2.5 Flash Image on Vertex AI**
    https://cloud.google.com/blog/products/ai-machine-learning/gemini-2-5-flash-image-on-vertex-ai
    Enterprise use cases and deployment

### Pricing & API Guides

22. **Gemini 2.5 Flash Image API Cost Analysis**
    https://blog.laozhang.ai/api-guides/gemini-25-flash-image-api/
    Detailed pricing breakdown and optimization

23. **Gemini Image Generation Limits**
    https://blog.laozhang.ai/api-guides/gemini-image-generation-limits/
    API limits and quota management

24. **Is Nano Banana Free?**
    https://skywork.ai/blog/nano-banana-free-access-gemini-2-5-flash-image-2025/
    Access options and pricing

### API Providers

25. **AIMLAPI - Gemini 3 Pro Image**
    https://aimlapi.com/models/gemini-3-pro-image
    Alternative API provider with pricing

26. **Kie.ai - Nano Banana Pro API**
    https://kie.ai/nano-banana
    API integration guide

### Comparisons & Benchmarks

27. **DALLE 3 vs Gemini 2.5 Flash Image**
    https://centrox.ai/blogs/artificial-intelligence/dall-e-3-vs-gemini-2-5-flash-image
    Cross-platform comparison

28. **Imagen 4 vs Gemini 2.5 Flash**
    https://www.imagen-veo-ai.com/blog/google-imagen-4-review
    Latest model comparison

29. **LMArena Leaderboard**
    (Gemini 2.5 Flash ranked #1 as of August 2025)

### Tools & SDKs

30. **Google AI Studio**
    https://aistudio.google.com
    Web-based testing and API key management

31. **Python SDK (@google/generative-ai)**
    Official Python client library

32. **TypeScript SDK (@google/generative-ai)**
    Official Node.js/TypeScript library

### Related Research

33. **SynthID Watermarking**
    Google's invisible watermarking technology for AI-generated content

34. **Gemini Model Card (PDF)**
    https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-2-5-Flash-Model-Card.pdf
    Technical specifications and benchmark results

---

## Document Metadata

**Created**: December 7, 2025
**Author**: Claude (deep-researcher agent)
**Target Project**: nanobanana-repo
**Research Scope**: Google Gemini & Imagen image generation models
**Primary Focus**: Technical diagram generation with text rendering
**Models Analyzed**: Gemini 2.5 Flash Image, Gemini 3 Pro Image, Imagen 3
**Total Sources**: 34+ official and community references
**Document Version**: 1.0

### Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-07 | 1.0 | Initial comprehensive research document |

---

## Appendix: Quick Reference Cards

### Model Selection Cheat Sheet

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK MODEL SELECTOR                                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 📊 Technical Diagrams (labels, annotations)                │
│    → Gemini 3 Pro Image (best text rendering)             │
│    → Gemini 2.5 Flash (cost-effective alternative)        │
│                                                             │
│ 🖼️ Photorealistic Images (no text)                         │
│    → Imagen 3 (best photorealism)                         │
│    → Gemini 3 Pro Image (good alternative)                │
│                                                             │
│ 💰 Budget Priority (high volume)                           │
│    → Gemini 2.5 Flash ($0.039/image)                      │
│                                                             │
│ 🎯 Quality Priority (professional)                         │
│    → Gemini 3 Pro Image ($0.12/image)                     │
│                                                             │
│ 🔄 Iterative Workflows                                     │
│    → Gemini models (multi-turn support)                   │
│    → NOT Imagen 3 (single-shot only)                      │
│                                                             │
│ 📐 High Resolution (4K)                                    │
│    → Gemini 3 Pro Image only                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Prompt Template Library

#### System Architecture Diagram
```
Create a [clean/modern/professional] system architecture diagram
showing [system name].

Components (with exact labels in sans-serif font):
- "[Component 1]": [position], [color], [shape]
- "[Component 2]": [position], [color], [shape]
- "[Component 3]": [position], [color], [shape]

Connections (with labeled arrows):
- "[Component 1]" → "[Component 2]": "[label]"
- "[Component 2]" → "[Component 3]": "[label]"

Style: [minimal/detailed/colorful]
Text: [size], [font], [color]
Layout: [horizontal/vertical/hierarchical]
Background: [white/gray/gradient]
```

#### Flowchart
```
Create a [vertical/horizontal] flowchart showing "[process name]".

Steps (with exact labels in bold):
- Start: "[label]" ([color] [shape])
- Step 1: "[label]" ([color] [shape])
- Decision: "[question]?" ([color] diamond)
  - Yes → "[label]" ([color] [shape])
  - No → "[label]" ([color] [shape])
- End: "[label]" ([color] [shape])

Style: [business/technical/simple]
Connectors: [arrows/lines], [color]
Background: [color/gradient]
```

#### Infographic
```
Design a [vertical/horizontal] infographic titled "[exact title]"
about [topic].

Sections:
1. Header: "[title]" ([size], [styling], [position])
2. "[Section 1 heading]": [content], [icon/visual]
3. "[Section 2 heading]": [content], [icon/visual]
4. "[Section 3 heading]": [content], [icon/visual]
5. Footer: "[text]" ([size], [styling])

Visual style: [color scheme], [typography]
Layout: [grid/flow/hierarchy]
Iconography: [style]
```

### API Configuration Reference

```python
# CONFIGURATION QUICK REFERENCE

# 1. Model Selection
models = {
    "fast": "gemini-2.5-flash-image",
    "pro": "gemini-3-pro-image-preview",
    "imagen": "imagen-3.0-generate-002"
}

# 2. Aspect Ratios
aspect_ratios = [
    "1:1",    # Square
    "3:2", "2:3",  # Classic photo
    "3:4", "4:3",  # Standard display
    "4:5", "5:4",  # Social media
    "9:16", "16:9",  # Widescreen
    "21:9"   # Ultra-wide (Gemini only)
]

# 3. Image Sizes
sizes = {
    "1K": "1K",  # All models
    "2K": "2K",  # All Gemini models
    "4K": "4K"   # Gemini 3 Pro only
}

# 4. Complete Config Template
config = genai.GenerateContentConfig(
    response_modalities=[genai.Modality.TEXT, genai.Modality.IMAGE],
    generation_config={
        "imageConfig": {
            "aspectRatio": "16:9",
            "imageSize": "2K"
        }
    },
    safety_settings={
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE"
    }
)

# 5. Pricing Calculator
def calculate_cost(num_images, model="gemini-2.5-flash-image"):
    costs = {
        "gemini-2.5-flash-image": 0.039,
        "gemini-3-pro-image-preview": 0.12,
        "imagen-3.0-generate-002": 0.03
    }
    return num_images * costs.get(model, 0)
```

---

**End of Document**

For questions, updates, or additional research needs, refer to the official Google AI documentation or consult the deep-researcher agent.
