#!/usr/bin/env python3
"""
Painting Gallery Generator for Stephen Sironi Portfolio - V2
Generates Featured Works section + Tabbed Gallery (Boston, MA | Delaware, OH | Other Pieces)
"""

import csv
import os
from pathlib import Path

# Configuration
CSV_FILE = "paintings-data.csv"
HTML_FILE = "index.html"
BACKUP_FILE = "index.html.backup"

# Category display names
CATEGORY_NAMES = {
    'boston': 'Boston, MA',
    'delaware': 'Delaware, OH',
    'misc': 'Other Pieces'
}

def read_paintings_data(csv_path):
    """Read painting data from CSV file."""
    paintings = []
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: {csv_path} not found!")
        print("Please create the CSV file with your painting data first.")
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
    """Validate that all required data is present and image files exist."""
    valid = True
    
    for i, painting in enumerate(paintings, 1):
        # Check required fields
        required_fields = ['title', 'location', 'filename', 'medium', 'price', 'description']
        for field in required_fields:
            if not painting.get(field):
                print(f"❌ Row {i}: Missing {field}")
                valid = False
        
        # Validate location
        if painting['location'] not in ['boston', 'delaware', 'misc']:
            print(f"❌ Row {i}: Invalid location '{painting['location']}' (must be boston, delaware, or misc)")
            valid = False
        
        # Check if image file exists
        image_path = f"images/paintings/{painting['location']}/{painting['filename']}"
        if not os.path.exists(image_path):
            print(f"⚠️  Row {i}: Image not found: {image_path}")
            print(f"   Make sure the file exists and the filename in CSV matches exactly!")
            valid = False
    
    if valid:
        print("✅ All paintings data validated successfully!")
    
    return valid

def generate_painting_card(painting, card_class="painting-card"):
    """Generate HTML for a single painting card."""
    return f'''
            <div class="{card_class}">
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
    """Generate HTML for Featured Works section."""
    featured = [p for p in paintings if p['featured']]
    
    if not featured:
        print("⚠️  No featured paintings found. Skipping featured section.")
        return ""
    
    cards_html = '\n'.join([generate_painting_card(p, "painting-card featured-card") for p in featured])
    
    section_html = f'''
    <!-- Featured Works Section -->
    <section class="featured-gallery">
        <h2>Featured Works</h2>
        <div class="featured-grid">
{cards_html}
        </div>
    </section>
'''
    
    print(f"✅ Generated Featured Works section with {len(featured)} paintings")
    return section_html

def generate_tabbed_gallery(paintings):
    """Generate HTML for tabbed gallery organized by location."""
    
    # Group paintings by location
    by_location = {
        'boston': [p for p in paintings if p['location'] == 'boston'],
        'delaware': [p for p in paintings if p['location'] == 'delaware'],
        'misc': [p for p in paintings if p['location'] == 'misc']
    }
    
    # Generate tab content for each category
    tab_contents = []
    for loc_key in ['boston', 'delaware', 'misc']:
        paintings_list = by_location[loc_key]
        if not paintings_list:
            continue
            
        cards_html = '\n'.join([generate_painting_card(p) for p in paintings_list])
        
        tab_contents.append(f'''
            <div class="tab-content" id="{loc_key}-tab" style="display: none;">
                <div class="gallery-grid">
{cards_html}
                </div>
            </div>''')
    
    # Combine into full gallery section
    gallery_html = f'''
    <!-- Tabbed Gallery Section -->
    <section class="gallery" id="gallery">
        <h2>Browse Collection</h2>
        
        <div class="tab-navigation">
            <button class="tab-button active" onclick="showTab('boston')">Boston, MA</button>
            <button class="tab-button" onclick="showTab('delaware')">Delaware, OH</button>
            <button class="tab-button" onclick="showTab('misc')">Other Pieces</button>
        </div>

{''.join(tab_contents)}
    </section>
