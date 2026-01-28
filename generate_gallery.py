#!/usr/bin/env python3
"""
Painting Gallery Generator for Stephen Sironi Portfolio - V3
Generates TWO pages:
  - index.html: Featured Works only
  - gallery.html: Full collection with tabbed navigation
"""

import csv
import os
from pathlib import Path

# Configuration
CSV_FILE = "paintings-data.csv"
INDEX_FILE = "index.html"
GALLERY_FILE = "gallery.html"
INDEX_BACKUP = "index.html.backup"
GALLERY_BACKUP = "gallery.html.backup"

def read_paintings_data(csv_path):
    """Read painting data from CSV file."""
    paintings = []
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: {csv_path} not found!")
        return None
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            paintings.append({
                'title': row['title'].strip(),
                'location': row['location'].strip().lower(),
                'filename': row['filename'].strip(),
                'medium': row['medium'].strip(),
                'price': row['price'].strip(),
                'description': row['description'].strip(),
                'featured': row.get('featured', '').strip().lower() == 'yes'
            })
    
    print(f"✅ Read {len(paintings)} paintings from {csv_path}")
    return paintings

def validate_paintings_data(paintings):
    """Validate data and image files."""
    valid = True
    
    for i, painting in enumerate(paintings, 1):
        required = ['title', 'location', 'filename', 'medium', 'price', 'description']
        for field in required:
            if not painting.get(field):
                print(f"❌ Row {i}: Missing {field}")
                valid = False
        
        if painting['location'] not in ['boston', 'delaware', 'misc']:
            print(f"❌ Row {i}: Invalid location '{painting['location']}'")
            valid = False
        
        image_path = f"images/paintings/{painting['location']}/{painting['filename']}"
        if not os.path.exists(image_path):
            print(f"⚠️  Row {i}: Image not found: {image_path}")
            valid = False
    
    if valid:
        print("✅ All data validated!")
    return valid

def generate_painting_card(painting):
    """Generate HTML for a painting card."""
    return f'''            <div class="painting-card">
                <div class="painting-image" style="background-image: url('images/paintings/{painting['location']}/{painting['filename']}'); background-size: cover; background-position: center;"></div>
                <div class="painting-info">
                    <h3>{painting['title']}</h3>
                    <p class="medium">{painting['medium']}</p>
                    <p class="description">{painting['description']}</p>
                    <div class="price-tag">From ${painting['price']}</div>
                    <button class="order-button" onclick="openOrderModal('{painting['title']}', {painting['price']})">ORDER PRINT</button>
                </div>
            </div>'''

def generate_featured_section(paintings):
    """Generate featured works HTML for index.html."""
    featured = [p for p in paintings if p['featured']]
    
    if not featured:
        print("⚠️  No featured paintings. Add 'yes' to featured column for 4-6 paintings.")
        return ""
    
    cards = '\n'.join([generate_painting_card(p) for p in featured])
    
    html = f'''    <!-- Featured Works Section -->
    <section class="featured-gallery" id="featured">
        <h2>Featured Works</h2>
        <p class="section-subtitle">A curated selection of signature pieces</p>
        <div class="featured-grid">
{cards}
        </div>
        <div class="view-all-cta">
            <a href="gallery.html" class="view-all-button">VIEW COMPLETE COLLECTION</a>
        </div>
    </section>
'''
    
    print(f"✅ Generated featured section with {len(featured)} paintings")
    return html

def generate_tabbed_gallery(paintings):
    """Generate tabbed gallery HTML for gallery.html."""
    by_location = {
        'boston': [p for p in paintings if p['location'] == 'boston'],
        'delaware': [p for p in paintings if p['location'] == 'delaware'],
        'misc': [p for p in paintings if p['location'] == 'misc']
    }
    
    tabs = []
    for loc in ['boston', 'delaware', 'misc']:
        if not by_location[loc]:
            continue
        cards = '\n'.join([generate_painting_card(p) for p in by_location[loc]])
        tabs.append(f'''        <div class="tab-content" id="{loc}-tab" style="display: none;">
            <div class="gallery-grid">
{cards}
            </div>
        </div>''')
    
    html = f'''    <!-- Tabbed Gallery Section -->
    <div class="gallery-container">
        <div class="tab-navigation">
            <button class="tab-button active" onclick="showTab('boston')">Boston, MA</button>
            <button class="tab-button" onclick="showTab('delaware')">Delaware, OH</button>
            <button class="tab-button" onclick="showTab('misc')">Other Pieces</button>
        </div>

{chr(10).join(tabs)}
    </div>
'''
    
    counts = {k: len(v) for k, v in by_location.items()}
    print(f"✅ Generated tabbed gallery: Boston ({counts['boston']}), Delaware ({counts['delaware']}), Other ({counts['misc']})")
    return html

