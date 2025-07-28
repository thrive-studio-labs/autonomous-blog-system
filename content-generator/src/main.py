import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'content-generator-secret-key')
CORS(app)

# Initialize OpenAI client
openai.api_key = os.environ.get('OPENAI_API_KEY')

class AIContentGenerator:
    """
    AI-powered content generator for 'AI for Everyone' blog.
    """
    
    def __init__(self):
        self.blog_niche = "AI for Everyone"
        self.target_audience = "AI-curious professionals and beginners"
        self.content_style = "Educational, accessible, practical"
        
    def generate_article(self, topic: str, word_count: int = 1500) -> Dict:
        """
        Generate a complete blog article about AI topics.
        
        Args:
            topic: The main topic/keyword for the article
            word_count: Target word count for the article
            
        Returns:
            Dictionary containing title, content, excerpt, tags, and categories
        """
        try:
            # Generate article outline first
            outline_prompt = f"""
            Create a detailed outline for a blog post about "{topic}" for the "AI for Everyone" blog.
            
            Target audience: AI-curious professionals and beginners who want practical AI knowledge
            Blog mission: Making AI accessible to everyone
            Style: Educational, friendly, practical with real-world examples
            
            Include:
            1. Compelling title (SEO-optimized)
            2. 5-7 main sections with subsections
            3. Key points to cover in each section
            4. Practical examples or use cases
            5. Actionable takeaways
            
            Focus on practical value and accessibility.
            """
            
            outline_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": outline_prompt}],
                max_tokens=800,
                temperature=0.7
            )
            
            outline = outline_response.choices[0].message.content
            
            # Generate full article based on outline
            article_prompt = f"""
            Write a comprehensive blog post based on this outline:
            
            {outline}
            
            Requirements:
            - Target length: {word_count} words
            - Write for "AI for Everyone" blog
            - Audience: Professionals curious about AI but not necessarily technical
            - Tone: Friendly, educational, encouraging
            - Include practical examples and real-world applications
            - Make complex concepts simple and accessible
            - Add actionable tips readers can implement
            - Use subheadings for better readability
            - Include a compelling introduction and conclusion
            
            Format as clean HTML with proper headings (h2, h3), paragraphs, and lists where appropriate.
            """
            
            article_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": article_prompt}],
                max_tokens=3000,
                temperature=0.7
            )
            
            content = article_response.choices[0].message.content
            
            # Generate SEO metadata
            seo_prompt = f"""
            Based on this article content about "{topic}", generate:
            
            1. SEO-optimized title (under 60 characters)
            2. Meta description (under 160 characters)
            3. 5-8 relevant tags
            4. 2-3 categories
            
            Article preview: {content[:500]}...
            
            Format as JSON:
            {{
                "title": "SEO title",
                "excerpt": "Meta description",
                "tags": ["tag1", "tag2", "tag3"],
                "categories": ["category1", "category2"]
            }}
            """
            
            seo_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": seo_prompt}],
                max_tokens=300,
                temperature=0.5
            )
            
            try:
                seo_data = json.loads(seo_response.choices[0].message.content)
            except:
                # Fallback SEO data
                seo_data = {
                    "title": f"Understanding {topic}: A Beginner's Guide to AI",
                    "excerpt": f"Learn everything you need to know about {topic} in AI. Practical guide for beginners and professionals.",
                    "tags": ["AI", "artificial intelligence", "technology", "beginners"],
                    "categories": ["AI Basics", "Technology"]
                }
            
            return {
                'success': True,
                'title': seo_data['title'],
                'content': content,
                'excerpt': seo_data['excerpt'],
                'tags': seo_data['tags'],
                'categories': seo_data['categories'],
                'word_count': len(content.split()),
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Content generation error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def suggest_topics(self, count: int = 10) -> List[str]:
        """Generate topic suggestions for AI blog content."""
        try:
            prompt = f"""
            Generate {count} engaging blog post topics for "AI for Everyone" blog.
            
            Focus on:
            - Practical AI applications for everyday users
            - AI tool reviews and comparisons
            - Beginner-friendly AI concepts
            - AI career and skills development
            - AI ethics and responsible use
            - Current AI trends and news
            
            Make topics specific, actionable, and appealing to AI-curious professionals.
            Return as a simple list, one topic per line.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.8
            )
            
            topics = response.choices[0].message.content.strip().split('\n')
            return [topic.strip('- ').strip() for topic in topics if topic.strip()]
            
        except Exception as e:
            logger.error(f"Topic suggestion error: {str(e)}")
            return [
                "ChatGPT vs Claude: Which AI Assistant is Right for You?",
                "5 Ways AI Can Boost Your Productivity at Work",
                "Understanding Machine Learning: A Complete Beginner's Guide",
                "AI Tools Every Small Business Should Know About",
                "The Future of AI: What to Expect in 2025"
            ]

# Initialize content generator
content_generator = AIContentGenerator()

@app.route('/')
def index():
    """Content Generator dashboard."""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Content Generator - Thrive Studio Digital Labs</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .card { background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
            .btn:hover { background: #0056b3; }
            .status { padding: 10px 20px; border-radius: 5px; margin: 10px 0; }
            .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
            .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
            input[type="text"], input[type="number"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
            .article-preview { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; max-height: 400px; overflow-y: auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 AI Content Generator</h1>
                <p>Creating amazing content for "AI for Everyone" blog</p>
                <button class="btn" onclick="suggestTopics()">Get Topic Ideas</button>
            </div>
            
            <div class="card">
                <h2>📝 Generate New Article</h2>
                <form id="generateForm">
                    <input type="text" id="topic" placeholder="Article topic (e.g., 'ChatGPT for beginners')" required>
                    <input type="number" id="wordCount" placeholder="Word count (default: 1500)" value="1500">
                    <button type="submit" class="btn">Generate Article</button>
                </form>
                <div id="generateStatus"></div>
                <div id="articlePreview" class="article-preview" style="display: none;"></div>
            </div>
            
            <div class="card">
                <h2>💡 Topic Suggestions</h2>
                <div id="topicSuggestions"></div>
            </div>
            
            <div class="card">
                <h2>📊 Generator Status</h2>
                <p><strong>Service:</strong> AI Content Generator</p>
                <p><strong>Model:</strong> GPT-4 + GPT-3.5-turbo</p>
                <p><strong>Blog:</strong> AI for Everyone</p>
                <p><strong>Status:</strong> <span style="color: green;">Ready</span></p>
            </div>
        </div>

        <script>
            async function generateArticle(topic, wordCount) {
                const statusDiv = document.getElementById('generateStatus');
                const previewDiv = document.getElementById('articlePreview');
                
                statusDiv.innerHTML = '<div class="status">🤖 Generating AI content... This may take 30-60 seconds.</div>';
                previewDiv.style.display = 'none';
                
                try {
                    const response = await fetch('/api/generate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ topic, word_count: wordCount })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        statusDiv.innerHTML = `<div class="status success">✅ Article generated! ${result.word_count} words</div>`;
                        previewDiv.innerHTML = `
                            <h3>${result.title}</h3>
                            <p><strong>Excerpt:</strong> ${result.excerpt}</p>
                            <p><strong>Tags:</strong> ${result.tags.join(', ')}</p>
                            <p><strong>Categories:</strong> ${result.categories.join(', ')}</p>
                            <div style="border-top: 1px solid #ddd; padding-top: 15px; margin-top: 15px;">
                                ${result.content.substring(0, 1000)}...
                            </div>
                        `;
                        previewDiv.style.display = 'block';
                    } else {
                        statusDiv.innerHTML = `<div class="status error">❌ Generation failed: ${result.error}</div>`;
                    }
                } catch (error) {
                    statusDiv.innerHTML = `<div class="status error">❌ Error: ${error.message}</div>`;
                }
            }
            
            async function suggestTopics() {
                const suggestionsDiv = document.getElementById('topicSuggestions');
                suggestionsDiv.innerHTML = '<p>🤖 Generating topic ideas...</p>';
                
                try {
                    const response = await fetch('/api/topics');
                    const result = await response.json();
                    
                    if (result.success) {
                        const topicsList = result.topics.map(topic => 
                            `<li style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 5px; cursor: pointer;" 
                                onclick="document.getElementById('topic').value='${topic}'">${topic}</li>`
                        ).join('');
                        suggestionsDiv.innerHTML = `<ul style="list-style: none; padding: 0;">${topicsList}</ul>`;
                    } else {
                        suggestionsDiv.innerHTML = '<p>❌ Failed to generate topics</p>';
                    }
                } catch (error) {
                    suggestionsDiv.innerHTML = `<p>❌ Error: ${error.message}</p>`;
                }
            }
            
            document.getElementById('generateForm').addEventListener('submit', (e) => {
                e.preventDefault();
                const topic = document.getElementById('topic').value;
                const wordCount = parseInt(document.getElementById('wordCount').value) || 1500;
                generateArticle(topic, wordCount);
            });
        </script>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'content-generator',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/generate', methods=['POST'])
def generate_content():
    """Generate AI content for blog post."""
    try:
        data = request.get_json()
        
        if not data or not data.get('topic'):
            return jsonify({'success': False, 'error': 'Topic is required'}), 400
        
        topic = data['topic']
        word_count = data.get('word_count', 1500)
        
        result = content_generator.generate_article(topic, word_count)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Generate endpoint error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to generate content'
        }), 500

@app.route('/api/topics')
def suggest_topics():
    """Get topic suggestions for blog content."""
    try:
        topics = content_generator.suggest_topics(10)
        return jsonify({
            'success': True,
            'topics': topics
        })
        
    except Exception as e:
        logger.error(f"Topics endpoint error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to generate topics'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5004))
    logger.info(f"Starting Content Generator on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
