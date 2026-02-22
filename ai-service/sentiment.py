"""Sentiment analysis module for resort reviews.

Uses LangChain and OpenAI to analyze customer review sentiment,
extract key topics, and provide actionable insights.
"""

import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


class SentimentLabel(str, Enum):
    """Sentiment classification labels."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class SentimentResult(BaseModel):
    """Sentiment analysis result schema."""
    sentiment: SentimentLabel = Field(description="Overall sentiment label")
    confidence: float = Field(description="Confidence score (0-1)", ge=0, le=1)
    score: float = Field(description="Sentiment score (-1 to 1)", ge=-1, le=1)
    key_topics: List[str] = Field(default=[], description="Key topics mentioned")
    aspects: Dict[str, Any] = Field(default={}, description="Aspect-level sentiment")
    summary: str = Field(description="Brief summary of the review")


@dataclass
class ReviewAnalysis:
    """Complete review analysis result."""
    review_id: str
    text: str
    sentiment: SentimentLabel
    confidence: float
    score: float
    key_topics: List[str]
    aspects: Dict[str, Any]
    summary: str
    action_required: bool = False
    priority: str = "low"


class SentimentAnalyzer:
    """Sentiment analyzer using OpenAI GPT."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the sentiment analyzer.
        
        Args:
            api_key: OpenAI API key (defaults to env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required")
        
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=self.api_key
        )
        
        self.parser = JsonOutputParser(pydantic_object=SentimentResult)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a sentiment analysis expert for hotel and resort reviews.
Analyze the following review and provide:
1. Overall sentiment (positive/neutral/negative)
2. Confidence score (0-1)
3. Sentiment score (-1 to 1, where -1 is very negative, 1 is very positive)
4. Key topics mentioned (e.g., cleanliness, service, food, location, amenities)
5. Aspect-level sentiment for: service, cleanliness, location, value, amenities
6. Brief 1-sentence summary

Respond in JSON format matching the schema."""),
            ("human", "Review: {review_text}")
        ])
        
        self.chain = self.prompt | self.llm | self.parser
    
    async def analyze_review(self, review_text: str, review_id: str = "") -> ReviewAnalysis:
        """Analyze a single review.
        
        Args:
            review_text: The review text to analyze
            review_id: Optional review identifier
            
        Returns:
            ReviewAnalysis with complete sentiment data
        """
        try:
            result: SentimentResult = await self.chain.ainvoke({
                "review_text": review_text
            })
            
            # Determine if action is required
            action_required = (
                result.sentiment == SentimentLabel.NEGATIVE and 
                result.confidence > 0.7
            )
            
            # Set priority based on sentiment and confidence
            priority = "low"
            if result.sentiment == SentimentLabel.NEGATIVE:
                if result.confidence > 0.9:
                    priority = "high"
                elif result.confidence > 0.7:
                    priority = "medium"
            
            return ReviewAnalysis(
                review_id=review_id,
                text=review_text,
                sentiment=result.sentiment,
                confidence=result.confidence,
                score=result.score,
                key_topics=result.key_topics,
                aspects=result.aspects,
                summary=result.summary,
                action_required=action_required,
                priority=priority
            )
            
        except Exception as e:
            # Fallback: return neutral sentiment on error
            return ReviewAnalysis(
                review_id=review_id,
                text=review_text,
                sentiment=SentimentLabel.NEUTRAL,
                confidence=0.0,
                score=0.0,
                key_topics=[],
                aspects={},
                summary=f"Analysis failed: {str(e)}",
                action_required=False,
                priority="low"
            )
    
    async def analyze_batch(
        self, 
        reviews: List[Dict[str, str]]
    ) -> List[ReviewAnalysis]:
        """Analyze multiple reviews in batch.
        
        Args:
            reviews: List of dicts with 'id' and 'text' keys
            
        Returns:
            List of ReviewAnalysis results
        """
        results = []
        for review in reviews:
            analysis = await self.analyze_review(
                review_text=review.get("text", ""),
                review_id=review.get("id", "")
            )
            results.append(analysis)
        return results
    
    def get_aggregate_stats(
        self, 
        analyses: List[ReviewAnalysis]
    ) -> Dict[str, Any]:
        """Get aggregate statistics from multiple analyses.
        
        Args:
            analyses: List of review analyses
            
        Returns:
            Dictionary with aggregate stats
        """
        if not analyses:
            return {
                "total_reviews": 0,
                "average_sentiment": 0,
                "sentiment_distribution": {},
                "top_topics": [],
                "action_required_count": 0
            }
        
        total = len(analyses)
        sentiment_counts = {
            "positive": sum(1 for a in analyses if a.sentiment == SentimentLabel.POSITIVE),
            "neutral": sum(1 for a in analyses if a.sentiment == SentimentLabel.NEUTRAL),
            "negative": sum(1 for a in analyses if a.sentiment == SentimentLabel.NEGATIVE)
        }
        
        avg_score = sum(a.score for a in analyses) / total
        
        # Collect all topics
        all_topics = []
        for analysis in analyses:
            all_topics.extend(analysis.key_topics)
        
        # Count topic frequency
        topic_counts = {}
        for topic in all_topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        # Get top 5 topics
        top_topics = sorted(
            topic_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        action_required = sum(1 for a in analyses if a.action_required)
        
        return {
            "total_reviews": total,
            "average_sentiment": round(avg_score, 2),
            "sentiment_distribution": sentiment_counts,
            "sentiment_percentages": {
                k: round(v / total * 100, 1) 
                for k, v in sentiment_counts.items()
            },
            "top_topics": [
                {"topic": t[0], "mentions": t[1]} 
                for t in top_topics
            ],
            "action_required_count": action_required,
            "high_priority_count": sum(
                1 for a in analyses if a.priority == "high"
            )
        }


# Singleton instance
_analyzer: Optional[SentimentAnalyzer] = None


def get_analyzer() -> SentimentAnalyzer:
    """Get or create sentiment analyzer singleton."""
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentAnalyzer()
    return _analyzer
