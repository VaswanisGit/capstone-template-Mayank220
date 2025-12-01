# Market Tools
from typing import List, Dict, Any

class MarketTools:
    @staticmethod
    def search_market(query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Deterministic placeholder for market search.
        Returns a list of dicts with title, snippet, provenance.
        """
        print(f"    [MarketTools] Searching for: {query}")
        
        q_lower = query.lower()
        
        # Sector-specific simulated data
        sectors = {
            "ai": {
                "market": "The Artificial Intelligence market is projected to reach $407B by 2027. Key growth areas include Generative AI and automation.",
                "competitors": "Major players include OpenAI, Google, and Anthropic. Niche verticals are becoming crowded.",
                "trends": "Enterprises are moving from experimentation to deployment. Data privacy and regulation are top concerns."
            },
            "pet": {
                "market": "The Global Pet Care market is valued at $235B. Owners are increasingly treating pets as family members ('humanization').",
                "competitors": "Dominant players include Rover, Wag, and Chewy. Local services remain highly fragmented.",
                "trends": "Premiumization of pet food and tech-enabled pet services (health monitoring, smart toys) are trending."
            },
            "food": {
                "market": "The Food Delivery and Tech market is maturing. Unit economics and profitability are now prioritized over growth at all costs.",
                "competitors": "UberEats, DoorDash, and local ghost kitchens dominate. Direct-to-consumer meal kits are seeing consolidation.",
                "trends": "Sustainability, plant-based options, and hyper-local delivery are key consumer demands."
            },
            "health": {
                "market": "Digital Health is stabilizing after the pandemic boom. Focus is shifting to hybrid care models and mental health.",
                "competitors": "Teladoc, Zocdoc, and specialized vertical players. Traditional providers are also entering the digital space.",
                "trends": "Telemedicine, wearable integration, and personalized medicine are driving the next wave of innovation."
            },
             "crypto": {
                "market": "The Cryptocurrency market remains volatile but institutional adoption is increasing via ETFs and tokenization.",
                "competitors": "Coinbase, Binance, and decentralized exchanges (DEXs). Regulation is a major competitive factor.",
                "trends": "DeFi, NFTs, and Layer 2 scaling solutions are the primary areas of technical development."
            }
        }
        
        # Default generic data
        selected_sector = "general"
        data = {
            "market": f"The market for '{query}' shows potential but requires clear differentiation. Early stage validation is critical.",
            "competitors": f"Direct competitors for '{query}' may be undefined, but indirect substitutes likely exist.",
            "trends": "Consumers are looking for convenience and value. Adoption will depend on user experience."
        }
        
        # Check for keywords
        for key, sector_data in sectors.items():
            if key in q_lower or (key == "pet" and ("dog" in q_lower or "cat" in q_lower)):
                selected_sector = key
                data = sector_data
                break
        
        return [
            {
                "title": f"Market Overview: {selected_sector.upper()} Sector",
                "snippet": data["market"],
                "provenance": f"simulated_{selected_sector}_report_2024"
            },
            {
                "title": f"Competitive Landscape: {selected_sector.upper()}",
                "snippet": data["competitors"],
                "provenance": f"simulated_{selected_sector}_competitor_db"
            },
            {
                "title": f"Key Trends: {selected_sector.upper()}",
                "snippet": data["trends"],
                "provenance": f"simulated_{selected_sector}_trends"
            }
        ][:k]
