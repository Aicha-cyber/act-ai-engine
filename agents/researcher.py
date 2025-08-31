from services.data_fetcher import get_stock_data
from services.ai_clients import ai_clients


class ResearchAgent:
    def __init__(self):
        pass

    def analyze_stock(self, ticker):
        # Analyze stock using OpenAI GPT-4
        try:
            stock_data = get_stock_data(ticker)
            # construct a natural language prompt with the data
            prompt = f"""
            Conduct comprehensive research on {ticker} ({stock_data.get('company_name', ticker)}).

            Company Data:
            - Current Price: ${stock_data.get('current_price', 'N/A')}
            - P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
            - Market Cap: ${stock_data.get('market_cap', 'N/A'):,}
            - Sector: {stock_data.get('sector', 'N/A')}
            - Industry: {stock_data.get('industry', 'N/A')}

            Provide detailed analysis covering:
            1. Company overview and business model
            2. Recent financial performance and trends
            3. Competitive position in the industry
            4. Growth prospects and potential risks
            5. Analyst sentiment and market outlook

            Return a well-structured research report in markdown format.
            """

            # Use OpenAI for analysis
            research_report = ai_clients.openai_analysis(prompt)

            # Fallback if OpenAI fails
            if "Error" in research_report:
                research_report = ai_clients.fallback_analysis(ticker, "research")

            return {
                "success": True,
                "ticker": ticker,
                "research_report": research_report,
                "raw_data": stock_data,
                "llm_used": "OpenAI GPT-4"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "ticker": ticker
            }


research_agent = ResearchAgent()
