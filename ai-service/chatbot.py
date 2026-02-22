from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import redis
import json
import asyncio
import openai
from datetime import datetime
import os
from contextlib import asynccontextmanager

# Import sentiment analysis
from sentiment import SentimentAnalyzer, SentimentLabel, get_analyzer, ReviewAnalysis

# Models
class ChatRequest(BaseModel):
    message: str
    session_id: str
    current_page: Optional[str] = None
    current_product_id: Optional[int] = None

class UpsellRequest(BaseModel):
    session_id: str
    user_action: str
    product_id: int

class ProductSuggestion(BaseModel):
    name: str
    slug: str
    price: float
    image: str

class ChatResponse(BaseModel):
    reply: str
    suggestions: List[ProductSuggestion] = []
    action: Optional[str] = None

class UpsellResponse(BaseModel):
    suggestion: str
    product: ProductSuggestion

# Global variables
redis_client = None
products_data = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client, products_data
    # Startup
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    products_data = await load_products_from_db()
    yield
    # Shutdown
    if redis_client:
        redis_client.close()

app = FastAPI(
    title="الخيمة Beach Resort AI Chatbot",
    description="AI Assistant for resort booking and information",
    version="1.0.0",
    lifespan=lifespan
)

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY", "your-openai-key")

async def load_products_from_db() -> List[Dict]:
    """Load products from database - mock for now"""
    return [
        {
            "id": 1,
            "name": "VIP Beach Access",
            "name_ar": "دخول شاطئ VIP",
            "slug": "vip-beach",
            "price": 150.0,
            "image": "/images/vip-beach.jpg",
            "description": "Premium beach experience with private cabana"
        },
        {
            "id": 2,
            "name": "Standard Beach Access",
            "name_ar": "دخول شاطئ عادي",
            "slug": "standard-beach",
            "price": 75.0,
            "image": "/images/standard-beach.jpg",
            "description": "Regular beach access with basic amenities"
        },
        {
            "id": 3,
            "name": "Deluxe Room",
            "name_ar": "غرفة ديلوكس",
            "slug": "deluxe-room",
            "price": 300.0,
            "image": "/images/deluxe-room.jpg",
            "description": "Spacious room with sea view"
        }
    ]

def detect_language(text: str) -> str:
    """Simple language detection"""
    arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
    return "ar" if arabic_chars > len(text) * 0.3 else "en"

def get_system_prompt(current_product: Optional[Dict] = None, lang: str = "en") -> str:
    """Generate system prompt with current context"""
    products_list = "\n".join([
        f"- {p['name']} ({p['name_ar']}): ${p['price']}" 
        for p in products_data
    ])
    
    current_season = "winter" if datetime.now().month in [12, 1, 2] else "summer"
    
    base_prompt = f"""You are the helpful AI assistant for الخيمة Beach Resort in Sharm El Sheikh.
You speak Arabic and English fluently. Respond in {'Arabic' if lang == 'ar' else 'English'}.
You ONLY answer questions about the resort's services: rooms, beach, activities, events, packages.
You are warm, friendly, and subtly suggest upgrades when relevant.

Available products:
{products_list}

Current season: {current_season}
Booking link format: /booking/{{product_slug}}

NEVER make up prices — use exact prices from the products list above.
Always suggest booking links for specific products."""

    if current_product:
        base_prompt += f"\n\nUser is currently viewing: {current_product['name']} (${current_product['price']})"
    
    return base_prompt

async def get_chat_history(session_id: str) -> List[Dict]:
    """Get chat history from Redis"""
    try:
        history_json = redis_client.get(f"chat:{session_id}")
        return json.loads(history_json) if history_json else []
    except:
        return []

async def save_chat_history(session_id: str, history: List[Dict]):
    """Save chat history to Redis with TTL"""
    try:
        # Keep only last 10 messages
        history = history[-10:]
        redis_client.setex(f"chat:{session_id}", 3600, json.dumps(history))
    except Exception as e:
        print(f"Error saving chat history: {e}")

async def call_gpt(messages: List[Dict], use_gpt4: bool = False) -> str:
    """Call OpenAI API"""
    try:
        model = "gpt-4o" if use_gpt4 else "gpt-4o-mini"
        
        client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-test-key"))
        
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "عذراً، حدث خطأ في النظام. يرجى المحاولة مرة أخرى." if detect_language(messages[-1]["content"]) == "ar" else "Sorry, there was a system error. Please try again."

