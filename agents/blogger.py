from services.data_fetcher import get_stock_data
from services.ai_clients import ai_clients
from datetime import datetime


class BloggerAgent:
    def __init__(self):
        pass

    def generate_blog_post(self, ticker, analysis_data=None):
        """Generate blog post using Ollama Llama 3"""
        try:
            stock_data = get_stock_data(ticker)

            prompt = f"""
            Create a professional investment blog post about {ticker} ({stock_data.get('company_name', ticker)}).

            Stock Data:
            - Price: ${stock_data.get('current_price', 'N/A')}
            - P/E: {stock_data.get('pe_ratio', 'N/A')}
            - Market Cap: ${stock_data.get('market_cap', 'N/A'):,}
            - Sector: {stock_data.get('sector', 'N/A')}
            - Industry: {stock_data.get('industry', 'N/A')}

            Additional Analysis: {analysis_data.get('reason', 'No additional analysis') if analysis_data else 'No additional analysis'}

            Create a comprehensive blog post including:
            1. Engaging title and introduction
            2. Company overview and business model
            3. Financial analysis and valuation
            4. Investment thesis and recommendation
            5. Risk factors and considerations
            6. Conclusion and future outlook

            Write in professional, engaging tone for investors. Use markdown formatting with headers, bullet points, and clear sections.
            """

            # Use Ollama Llama 3 for content generation
            blog_post = ai_clients.ollama_llama_analysis(prompt)

            # Fallback if Ollama fails
            if "Error" in blog_post:
                blog_post = ai_clients.fallback_analysis(ticker, "blog")

            return {
                "success": True,
                "ticker": ticker,
                "blog_post": blog_post,
                "formatted_date": datetime.now().strftime('%Y-%m-%d'),
                "raw_data": stock_data,
                "llm_used": "Ollama Llama 3"
            }

        except Exception as e:  # error handler in case of different failures
            return {
                "success": False,
                "error": str(e),
                "ticker": ticker
            }


blogger_agent = BloggerAgent()
