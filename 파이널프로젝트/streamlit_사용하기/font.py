import matplotlib.font_manager as fm

# 사용 가능한 폰트 목록 확인
for font in fm.fontManager.ttflist:
    print(font.name)