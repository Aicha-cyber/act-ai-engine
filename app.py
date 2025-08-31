from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from agents.researcher import research_agent
from agents.accountant import accountant_agent
from agents.recommender import recommender_agent
from agents.blogger import blogger_agent
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)


# connect the root URL (GET /) to the home()
@app.route("/")
def home():
    return jsonify({
        "message": "ACT-AI Engine is running!",
        "status": "success",
        "version": "1.0.0",
        "agents": ["research", "accounting", "recommender", "blogger"]
    })


# GET /health - a simple health check
@app.route("/health")
def health_check():
    return jsonify({"status": "healthy", "service": "ACT-AI Engine"})


# POST /analyze - the main analysis workflow
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        if not data or 'ticker' not in data:
            return jsonify({"error": "Missing 'ticker' in request body"}), 400

        ticker = data.get('ticker', 'AAPL').upper()

        # Use all four agents for comprehensive analysis
        # Researcher: basic context & fundamentals
        research_result = research_agent.analyze_stock(ticker)
        # Accountant: ratio/financial health analysis
        accounting_result = accountant_agent.analyze_financials(ticker)
        # Recommender: buy/sell/hold
        recommendation_result = recommender_agent.generate_recommendation(ticker)
        # Blogger: formatted markdown report
        blog_result = blogger_agent.generate_blog_post(ticker, recommendation_result)

        return jsonify({
            "ticker": ticker,
            "research": research_result,
            "accounting": accounting_result,
            "recommendation": recommendation_result,
            "blog": blog_result,
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    print("Starting ACT-AI Engine...")
    print(f"Debug mode: {debug_mode}")
    print(f"Running on port: {port}")

    app.run(host="0.0.0.0", port=port, debug=debug_mode)