def get_product_suggestions(message: str, current_product_id: Optional[int] = None) -> List[ProductSuggestion]:
    """Generate product suggestions based on message content"""
    suggestions = []
    message_lower = message.lower()
    
    # Simple keyword matching for suggestions
    if any(word in message_lower for word in ["beach", "شاطئ", "sea", "بحر"]):
        for product in products_data:
            if "beach" in product["slug"] and product["id"] != current_product_id:
                suggestions.append(ProductSuggestion(**product))
    
    if any(word in message_lower for word in ["room", "غرفة", "stay", "إقامة"]):
        for product in products_data:
            if "room" in product["slug"] and product["id"] != current_product_id:
                suggestions.append(ProductSuggestion(**product))
    
    return suggestions[:3]  # Max 3 suggestions

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        # Detect language
        lang = detect_language(request.message)
        
        # Get current product context
        current_product = None
        if request.current_product_id:
            current_product = next((p for p in products_data if p["id"] == request.current_product_id), None)
        
        # Get chat history
        history = await get_chat_history(request.session_id)
        
        # Build messages for GPT
        messages = [{"role": "system", "content": get_system_prompt(current_product, lang)}]
        
        # Add history
        for msg in history:
            messages.append(msg)
        
        # Add current message
        messages.append({"role": "user", "content": request.message})
        
        # Determine if we need GPT-4 (complex queries)
        use_gpt4 = len(request.message) > 100 or any(word in request.message.lower() for word in ["compare", "difference", "قارن", "فرق"])
        
        # Call GPT
        reply = await call_gpt(messages, use_gpt4)
        
        # Update history
        history.append({"role": "user", "content": request.message})
        history.append({"role": "assistant", "content": reply})
        await save_chat_history(request.session_id, history)
        
        # Generate suggestions
        suggestions = get_product_suggestions(request.message, request.current_product_id)
        
        return ChatResponse(
            reply=reply,
            suggestions=suggestions
        )
        
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/chat/stream")
async def chat_stream(message: str, session_id: str, current_page: Optional[str] = None, current_product_id: Optional[int] = None):
    """Streaming chat endpoint"""
    async def generate():
        try:
            # Use the same logic as regular chat but stream the response
            request = ChatRequest(
                message=message,
                session_id=session_id,
                current_page=current_page,
                current_product_id=current_product_id
            )
            
            response = await chat(request)
            
            # Stream the response word by word
            words = response.reply.split()
            for i, word in enumerate(words):
                yield f"data: {json.dumps({'word': word, 'is_final': i == len(words) - 1})}\n\n"
                await asyncio.sleep(0.1)
                
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/plain")

@app.post("/chat/upsell", response_model=UpsellResponse)
async def upsell(request: UpsellRequest):
    """Generate contextual upsell suggestions"""
    try:
        # Get the product being viewed
        current_product = next((p for p in products_data if p["id"] == request.product_id), None)
        if not current_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Get chat history for context
        history = await get_chat_history(request.session_id)
        
        # Find a relevant upsell product
        upsell_product = None
        if "beach" in current_product["slug"]:
            # If viewing standard beach, suggest VIP
            if current_product["price"] < 100:
                upsell_product = next((p for p in products_data if "vip" in p["slug"].lower()), None)
        elif "room" in current_product["slug"]:
            # Suggest higher tier room or beach access
            upsell_product = next((p for p in products_data if p["price"] > current_product["price"]), None)
        
        if not upsell_product:
            upsell_product = products_data[0]  # Fallback
        
        # Generate contextual suggestion
        lang = "ar" if history and detect_language(history[-1].get("content", "")) == "ar" else "en"
        
        if lang == "ar":
            suggestion = f"لتجربة أفضل، جرب {upsell_product['name_ar']} بسعر ${upsell_product['price']}"
        else:
            suggestion = f"For a better experience, try {upsell_product['name']} at ${upsell_product['price']}"
        
        return UpsellResponse(
            suggestion=suggestion,
            product=ProductSuggestion(**upsell_product)
        )
        
    except Exception as e:
        print(f"Upsell error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Sentiment Analysis Models
class SentimentRequest(BaseModel):
    review_text: str
    review_id: Optional[str] = None

class BatchSentimentRequest(BaseModel):
    reviews: List[Dict[str, str]]  # List of {id, text} dicts

class SentimentResponse(BaseModel):
    review_id: str
    sentiment: str
    confidence: float
    score: float
    key_topics: List[str]
    aspects: Dict[str, Any]
    summary: str
    action_required: bool
    priority: str

class AggregateStatsResponse(BaseModel):
    total_reviews: int
    average_sentiment: float
    sentiment_distribution: Dict[str, int]
    sentiment_percentages: Dict[str, float]
    top_topics: List[Dict[str, Any]]
    action_required_count: int
    high_priority_count: int

# Sentiment Analysis Endpoints
@app.post("/analyze-sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """Analyze sentiment of a single review."""
    try:
        analyzer = get_analyzer()
        result = await analyzer.analyze_review(
            review_text=request.review_text,
            review_id=request.review_id or ""
        )
        
        return SentimentResponse(
            review_id=result.review_id,
            sentiment=result.sentiment.value,
            confidence=result.confidence,
            score=result.score,
            key_topics=result.key_topics,
            aspects=result.aspects,
            summary=result.summary,
            action_required=result.action_required,
            priority=result.priority
        )
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-sentiment/batch", response_model=List[SentimentResponse])
async def analyze_sentiment_batch(request: BatchSentimentRequest):
    """Analyze sentiment of multiple reviews in batch."""
    try:
        analyzer = get_analyzer()
        results = await analyzer.analyze_batch(request.reviews)
        
        return [
            SentimentResponse(
                review_id=r.review_id,
                sentiment=r.sentiment.value,
                confidence=r.confidence,
                score=r.score,
                key_topics=r.key_topics,
                aspects=r.aspects,
                summary=r.summary,
                action_required=r.action_required,
                priority=r.priority
            )
            for r in results
        ]
    except Exception as e:
        print(f"Batch sentiment analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-sentiment/stats", response_model=AggregateStatsResponse)
async def analyze_sentiment_stats(request: BatchSentimentRequest):
    """Get aggregate sentiment statistics for multiple reviews."""
    try:
        analyzer = get_analyzer()
        analyses = await analyzer.analyze_batch(request.reviews)
        stats = analyzer.get_aggregate_stats(analyses)
        
        return AggregateStatsResponse(**stats)
    except Exception as e:
        print(f"Sentiment stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test Redis connection
        redis_client.ping()
        return {"status": "healthy", "redis": "connected", "products_loaded": len(products_data)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
