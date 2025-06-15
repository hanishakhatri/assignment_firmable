# setting.py

INDEX_NAME = 'CC-MAIN-2025-13'
INDEX_SERVER = 'http://index.commoncrawl.org/'
CC_DATA_PREFIX = 'https://data.commoncrawl.org/'
USER_AGENT = 'cc-australia-extractor/1.0 (hanishakhatri777@gmail.com)'

INDUSTRY_KEYWORDS_ENHANCED = [
    ('healthcare', {
        'content': ['clinic', 'hospital', 'dental', 'health', 'medical', 'wellness', 'therapy', 'physio', 'nursing', 'doctor', 'medicine', 'healthcare', 'patient', 'treatment'],
        'company_name': ['medical', 'health', 'dental', 'clinic', 'hospital', 'physio', 'therapy', 'wellness', 'care', 'surgery', 'pharmaceutical', 'pharma', 'med', 'healthcare']
    }),
    ('finance', {
        'content': ['bank', 'insurance', 'finance', 'investment', 'accounting', 'tax', 'superannuation', 'loan', 'mortgage', 'financial', 'money', 'credit', 'wealth'],
        'company_name': ['bank', 'financial', 'finance', 'investment', 'insurance', 'accounting', 'tax', 'super', 'loan', 'mortgage', 'capital', 'wealth', 'credit', 'fund']
    }),
    ('education', {
        'content': ['school', 'university', 'training', 'education', 'course', 'elearning', 'academy', 'tutoring', 'college', 'learning', 'student', 'teach'],
        'company_name': ['school', 'university', 'college', 'academy', 'education', 'learning', 'training', 'institute', 'tutor', 'teach', 'study', 'campus']
    }),
    ('technology', {
        'content': ['software', 'technology', 'it', 'web design', 'digital', 'ecommerce', 'hosting', 'cloud', 'developer', 'data', 'tech', 'computer', 'app'],
        'company_name': ['tech', 'software', 'digital', 'it', 'web', 'app', 'cloud', 'data', 'cyber', 'online', 'internet', 'systems', 'solutions', 'dev']
    }),
    ('legal', {
        'content': ['legal', 'law', 'estate', 'conveyancing', 'lawyer', 'solicitor', 'court', 'litigation', 'attorney', 'legal services'],
        'company_name': ['legal', 'law', 'lawyer', 'solicitor', 'attorney', 'court', 'justice', 'litigation', 'advocate', 'counsel', 'barrister']
    }),
    ('consulting', {
        'content': ['consulting', 'strategy', 'advisory', 'services', 'solutions', 'management', 'business consulting', 'consultant', 'advice'],
        'company_name': ['consulting', 'advisory', 'solutions', 'strategy', 'management', 'services', 'group', 'partners', 'associates', 'advisors']
    }),
    ('retail', {
        'content': ['shop', 'store', 'buy', 'product', 'sale', 'retail', 'cart', 'ecommerce', 'clothing', 'furniture', 'shopping', 'merchandise'],
        'company_name': ['store', 'shop', 'retail', 'boutique', 'mart', 'emporium', 'warehouse', 'outlet', 'market', 'trading', 'supplies']
    }),
    ('arts_entertainment', {
        'content': ['museum', 'art', 'gallery', 'performance', 'exhibit', 'music', 'concert', 'drama', 'theatre', 'entertainment', 'cultural', 'creative'],
        'company_name': ['art', 'gallery', 'museum', 'theatre', 'studio', 'creative', 'design', 'entertainment', 'media', 'cultural', 'arts']
    }),
    ('non_profit', {
        'content': ['charity', 'fundraising', 'donation', 'disaster relief', 'ngo', 'non-profit', 'volunteer', 'aid', 'foundation', 'community'],
        'company_name': ['foundation', 'charity', 'fund', 'association', 'society', 'community', 'trust', 'relief', 'aid', 'support']
    }),
    ('construction', {
        'content': ['construction', 'building', 'contractor', 'renovation', 'plumbing', 'electrical', 'carpentry', 'roofing', 'concrete', 'architecture'],
        'company_name': ['construction', 'building', 'builders', 'contractor', 'plumbing', 'electrical', 'roofing', 'concrete', 'homes', 'projects']
    }),
    ('automotive', {
        'content': ['car', 'auto', 'vehicle', 'motor', 'garage', 'mechanic', 'repair', 'parts', 'dealership', 'automotive'],
        'company_name': ['auto', 'motor', 'car', 'vehicle', 'garage', 'automotive', 'parts', 'service', 'repair', 'dealership']
    }),
    ('food_beverage', {
        'content': ['restaurant', 'cafe', 'food', 'catering', 'bar', 'pub', 'dining', 'kitchen', 'chef', 'menu', 'coffee'],
        'company_name': ['cafe', 'restaurant', 'bar', 'pub', 'kitchen', 'catering', 'food', 'dining', 'grill', 'bistro', 'coffee']
    }),
    ('real_estate', {
        'content': ['real estate', 'property', 'realtor', 'agent', 'rental', 'lease', 'apartment', 'house', 'commercial property'],
        'company_name': ['real estate', 'property', 'realty', 'homes', 'land', 'estates', 'rentals', 'letting', 'housing']
    }),
    ('transportation', {
        'content': ['transport', 'shipping', 'logistics', 'delivery', 'freight', 'courier', 'moving', 'taxi', 'bus', 'truck'],
        'company_name': ['transport', 'logistics', 'shipping', 'delivery', 'freight', 'courier', 'moving', 'express', 'cargo']
    }),
    ('manufacturing', {
        'content': ['manufacturing', 'factory', 'production', 'industrial', 'machinery', 'equipment', 'assembly', 'fabrication'],
        'company_name': ['manufacturing', 'industries', 'factory', 'production', 'industrial', 'machinery', 'equipment', 'fabrication', 'works']
    })
]

DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'assignment_firmable',
    'user': 'postgres',
    'password': 'password',  # Replace with your actual password
}