'''
    
    counts = {k: len(v) for k, v in by_location.items()}
    print(f"✅ Generated tabbed gallery: Boston ({counts['boston']}), Delaware ({counts['delaware']}), Other ({counts['misc']})")
    
    return gallery_html

def update_html_file(html_file, featured_html, gallery_html):
    """Update the index.html file with new gallery content."""
    
    # Create backup
    if os.path.exists(html_file):
        import shutil
        shutil.copy(html_file, BACKUP_FILE)
        print(f"✅ Created backup: {BACKUP_FILE}")
    
    # Read current HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the gallery section
    # Looking for featured works or tabbed gallery section
    # Try to find existing sections first
    if '    <!-- Featured Works Section -->' in content:
        start_marker = '    <!-- Featured Works Section -->'
    elif '    <!-- Tabbed Gallery Section -->' in content:
        start_marker = '    <!-- Tabbed Gallery Section -->'
    else:
        start_marker = '    <!-- Gallery Section -->'
    
    end_marker = '    <!-- Contact Section -->'
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print("❌ Error: Could not find gallery section markers in HTML!")
        return False
    
    # Build new gallery sections
    new_sections = featured_html + '\n' + gallery_html + '\n\n'
    
    # Replace content
    new_content = (
        content[:start_idx] +
        new_sections +
        content[end_idx:]
    )
    
    # Write updated HTML
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated {html_file} with featured section and tabbed gallery!")
    return True

def update_css_styles(html_file):
    """Add/update CSS for featured section and tabs."""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if our new styles already exist
    if '.featured-gallery' in content:
        print("✅ CSS styles already present")
        return
    
    # Find where to insert new CSS (after the existing gallery styles)
    insert_after = '        /* Gallery Section */'
    
    new_css = '''
        /* Featured Works Section */
        .featured-gallery {
            padding: 8rem 5%;
            background: var(--canvas-white);
        }

        .featured-gallery h2 {
            font-family: 'Cormorant Garamond', serif;
            font-size: 3.5rem;
            font-weight: 300;
            text-align: center;
            margin-bottom: 4rem;
        }

        .featured-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 3rem;
            max-width: 1400px;
            margin: 0 auto;
        }

        .featured-card {
            background: white;
            overflow: hidden;
            transition: transform 0.4s ease, box-shadow 0.4s ease;
        }

        .featured-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        }

        .featured-card .painting-image {
            height: 450px;
        }

        /* Tabbed Gallery Section */
        .tab-navigation {
            display: flex;
            justify-content: center;
            gap: 0;
            margin-bottom: 4rem;
            border-bottom: 2px solid var(--gallery-gray);
        }

        .tab-button {
            padding: 1rem 2.5rem;
            background: transparent;
            border: none;
            font-family: 'Manrope', sans-serif;
            font-size: 1rem;
            font-weight: 500;
            color: #999;
            cursor: pointer;
            transition: all 0.3s ease;
            border-bottom: 3px solid transparent;
            letter-spacing: 0.5px;
        }

        .tab-button:hover {
            color: var(--accent-rust);
        }

        .tab-button.active {
            color: var(--ink-black);
            border-bottom: 3px solid var(--accent-rust);
        }

        .tab-content {
            animation: fadeIn 0.4s ease-in;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .painting-info .description {
            font-size: 0.95rem;
            color: #666;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }

        @media (max-width: 968px) {
            .featured-grid {
                grid-template-columns: 1fr;
            }

            .tab-navigation {
                flex-wrap: wrap;
            }

            .tab-button {
                padding: 0.8rem 1.5rem;
                font-size: 0.9rem;
            }
        }

        '''
    
    # Insert the new CSS
    new_content = content.replace(insert_after, insert_after + new_css)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Added featured gallery and tab CSS styles")

def add_tab_javascript(html_file):
    """Add JavaScript for tab switching functionality."""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if function already exists
    if 'function showTab(' in content:
        print("✅ Tab JavaScript already present")
        return
    
    # Find the script section (before closing </script> tag near the end)
    script_marker = '        // Smooth scrolling for navigation'
    
    tab_js = '''
        // Tab switching functionality
        function showTab(tabName) {
            // Hide all tab contents
            const tabContents = document.querySelectorAll('.tab-content');
            tabContents.forEach(content => {
                content.style.display = 'none';
            });
            
            // Remove active class from all buttons
            const tabButtons = document.querySelectorAll('.tab-button');
            tabButtons.forEach(button => {
                button.classList.remove('active');
            });
            
            // Show selected tab
            const selectedTab = document.getElementById(tabName + '-tab');
            if (selectedTab) {
                selectedTab.style.display = 'block';
            }
            
            // Add active class to clicked button
            event.target.classList.add('active');
        }

        // Show Boston tab by default on page load
        window.addEventListener('DOMContentLoaded', () => {
            const bostonTab = document.getElementById('boston-tab');
            if (bostonTab) {
                bostonTab.style.display = 'block';
            }
        });

        '''
    
    new_content = content.replace(script_marker, tab_js + '\n        ' + script_marker)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Added tab switching JavaScript")

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("  Stephen Sironi Gallery Generator V2")
    print("  Featured Works + Tabbed Gallery")
    print("="*60 + "\n")
    
    # Step 1: Read CSV data
    paintings = read_paintings_data(CSV_FILE)
    if paintings is None:
        return
    
    if len(paintings) == 0:
        print("❌ No paintings found in CSV. Please add your painting data first.")
        return
    
    # Step 2: Validate data
    print("\n--- Validating Data ---")
    if not validate_paintings_data(paintings):
        print("\n❌ Validation failed. Please fix the issues above and try again.")
        return
    
    # Step 3: Generate HTML sections
    print("\n--- Generating Gallery HTML ---")
    featured_html = generate_featured_section(paintings)
    gallery_html = generate_tabbed_gallery(paintings)
    
    # Step 4: Update HTML file
    print("\n--- Updating index.html ---")
    if not update_html_file(HTML_FILE, featured_html, gallery_html):
        return
    
    # Step 5: Update CSS and JavaScript
    update_css_styles(HTML_FILE)
    add_tab_javascript(HTML_FILE)
    
    # Step 6: Summary
    featured_count = sum(1 for p in paintings if p['featured'])
    boston_count = sum(1 for p in paintings if p['location'] == 'boston')
    delaware_count = sum(1 for p in paintings if p['location'] == 'delaware')
    misc_count = sum(1 for p in paintings if p['location'] == 'misc')
    
    print("\n" + "="*60)
    print("✅ SUCCESS! Gallery updated with featured section and tabs.")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   • Total paintings: {len(paintings)}")
    print(f"   • Featured: {featured_count}")
    print(f"   • Boston, MA: {boston_count}")
    print(f"   • Delaware, OH: {delaware_count}")
    print(f"   • Other Pieces: {misc_count}")
    print(f"\n📁 Files:")
    print(f"   • Updated: {HTML_FILE}")
    print(f"   • Backup: {BACKUP_FILE}")
    print(f"\n🚀 Next Steps:")
    print(f"   1. Open index.html in your browser to preview")
    print(f"   2. Check the Featured Works section")
    print(f"   3. Click through the tabs (Boston, MA | Delaware, OH | Other Pieces)")
    print(f"   4. If it looks good:")
    print(f"      git add .")
    print(f"      git commit -m 'Add featured works and tabbed gallery'")
    print(f"      git push")
    print("\n")

if __name__ == "__main__":
    main()
