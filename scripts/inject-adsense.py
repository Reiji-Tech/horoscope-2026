#!/usr/bin/env python3
"""
AdSense自動挿入スクリプト
全HTMLファイルに最適な位置でAdSenseコードを挿入します
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

# 環境変数からAdSense情報を取得
ADSENSE_CLIENT_ID = os.getenv('ADSENSE_CLIENT_ID', 'ca-pub-XXXXXXXXXXXXXXXXX')
ADSENSE_SLOT_HEADER = os.getenv('ADSENSE_SLOT_HEADER', '1234567890')
ADSENSE_SLOT_SIDEBAR = os.getenv('ADSENSE_SLOT_SIDEBAR', '0987654321')
ADSENSE_SLOT_FOOTER = os.getenv('ADSENSE_SLOT_FOOTER', '1357924680')

# AdSenseコードテンプレート
ADSENSE_SCRIPT = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={client_id}"
     crossorigin="anonymous"></script>
"""

def create_adsense_unit(slot_id, format_type='auto', style='display:block'):
    """AdSense広告ユニットを生成"""
    return f"""
<!-- AdSense広告 -->
<ins class="adsbygoogle"
     style="{style}"
     data-ad-client="{ADSENSE_CLIENT_ID}"
     data-ad-slot="{slot_id}"
     data-ad-format="{format_type}"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({{}});
</script>
"""

def inject_adsense_to_html(html_path):
    """HTMLファイルにAdSenseコードを挿入"""
    print(f"処理中: {html_path}")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # すでにAdSenseが挿入されているかチェック
    if 'adsbygoogle' in content:
        print(f"  ⏭️  スキップ（既に挿入済み）: {html_path}")
        return False
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 1. <head>にAdSenseスクリプトを追加
    head = soup.find('head')
    if head:
        adsense_script = BeautifulSoup(ADSENSE_SCRIPT.format(client_id=ADSENSE_CLIENT_ID), 'html.parser')
        head.append(adsense_script)
        print(f"  ✅ ヘッダースクリプト挿入")
    
    # 2. ヘッダー広告（最初のh1の後）
    first_h1 = soup.find('h1')
    if first_h1:
        header_ad = BeautifulSoup(create_adsense_unit(ADSENSE_SLOT_HEADER), 'html.parser')
        first_h1.insert_after(header_ad)
        print(f"  ✅ ヘッダー広告挿入")
    
    # 3. サイドバー広告（サイドバーがあれば）
    sidebar = soup.find(['aside', 'div'], class_=re.compile(r'sidebar|side-bar'))
    if sidebar:
        sidebar_ad = BeautifulSoup(
            create_adsense_unit(ADSENSE_SLOT_SIDEBAR, format_type='vertical'),
            'html.parser'
        )
        sidebar.insert(0, sidebar_ad)
        print(f"  ✅ サイドバー広告挿入")
    
    # 4. フッター広告（フッターの前）
    footer = soup.find('footer')
    if footer:
        footer_ad = BeautifulSoup(create_adsense_unit(ADSENSE_SLOT_FOOTER), 'html.parser')
        footer.insert(0, footer_ad)
        print(f"  ✅ フッター広告挿入")
    else:
        # フッターがない場合はbodyの最後に追加
        body = soup.find('body')
        if body:
            footer_ad = BeautifulSoup(create_adsense_unit(ADSENSE_SLOT_FOOTER), 'html.parser')
            body.append(footer_ad)
            print(f"  ✅ フッター広告挿入（body末尾）")
    
    # 5. コンテンツ内広告（最初のh2の後 - オプション）
    first_h2 = soup.find('h2')
    if first_h2:
        content_ad = BeautifulSoup(
            create_adsense_unit(ADSENSE_SLOT_HEADER, format_type='fluid'),
            'html.parser'
        )
        first_h2.insert_after(content_ad)
        print(f"  ✅ コンテンツ内広告挿入")
    
    # ファイルに書き込み
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    
    print(f"  ✨ 完了: {html_path}\n")
    return True

def main():
    """メイン処理"""
    print("=" * 60)
    print("🚀 AdSense自動挿入システム")
    print("=" * 60)
    print(f"Client ID: {ADSENSE_CLIENT_ID[:20]}...")
    print()
    
    # HTMLファイルを検索
    html_files = list(Path('.').rglob('*.html'))
    
    # node_modules, .git などを除外
    html_files = [
        f for f in html_files 
        if not any(exclude in str(f) for exclude in ['node_modules', '.git', 'vendor'])
    ]
    
    print(f"対象HTMLファイル: {len(html_files)}個\n")
    
    updated_count = 0
    for html_file in html_files:
        if inject_adsense_to_html(html_file):
            updated_count += 1
    
    print("=" * 60)
    print(f"✅ 処理完了: {updated_count}/{len(html_files)} ファイルを更新")
    print("=" * 60)

if __name__ == '__main__':
    main()
