import os
from openai import OpenAI

# Will use OPENAI_API_KEY from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import streamlit as st
import openai
import json
from datetime import datetime

# API Key
openai.api_key = ""
    st.error("❌ Please add your OpenAI API key to app.py line 7")
    st.stop()

# Page Config
st.set_page_config(
    page_title="SEO Listing Master",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-size: 16px;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🎯 SEO Listing Master")
    st.write("Generate optimized product listings for any marketplace")
with col2:
    st.markdown("### 🚀 v1.0")

st.markdown("---")

# Marketplace Config
MARKETPLACES = {
    "Amazon": {
        "title_max": 200,
        "bullets_max": 1000,
        "desc_max": 2000,
        "color": "#FF9900"
    },
    "Walmart": {
        "title_max": 150,
        "bullets_max": 800,
        "desc_max": 1500,
        "color": "#0071CE"
    },
    "Myntra": {
        "title_max": 100,
        "bullets_max": 600,
        "desc_max": 1200,
        "color": "#EE5A6F"
    },
    "Flipkart": {
        "title_max": 120,
        "bullets_max": 700,
        "desc_max": 1300,
        "color": "#FFB800"
    }
}

# Sidebar
st.sidebar.header("📊 Settings")
marketplace = st.sidebar.selectbox(
    "Select Marketplace",
    list(MARKETPLACES.keys()),
    index=0
)
st.sidebar.markdown(f"**Title Limit:** {MARKETPLACES[marketplace]['title_max']} chars")
st.sidebar.markdown(f"**Description Limit:** {MARKETPLACES[marketplace]['desc_max']} chars")

# Main Content
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Product Information")
    
    product_name = st.text_input(
        "Product Name *",
        placeholder="e.g., Wireless Bluetooth Headphones",
        help="Enter your product name"
    )
    
    category = st.selectbox(
        "Category *",
        ["Electronics", "Fashion", "Home & Kitchen", "Sports", "Beauty", "Books", "Toys", "Other"]
    )
    
    keywords = st.text_area(
        "Keywords (one per line) *",
        height=100,
        placeholder="wireless\nBluetooth\nnoise cancelling\nbass boost",
        help="Enter keywords separated by new lines"
    )
    
    description = st.text_area(
        "Product Description",
        height=100,
        placeholder="Brief description of your product...",
        help="Optional: Existing description to enhance"
    )

with col2:
    st.subheader("⚙️ Customization")
    
    tone = st.selectbox(
        "Tone of Writing",
        ["Professional", "Casual", "Luxury", "Budget-Friendly", "Technical", "Fun & Playful"]
    )
    
    variations = st.slider(
        "Number of Variations",
        min_value=1,
        max_value=3,
        value=1,
        help="Generate multiple versions"
    )
    
    language = st.selectbox(
        "Language",
        ["English", "English (Simple)", "Hindi-English Mix"]
    )
    
    st.markdown("---")
    
    target_audience = st.multiselect(
        "Target Audience",
        ["Budget Conscious", "Premium Buyers", "Tech Enthusiasts", "General Public"],
        default=["General Public"]
    )

st.markdown("---")

# Generate Button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    generate_btn = st.button("🚀 Generate Listing", use_container_width=True, type="primary")

# Generation Logic
if generate_btn:
    if not product_name.strip() or not keywords.strip():
        st.error("❌ Please fill in Product Name and Keywords!")
        st.stop()
    
    st.markdown("---")
    st.header("📋 Generated Content")
    
    # Progress Bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Generate Title
        status_text.text("⏳ Generating Title...")
        progress_bar.progress(20)
        
        title_prompt = f"""Generate a compelling product title for {marketplace} marketplace:
Product: {product_name}
Category: {category}
Keywords: {keywords}
Tone: {tone}
Max Characters: {MARKETPLACES[marketplace]['title_max']}

Requirements:
- Include main keyword at the start
- Include 2-3 supporting keywords
- Compelling and professional
- No ALL CAPS
- ONLY the title, nothing else

Title:"""
        
        title_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": title_prompt}],
            temperature=0.7,
            max_tokens=100
        )
        title = title_response.choices[0].message.content.strip()
        
        # Generate Bullets
        status_text.text("⏳ Generating 5 Bullet Points...")
        progress_bar.progress(40)
        
        bullets_prompt = f"""Generate 5 compelling bullet points for {marketplace}:
Product: {product_name}
Category: {category}
Keywords: {keywords}
Tone: {tone}
Target Audience: {', '.join(target_audience)}
Max 1000 chars total

Format:
- Benefit/Feature with keyword
- Key feature and advantage
- Unique selling proposition
- Quality/warranty information
- Call to action

Generate ONLY the 5 bullet points without numbering:"""
        
        bullets_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": bullets_prompt}],
            temperature=0.7,
            max_tokens=500
        )
        bullets = bullets_response.choices[0].message.content.strip()
        
        # Generate Description
        status_text.text("⏳ Generating Product Description...")
        progress_bar.progress(60)
        
        desc_prompt = f"""Write a detailed product description for {marketplace}:
Product: {product_name}
Category: {category}
Keywords: {keywords}
Tone: {tone}
Existing Description: {description if description else "None"}
Target Audience: {', '.join(target_audience)}
Max Characters: {MARKETPLACES[marketplace]['desc_max']}

Structure:
- Opening hook (what problem it solves)
- Key features and benefits (3-4 paragraphs)
- Use cases
- Quality assurance/warranty

Include keywords naturally. Make it persuasive and professional:"""
        
        desc_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": desc_prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        product_desc = desc_response.choices[0].message.content.strip()
        
        # Generate Backend Keywords
        status_text.text("⏳ Generating Backend Keywords...")
        progress_bar.progress(80)
        
        backend_prompt = f"""Generate 5 sets of backend search keywords for {marketplace}:
Product: {product_name}
Primary Keywords: {keywords}

Requirements:
- 5 different keyword sets
- Each max 50 characters
- Long-tail keywords
- Search intent focused
- Comma-separated

Format as:
Set 1: keyword1, keyword2, keyword3
Set 2: keyword4, keyword5, keyword6
etc."""
        
        backend_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": backend_prompt}],
            temperature=0.7,
            max_tokens=300
        )
        backend_keywords = backend_response.choices[0].message.content.strip()
        
        progress_bar.progress(100)
        status_text.text("✅ Generation Complete!")
        
        # Results in Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🎯 Title",
            "📌 Bullets",
            "📝 Description",
            "🔑 Backend Keywords",
            "📊 Analysis"
        ])
        
        with tab1:
            st.subheader("Optimized Title")
            char_count = len(title)
            max_chars = MARKETPLACES[marketplace]['title_max']
            
            if char_count <= max_chars:
                st.success(f"✅ {char_count}/{max_chars} characters")
            else:
                st.warning(f"⚠️ {char_count}/{max_chars} characters (exceeds limit)")
            
            st.code(title, language="text")
            st.button("📋 Copy Title", key="copy_title")
        
        with tab2:
            st.subheader("5 Compelling Bullet Points")
            char_count = len(bullets)
            max_chars = MARKETPLACES[marketplace]['bullets_max']
            
            if char_count <= max_chars:
                st.success(f"✅ {char_count}/{max_chars} characters")
            else:
                st.warning(f"⚠️ {char_count}/{max_chars} characters (exceeds limit)")
            
            st.text(bullets)
            st.button("📋 Copy Bullets", key="copy_bullets")
        
        with tab3:
            st.subheader("Product Description")
            char_count = len(product_desc)
            max_chars = MARKETPLACES[marketplace]['desc_max']
            
            if char_count <= max_chars:
                st.success(f"✅ {char_count}/{max_chars} characters")
            else:
                st.warning(f"⚠️ {char_count}/{max_chars} characters (exceeds limit)")
            
            st.text(product_desc)
            st.button("📋 Copy Description", key="copy_desc")
        
        with tab4:
            st.subheader("Backend Keywords")
            st.text(backend_keywords)
            st.button("📋 Copy Keywords", key="copy_keywords")
        
        with tab5:
            st.subheader("SEO Analysis")
            
            # SEO Score Calculation
            score = 0
            metrics = []
            
            # Check keywords in content
            keywords_list = keywords.lower().split('\n')
            title_lower = title.lower()
            desc_lower = product_desc.lower()
            
            if keywords_list[0].strip() in title_lower:
                score += 20
                metrics.append("✅ Main keyword in title")
            else:
                metrics.append("❌ Main keyword not in title")
            
            keyword_in_bullets = sum(1 for kw in keywords_list if kw.strip() in bullets.lower())
            score += min(20, keyword_in_bullets * 5)
            metrics.append(f"✅ {keyword_in_bullets} keywords in bullets")
            
            if len(title) >= 50 and len(title) <= MARKETPLACES[marketplace]['title_max']:
                score += 15
                metrics.append("✅ Title length optimal")
            
            if len(bullets) >= 100:
                score += 15
                metrics.append("✅ Bullet points detailed")
            
            if len(product_desc) >= 300:
                score += 20
                metrics.append("✅ Description comprehensive")
            
            score = min(100, score)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.metric("SEO Score", f"{score}/100")
                
            with col2:
                if score >= 80:
                    st.success("Excellent SEO Optimization!")
                elif score >= 60:
                    st.info("Good SEO Optimization")
                else:
                    st.warning("Could be improved")
            
            st.subheader("Metrics")
            for metric in metrics:
                st.write(metric)
            
            # Stats
            st.subheader("Content Statistics")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Title Length", f"{len(title)} chars")
            col2.metric("Bullets Length", f"{len(bullets)} chars")
            col3.metric("Description Length", f"{len(product_desc)} chars")
            col4.metric("Keywords Used", len(keywords_list))
        
        st.markdown("---")
        st.success("✨ Listing generated successfully!")
        
        # Download Option
        col1, col2 = st.columns(2)
        with col1:
            export_data = f"""
PRODUCT: {product_name}
MARKETPLACE: {marketplace}
GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

TITLE ({len(title)} chars):
{title}

BULLET POINTS ({len(bullets)} chars):
{bullets}

DESCRIPTION ({len(product_desc)} chars):
{product_desc}

BACKEND KEYWORDS:
{backend_keywords}

SEO SCORE: {score}/100
"""
            st.download_button(
                label="⬇️ Download as Text",
                data=export_data,
                file_name=f"{product_name.replace(' ', '_')}_listing.txt",
                mime="text/plain"
            )
        
        with col2:
            st.info("💡 Tip: Copy content above and paste directly into marketplace listings!")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Make sure your OpenAI API key is valid and you have credits!")

else:
    st.info("⏳ Fill in the product information and click 'Generate Listing' to start!")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <small>SEO Listing Master | Powered by OpenAI | Made with ❤️</small>
</div>
""", unsafe_allow_html=True)
