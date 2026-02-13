#!/usr/bin/env python3
"""
sitemap.xml自動生成スクリプト
Google検索エンジン用のサイトマップを自動生成
"""

from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

SITE_URL = "https://reiji-tech.github.io/horoscope-2026"

# 優先度設定
PRIORITY_MAP = {
    'index.html': '1.0',
    'home.html': '1.0',
    'aries.html': '0.9',
    'taurus.html': '0.9',
    'gemini.html': '0.9',
    'cancer.html': '0.9',
    'leo.html': '0.9',
    'virgo.html': '0.9',
    'libra.html': '0.9',
    'scorpio.html': '0.9',
    'sagittarius.html': '0.9',
    'capricorn.html': '0.9',
    'aquarius.html': '0.9',
    'pisces.html': '0.9',
}

# 更新頻度設定
CHANGEFREQ_MAP = {
    'index.html': 'daily',
    'home.html': 'daily',
}

def prettify_xml(elem):
    """XMLを整形"""
    rough_string = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def generate_sitemap():
    """sitemap.xmlを生成"""
    print("=" * 60)
    print("🗺️  サイトマップ生成")
    print("=" * 60)
    print()
    
    # HTMLファイルを検索
    html_files = list(Path('.').rglob('*.html'))
    html_files = [
        f for f in html_files 
        if not any(exclude in str(f) for exclude in ['node_modules', '.git', 'vendor', 'lighthouse-reports'])
    ]
    
    print(f"対象HTMLファイル: {len(html_files)}個\n")
    
    # XML作成
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    for html_file in sorted(html_files):
        filename = html_file.name
        relative_path = str(html_file).replace('\\', '/')
        
        # URL作成
        if filename == 'index.html' and str(html_file.parent) == '.':
            url_path = SITE_URL + '/'
        else:
            url_path = f"{SITE_URL}/{relative_path}"
        
        # <url>要素作成
        url_elem = ET.SubElement(urlset, 'url')
        
        # <loc>
        loc = ET.SubElement(url_elem, 'loc')
        loc.text = url_path
        
        # <lastmod>
        lastmod = ET.SubElement(url_elem, 'lastmod')
        lastmod.text = current_date
        
        # <changefreq>
        changefreq = ET.SubElement(url_elem, 'changefreq')
        changefreq.text = CHANGEFREQ_MAP.get(filename, 'weekly')
        
        # <priority>
        priority = ET.SubElement(url_elem, 'priority')
        priority.text = PRIORITY_MAP.get(filename, '0.8')
        
        print(f"  ✅ 追加: {url_path}")
    
    # XML整形して保存
    xml_content = prettify_xml(urlset)
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print()
    print("=" * 60)
    print("✅ sitemap.xml 生成完了")
    print(f"📍 場所: ./sitemap.xml")
    print(f"📊 URL数: {len(html_files)}")
    print("=" * 60)

if __name__ == '__main__':
    generate_sitemap()
