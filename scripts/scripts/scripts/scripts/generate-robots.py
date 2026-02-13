#!/usr/bin/env python3
"""
robots.txt自動生成スクリプト
検索エンジンクローラー向けの設定ファイルを生成
"""

SITE_URL = "https://reiji-tech.github.io/horoscope-2026"

def generate_robots():
    """robots.txtを生成"""
    print("=" * 60)
    print("🤖 robots.txt生成")
    print("=" * 60)
    print()
    
    robots_content = f"""# robots.txt for {SITE_URL}
# 2026年占いサイト

# Google検索エンジン
User-agent: Googlebot
Allow: /
Crawl-delay: 0

# Bingbot
User-agent: Bingbot
Allow: /
Crawl-delay: 1

# すべての検索エンジン
User-agent: *
Allow: /

# クロール禁止ディレクトリ
Disallow: /assets/
Disallow: /scripts/
Disallow: /.git/
Disallow: /node_modules/

# サイトマップの場所
Sitemap: {SITE_URL}/sitemap.xml

# AdSense広告クローラー
User-agent: Mediapartners-Google
Allow: /

# 画像検索
User-agent: Googlebot-Image
Allow: /images/

# モバイルbot
User-agent: Googlebot-Mobile
Allow: /
"""
    
    with open('robots.txt', 'w', encoding='utf-8') as f:
        f.write(robots_content)
    
    print("  ✅ robots.txt 生成完了")
    print(f"  📍 場所: ./robots.txt")
    print()
    print("=" * 60)
    print("✅ 完了")
    print("=" * 60)

if __name__ == '__main__':
    generate_robots()
```

---

### ⑤ もう一つ重要なファイル: `requirements.txt`

**ファイル名**: `requirements.txt`（ルートディレクトリ、scriptsフォルダではない）
```
beautifulsoup4==4.12.2
lxml==4.9.3
requests==2.31.0
```

---

## ✅ 完了後の確認

すべてのファイルを作成したら、以下のURLで確認:
```
https://github.com/reiji-tech/horoscope-2026/tree/main/scripts
