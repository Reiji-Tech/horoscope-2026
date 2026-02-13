#!/usr/bin/env python3
"""
SEO自動最適化スクリプト
メタタグ、構造化データ、OGP画像などを自動追加
"""

import os
import json
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

# サイト基本情報
SITE_URL = "https://reiji-tech.github.io/horoscope-2026"
SITE_NAME = "2026年占い - 12星座別完全ガイド"
SITE_DESCRIPTION = "2026年の運勢を12星座別に完全解説。恋愛、仕事、金運、健康運を詳しく占います。"

# 星座情報
ZODIAC_INFO = {
    'aries': {'ja': '牡羊座', 'en': 'Aries', 'date': '3/21-4/19', 'emoji': '♈'},
    'taurus': {'ja': '牡牛座', 'en': 'Taurus', 'date': '4/20-5/20', 'emoji': '♉'},
    'gemini': {'ja': '双子座', 'en': 'Gemini', 'date': '5/21-6/21', 'emoji': '♊'},
    'cancer': {'ja': '蟹座', 'en': 'Cancer', 'date': '6/22-7/22', 'emoji': '♋'},
    'leo': {'ja': '獅子座', 'en': 'Leo', 'date': '7/23-8/22', 'emoji': '♌'},
    'virgo': {'ja': '乙女座', 'en': 'Virgo', 'date': '8/23-9/22', 'emoji': '♍'},
    'libra': {'ja': '天秤座', 'en': 'Libra', 'date': '9/23-10/23', 'emoji': '♎'},
    'scorpio': {'ja': '蠍座', 'en': 'Scorpio', 'date': '10/24-11/22', 'emoji': '♏'},
    'sagittarius': {'ja': '射手座', 'en': 'Sagittarius', 'date': '11/23-12/21', 'emoji': '♐'},
    'capricorn': {'ja': '山羊座', 'en': 'Capricorn', 'date': '12/22-1/19', 'emoji': '♑'},
    'aquarius': {'ja': '水瓶座', 'en': 'Aquarius', 'date': '1/20-2/18', 'emoji': '♒'},
    'pisces': {'ja': '魚座', 'en': 'Pisces', 'date': '2/19-3/20', 'emoji': '♓'},
}

def create_structured_data(page_type, zodiac_sign=None):
    """構造化データ（JSON-LD）を生成"""
    
    if page_type == 'homepage':
        return {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": SITE_NAME,
            "url": SITE_URL,
            "description": SITE_DESCRIPTION,
            "publisher": {
                "@type": "Organization",
                "name": "Horoscope 2026"
            }
        }
    
    elif page_type == 'article' and zodiac_sign:
        info = ZODIAC_INFO.get(zodiac_sign, {})
        return {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": f"【2026年運勢】{info.get('ja', '')}の完全ガイド",
            "description": f"{info.get('ja', '')}({info.get('date', '')})の2026年運勢。恋愛運、仕事運、金運、健康運を詳しく解説。",
            "author": {
                "@type": "Organization",
                "name": "Horoscope 2026"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Horoscope 2026"
            },
            "datePublished": "2026-01-01",
            "dateModified": datetime.now().strftime("%Y-%m-%d"),
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"{SITE_URL}/{zodiac_sign}.html"
            }
        }
    
    return None