def update_index_html(featured_html, paintings):
    """Update index.html with featured works and hero backgrounds."""
    if not os.path.exists(INDEX_FILE):
        print(f"❌ {INDEX_FILE} not found!")
        return False
    
    import shutil
    shutil.copy(INDEX_FILE, INDEX_BACKUP)
    print(f"✅ Created backup: {INDEX_BACKUP}")
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update featured works section
    marker = '    <!-- Featured Works Section -->'
    end_marker = '    <!-- Contact Section -->'
    
    start = content.find(marker)
    end = content.find(end_marker)
    
    if start == -1 or end == -1:
        print("❌ Could not find markers in index.html")
        return False
    
    content = content[:start] + featured_html + '\n' + content[end:]
    
    # Update hero background paintings with actual featured paintings
    featured = [p for p in paintings if p['featured']]
    if featured:
        # Take up to 3 featured paintings for hero rotation
        hero_paintings = featured[:3]
        
        for i, painting in enumerate(hero_paintings, 1):
            old_style = f'.hero-painting-{i} {{\n            background: linear-gradient'
            new_style = f'.hero-painting-{i} {{\n            background-image: url(\'images/paintings/{painting["location"]}/{painting["filename"]}\');\n            background: linear-gradient'
            
            # Find and replace the hero painting style
            placeholder = f'.hero-painting-{i} {{'
            if placeholder in content:
                # Find the closing brace for this class
                start_pos = content.find(placeholder)
                end_pos = content.find('}', start_pos)
                old_block = content[start_pos:end_pos+1]
                new_block = f'''.hero-painting-{i} {{
            background-image: url('images/paintings/{painting["location"]}/{painting["filename"]}');
            background-size: cover;
            background-position: center;
        }}'''
                content = content.replace(old_block, new_block)
        
        print(f"✅ Updated hero with {len(hero_paintings)} featured painting backgrounds")
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {INDEX_FILE}")
    return True

def update_gallery_html(gallery_html):
    """Update gallery.html with full collection."""
    if not os.path.exists(GALLERY_FILE):
        print(f"❌ {GALLERY_FILE} not found!")
        return False
    
    import shutil
    shutil.copy(GALLERY_FILE, GALLERY_BACKUP)
    print(f"✅ Created backup: {GALLERY_BACKUP}")
    
    with open(GALLERY_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    marker = '    <!-- Tabbed Gallery Section -->'
    end_marker = '    <!-- Footer -->'
    
    start = content.find(marker)
    end = content.find(end_marker)
    
    if start == -1 or end == -1:
        print("❌ Could not find markers in gallery.html")
        return False
    
    new_content = content[:start] + gallery_html + '\n' + content[end:]
    
    with open(GALLERY_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated {GALLERY_FILE}")
    return True

def main():
    """Main execution."""
    print("\n" + "="*60)
    print("  Stephen Sironi Gallery Generator V3")
    print("  Two-Page System: Featured + Full Gallery")
    print("="*60 + "\n")
    
    # Read and validate
    paintings = read_paintings_data(CSV_FILE)
    if not paintings:
        return
    
    print("\n--- Validating Data ---")
    if not validate_paintings_data(paintings):
        print("\n❌ Fix issues and try again.")
        return
    
    # Generate HTML
    print("\n--- Generating HTML ---")
    featured_html = generate_featured_section(paintings)
    gallery_html = generate_tabbed_gallery(paintings)
    
    # Update files
    print("\n--- Updating Files ---")
    if not update_index_html(featured_html, paintings):
        return
    if not update_gallery_html(gallery_html):
        return
    
    # Summary
    featured_count = sum(1 for p in paintings if p['featured'])
    boston = sum(1 for p in paintings if p['location'] == 'boston')
    delaware = sum(1 for p in paintings if p['location'] == 'delaware')
    misc = sum(1 for p in paintings if p['location'] == 'misc')
    
    print("\n" + "="*60)
    print("✅ SUCCESS! Both pages updated.")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   • Total paintings: {len(paintings)}")
    print(f"   • Featured (index.html): {featured_count}")
    print(f"   • Boston, MA: {boston}")
    print(f"   • Delaware, OH: {delaware}")
    print(f"   • Other Pieces: {misc}")
    print(f"\n📁 Files:")
    print(f"   • {INDEX_FILE} - Featured works only")
    print(f"   • {GALLERY_FILE} - Full collection with tabs")
    print(f"\n🚀 Next Steps:")
    print(f"   1. Preview index.html (home page)")
    print(f"   2. Preview gallery.html (full gallery)")
    print(f"   3. Test navigation between pages")
    print(f"   4. If good: git add . && git commit -m 'Two-page gallery' && git push")
    print("\n")

if __name__ == "__main__":
    main()
