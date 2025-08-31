from services.data_fetcher import get_stock_data
from services.ai_clients import ai_clients


class RecommenderAgent:
    def __init__(self):
        pass

    def generate_recommendation(self, ticker):
        """Generate recommendation using Ollama Mistral"""
        try:
            stock_data = get_stock_data(ticker)

            prompt = f"""
            Provide investment recommendation for {ticker} ({stock_data.get('company_name', ticker)}).

            Key Data:
            - Price: ${stock_data.get('current_price', 'N/A')}
            - P/E: {stock_data.get('pe_ratio', 'N/A')}
            - Market Cap: ${stock_data.get('market_cap', 'N/A'):,}
            - Sector: {stock_data.get('sector', 'N/A')}

            Analyze and provide:
            1. BUY/SELL/HOLD recommendation
            2. Confidence level (High/Medium/Low)
            3. Detailed reasoning
            4. Risk assessment
            5. Time horizon (Short/Medium/Long-term)
            6. Price target if possible

            Return in structured format.
            """

            # Use Ollama Mistral for risk-aware recommendations
            recommendation_analysis = ai_clients.ollama_mistral_analysis(prompt)

            # Fallback if Ollama fails
            if "Error" in recommendation_analysis:
                recommendation_analysis = ai_clients.fallback_analysis(ticker, "recommendation")
                recommendation = "HOLD"
                confidence = "Low"
                reason = "LLM analysis required"
            else:
                # Parse the recommendation from Mistral output
                recommendation = self._parse_recommendation(recommendation_analysis)
                confidence = self._parse_confidence(recommendation_analysis)
                reason = recommendation_analysis

            return {
                "success": True,
                "ticker": ticker,
                "recommendation": recommendation,
                "confidence": confidence,
                "reason": reason,
                "analysis": recommendation_analysis,
                "raw_data": stock_data,
                "llm_used": "Ollama Mistral"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "ticker": ticker
            }

    def _parse_recommendation(self, analysis):
        """Parse recommendation from LLM output"""
        analysis_lower = analysis.lower()
        if "buy" in analysis_lower:
            return "BUY"
        elif "sell" in analysis_lower:
            return "SELL"
        else:
            return "HOLD"

    def _parse_confidence(self, analysis):
        """"Parse confidence level from LLM output"""
        analysis_lower = analysis.lower()
        if "high confidence" in analysis_lower:
            return "High"
        elif "medium confidence" in analysis_lower:
            return "Medium"
        else:
            return "Low"


recommender_agent = RecommenderAgent()
