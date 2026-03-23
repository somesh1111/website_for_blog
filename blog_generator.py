from google import genai
from google.genai import types

class BlogGenerator:

    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def generate_blog(self, notification, stock_history):

        # Your original prompt preserved exactly as requested
        prompt = f"""
You are a professional financial journalist who writes detailed stock market articles similar to financial media websites like Moneycontrol, Economic Times Markets, and Business Standard.

Convert the following stock market notification into a professional financial blog article.

IMPORTANT GLOBAL RULES
- Return ONLY clean readable text.
- Do NOT use markdown like ## or **.
- Do NOT use HTML tags.
- Do NOT wrap output in ``` or ```html code blocks.
- Write the article in a professional financial journalism style.
- Write in clear paragraphs with proper section titles.
- Never mention missing information.
- Never write phrases like "the notification does not mention", "not provided in the notification", "not detailed in the notification", or similar.
- Do not explain data availability.
- The article should read like a complete financial news story written for investors.

ARTICLE STRUCTURE

Title  
Create a strong SEO-friendly headline similar to financial news websites.

Synopsis  
Write a short 2–3 sentence summary explaining the key development and why the stock may attract investor attention.

What’s the News?  
Explain the order, contract, or announcement clearly including:
- Order value
- Client or awarding authority
- Execution timeline if available
- Strategic importance of the deal
- How the project strengthens the company’s position in its sector

Stock Performance  

Explain the stock movement and performance in a natural financial commentary style.

Include:
- Latest stock price movement around the time of the announcement if available.
- Stock performance trend over the last 3 months.
- Stock performance trend over the last 1 year.

WRITING RULES FOR STOCK PERFORMANCE
- Do not refer to the notification while describing performance.
- Do not say that information is missing.
- Write the analysis as a natural market commentary.

If exact numbers are not available:
- Describe the general trend such as strong growth, moderate growth, sideways consolidation, correction, or decline.
- Focus on market trend, investor sentiment, and historical movement rather than explaining missing numbers.

Order Book Value
Explain how the new contract strengthens the company’s project pipeline and improves revenue visibility.

TASK: Use the Google Search tool to confirm and include the company's latest consolidated order book value. 
(Note for example: As of Q3 FY26, the official figure was reported).

Discuss:
- The current total order book figure and what this scale signifies for a mid-cap infrastructure player.
- The strategic importance of the new order in relation to this existing backlog.
- The company’s consistent ability to win large-scale, technically complex contracts.
- How these combined factors contribute to long-term growth and execution stability.

Do NOT state that this information was "searched" or "provided in a prompt." Integrate it seamlessly into the financial report.

Business Overview  

Explain what the company does, its core business segments, and the sectors it operates in.

Mention:
- Major business areas
- Key industry segments
- Typical clients or project types

Financial Overview  

Provide a brief overview of the company’s financial profile such as:

- Revenue growth trend
- Profitability trend
- Market capitalization if known
- Price-to-Earnings (P/E) ratio if relevant
- Overall financial strength or market positioning

Write this section like a financial analyst summarizing the company’s financial standing.

STYLE REQUIREMENTS

- The article should read like a professional financial news report.
- Maintain a neutral, analytical tone suitable for investors.
- Write clearly structured paragraphs under each section title.
- Avoid speculation beyond reasonable financial commentary.

Use the following historical stock data if useful.

Stock Data History:
{stock_history}

Notification:
{notification}
"""

        # 1. Create the Google Search tool for live grounding
        grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )

        # 2. Configuration to use the tool with gemini-3-flash-preview
        config = types.GenerateContentConfig(
            tools=[grounding_tool],
            temperature=0.1
        )

        # 3. Generate content using your specific model choice
        response = self.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=config,
        )

        blog = response.text

        # Cleanup logic to remove code blocks if model ignores instructions
        blog = blog.replace("```html", "")
        blog = blog.replace("```", "")

        # Optional: Log the prompt for debugging
        with open("prompt.txt", "w", encoding="utf8") as file:
            file.write(prompt)

        return blog.strip()