def optimize_html_file(html_path):
    """HTMLファイルのSEO最適化"""
    print(f"SEO最適化中: {html_path}")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    head = soup.find('head')
    
    if not head:
        print(f"  ⚠️  <head>タグが見つかりません")
        return False
    
    # ファイル名から星座を特定
    filename = Path(html_path).stem
    zodiac_sign = filename if filename in ZODIAC_INFO else None
    is_homepage = filename in ['index', 'home']
    
    # 1. メタタグの追加・更新
    if zodiac_sign:
        info = ZODIAC_INFO[zodiac_sign]
        title = f"【2026年運勢】{info['ja']}の完全ガイド | 恋愛・仕事・金運"
        description = f"{info['ja']}({info['date']})の2026年運勢を詳しく解説。恋愛運、仕事運、金運、健康運を占います。ラッキーカラーや開運アドバイスも。"
        keywords = f"{info['ja']},2026年運勢,{info['en']},占い,ホロスコープ,恋愛運,仕事運,金運"
    else:
        title = SITE_NAME
        description = SITE_DESCRIPTION
        keywords = "占い,2026年,運勢,ホロスコープ,12星座,恋愛運,仕事運,金運"
    
    # タイトル
    if not soup.find('title'):
        title_tag = soup.new_tag('title')
        title_tag.string = title
        head.append(title_tag)
        print(f"  ✅ タイトル追加")
    
    # メタディスクリプション
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if not meta_desc:
        meta_desc = soup.new_tag('meta', attrs={'name': 'description', 'content': description})
        head.append(meta_desc)
        print(f"  ✅ メタディスクリプション追加")
    
    # キーワード
    if not soup.find('meta', attrs={'name': 'keywords'}):
        meta_keywords = soup.new_tag('meta', attrs={'name': 'keywords', 'content': keywords})
        head.append(meta_keywords)
        print(f"  ✅ キーワード追加")
    
    # viewport
    if not soup.find('meta', attrs={'name': 'viewport'}):
        meta_viewport = soup.new_tag('meta', attrs={
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0'
        })
        head.append(meta_viewport)
        print(f"  ✅ Viewport追加")
    
    # 2. OGP（Open Graph Protocol）タグ
    og_tags = {
        'og:title': title,
        'og:description': description,
        'og:type': 'article' if zodiac_sign else 'website',
        'og:url': f"{SITE_URL}/{filename}.html",
        'og:site_name': SITE_NAME,
        'og:locale': 'ja_JP',
    }
    
    for property_name, content in og_tags.items():
        if not soup.find('meta', attrs={'property': property_name}):
            og_tag = soup.new_tag('meta', attrs={'property': property_name, 'content': content})
            head.append(og_tag)
    
    print(f"  ✅ OGPタグ追加")
    
    # 3. Twitter Card
    twitter_tags = {
        'twitter:card': 'summary_large_image',
        'twitter:title': title,
        'twitter:description': description,
    }
    
    for name, content in twitter_tags.items():
        if not soup.find('meta', attrs={'name': name}):
            twitter_tag = soup.new_tag('meta', attrs={'name': name, 'content': content})
            head.append(twitter_tag)
    
    print(f"  ✅ Twitterカード追加")
    
    # 4. 構造化データ（JSON-LD）
    page_type = 'article' if zodiac_sign else 'homepage'
    structured_data = create_structured_data(page_type, zodiac_sign)
    
    if structured_data and not soup.find('script', attrs={'type': 'application/ld+json'}):
        script_tag = soup.new_tag('script', type='application/ld+json')
        script_tag.string = json.dumps(structured_data, ensure_ascii=False, indent=2)
        head.append(script_tag)
        print(f"  ✅ 構造化データ追加")
    
    # 5. カノニカルURL
    if not soup.find('link', attrs={'rel': 'canonical'}):
        canonical = soup.new_tag('link', attrs={
            'rel': 'canonical',
            'href': f"{SITE_URL}/{filename}.html"
        })
        head.append(canonical)
        print(f"  ✅ カノニカルURL追加")
    
    # 6. 言語指定
    html_tag = soup.find('html')
    if html_tag and not html_tag.get('lang'):
        html_tag['lang'] = 'ja'
        print(f"  ✅ 言語属性追加")
    
    # 7. 文字エンコーディング
    if not soup.find('meta', attrs={'charset': True}):
        charset_meta = soup.new_tag('meta', attrs={'charset': 'UTF-8'})
        head.insert(0, charset_meta)
        print(f"  ✅ 文字エンコーディング追加")
    
    # ファイルに書き込み
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    
    print(f"  ✨ SEO最適化完了\n")
    return True

def main():
    """メイン処理"""
    print("=" * 60)
    print("🔍 SEO自動最適化システム")
    print("=" * 60)
    print()
    
    # HTMLファイルを検索
    html_files = list(Path('.').rglob('*.html'))
    html_files = [
        f for f in html_files 
        if not any(exclude in str(f) for exclude in ['node_modules', '.git', 'vendor'])
    ]
    
    print(f"対象HTMLファイル: {len(html_files)}個\n")
    
    for html_file in html_files:
        optimize_html_file(html_file)
    
    print("=" * 60)
    print("✅ SEO最適化完了")
    print("=" * 60)

if __name__ == '__main__':
    main()
