#!/usr/bin/env python3
"""
Painting Gallery Generator for Stephen Sironi Portfolio
This script reads painting data from a CSV and generates HTML gallery cards.
Designed to be used with Claude Code for efficient bulk import.
"""

import csv
import os
from pathlib import Path

# Configuration
CSV_FILE = "paintings-data.csv"
HTML_FILE = "index.html"
BACKUP_FILE = "index.html.backup"

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
                'description': row['description'].strip()
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

def generate_gallery_html(paintings):
    """Generate HTML for all painting gallery cards."""
    html_parts = []
    
    for painting in paintings:
        card_html = f'''
            <div class="painting-card">
                <div class="painting-image" style="background-image: url('images/paintings/{painting['location']}/{painting['filename']}'); background-size: cover; background-position: center;"></div>
                <div class="painting-info">
                    <h3>{painting['title']}</h3>
                    <p class="medium">{painting['medium']}</p>
                    <p class="description">{painting['description']}</p>
                    <div class="price-tag">From ${painting['price']}</div>
                    <button class="order-button" onclick="openOrderModal('{painting['title']}', {painting['price']})">ORDER PRINT</button>
                </div>
            </div>'''
        
        html_parts.append(card_html)
    
    return '\n'.join(html_parts)

def update_html_file(html_file, gallery_html):
    """Update the index.html file with new gallery content."""
    
    # Create backup
    if os.path.exists(html_file):
        import shutil
        shutil.copy(html_file, BACKUP_FILE)
        print(f"✅ Created backup: {BACKUP_FILE}")
    
    # Read current HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the gallery grid section
    start_marker = '<div class="gallery-grid">'
    end_marker = '</div>\n    </section>\n\n    <!-- Contact Section -->'
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print("❌ Error: Could not find gallery section in HTML!")
        print("Make sure index.html has the correct structure.")
        return False
    
    # Replace gallery content
    new_content = (
        content[:start_idx + len(start_marker)] +
        '\n' + gallery_html + '\n        ' +
        content[end_idx:]
    )
    
    # Write updated HTML
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated {html_file} with {gallery_html.count('painting-card')} paintings!")

    return True

def add_description_css():
    """Add CSS for description paragraph if not already present."""
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if description CSS exists
    if '.painting-info .description' in content:
        return  # Already exists
    
    # Find where to insert (after .painting-info .medium)
    insert_after = '''.painting-info .medium {
            font-size: 0.9rem;
            color: #888;
            margin-bottom: 1.5rem;
            font-style: italic;
        }'''
    
    description_css = '''

        .painting-info .description {
            font-size: 0.95rem;
            color: #666;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }'''
    
    new_content = content.replace(insert_after, insert_after + description_css)
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Added description CSS styling")

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("  Stephen Sironi Gallery Generator")
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
    
    # Step 3: Generate HTML
    print("\n--- Generating Gallery HTML ---")
    gallery_html = generate_gallery_html(paintings)
    
    # Step 4: Update HTML file
    print("\n--- Updating index.html ---")
    if not update_html_file(HTML_FILE, gallery_html):
        return
    
    # Step 5: Add description CSS
    add_description_css()
    
    # Step 6: Summary
    print("\n" + "="*60)
    print("✅ SUCCESS! Gallery updated with all paintings.")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   • Total paintings: {len(paintings)}")
    print(f"   • Boston: {sum(1 for p in paintings if p['location'] == 'boston')}")
    print(f"   • Delaware: {sum(1 for p in paintings if p['location'] == 'delaware')}")
    print(f"   • Misc: {sum(1 for p in paintings if p['location'] == 'misc')}")
    print(f"\n📁 Files:")
    print(f"   • Updated: {HTML_FILE}")
    print(f"   • Backup: {BACKUP_FILE}")
    print(f"\n🚀 Next Steps:")
    print(f"   1. Open index.html in your browser to preview")
    print(f"   2. If it looks good:")
    print(f"      git add .")
    print(f"      git commit -m 'Add all paintings to gallery'")
    print(f"      git push")
    print(f"   3. If you need to make changes:")
    print(f"      • Edit paintings-data.csv")
    print(f"      • Run this script again")
    print(f"      • (Your backup is safe at {BACKUP_FILE})")
    print("\n")

if __name__ == "__main__":
    main()
