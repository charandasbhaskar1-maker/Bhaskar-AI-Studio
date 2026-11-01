Bhaskar AI Studio – Backend

Bhaskar AI Studio का Backend FastAPI पर बनाया जा रहा है।

वर्तमान सुविधाएँ

- FastAPI application
- Health check API
- Storyboard planning API
- Hindi, Chhattisgarhi और English भाषा का समर्थन
- Photorealistic Cinematic सहित अलग-अलग visual styles
- 1 से 10 scenes तक storyboard planning

आवश्यकताएँ

Python 3.10 या उससे नया संस्करण।

Installation

pip install -r requirements.txt

Run

uvicorn main:app --reload

API Endpoints

- "GET /" – Backend status
- "GET /health" – Health check
- "POST /api/storyboard" – Storyboard planning

API documentation:

"/docs"

Important

यह शुरुआती Backend version है। वास्तविक AI image, video और audio generation अभी connected नहीं है। AI providers और secure cloud services आगे के चरणों में जोड़े जाएँगे।

Project: Bhaskar AI Studio
Version: 0.1.0