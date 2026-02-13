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
    
    return Non
