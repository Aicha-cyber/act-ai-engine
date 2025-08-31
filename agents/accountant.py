from services.data_fetcher import get_stock_data
from services.ai_clients import ai_clients


class AccountantAgent:
    def __init__(self):
        pass

    def analyze_financials(self, ticker):
        """Analyze financials using Groq API"""
        try:
            stock_data = get_stock_data(ticker)  # Get basic stock info
            # build llm prompt dynamically with the stock info
            prompt = f"""
            Analyze financial ratios and valuation for {ticker} ({stock_data.get('company_name', ticker)}).

            Financial Data:
            - Current Price: ${stock_data.get('current_price', 'N/A')}
            - P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
            - Market Cap: ${stock_data.get('market_cap', 'N/A'):,}
            - Sector: {stock_data.get('sector', 'N/A')}
            - Industry: {stock_data.get('industry', 'N/A')}

            Provide comprehensive financial analysis covering:
            1. Valuation assessment (P/E, P/S, P/B ratios)
            2. Profitability metrics and trends
            3. Liquidity and solvency ratios
            4. Comparison with industry peers
            5. Financial health score (1-10)

            Return structured financial analysis in markdown format.
            """

            # Use Groq for financial analysis
            financial_analysis = ai_clients.groq_analysis(prompt)

            # Fallback if Groq fails
            if "Error" in financial_analysis:
                financial_analysis = ai_clients.fallback_analysis(ticker, "accounting")

            return {
                "success": True,
                "ticker": ticker,
                "financial_analysis": financial_analysis,
                "raw_data": stock_data,
                "llm_used": "Groq Mixtral"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "ticker": ticker
            }


accountant_agent = AccountantAgent()
