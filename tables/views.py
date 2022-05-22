from django.shortcuts import render
import pandas as pd
import json
import os

csv_filename = os.path.join(os.path.dirname(__file__), 'where2.xlsx')
category_filter = [
    {
        'name': 'play',
        'label': '놀이',
    },
    {
        'name': 'nature',
        'label': '자연',
    },
    {
        'name': 'history',
        'label': '역사',
    },
    {
        'name': 'art',
        'label': '예술',
    },
    {
        'name': 'curriculum',
        'label': '교과연계',
    },
    {
        'name': 'science',
        'label': '과학',
    },
    {
        'name': 'course',
        'label': '진로',
    },
] 

def index(request):
    df = pd.read_excel(csv_filename)
    json_records = df.reset_index().to_json(orient ='records')
    data = []

    # category 체크 여부 확인
    category_name_checked = []
    category_label_checked = []
    for category in category_filter:
        if request.GET.get(category['name']) == 'on':
            category_name_checked.append(category['name'])
            category_label_checked.append(category['label'])

    # 데이터 필터링
    data = json.loads(json_records)
    if category_label_checked:
        data = list(filter(lambda x: x['category'] in category_label_checked, data))

    context = {
        'd': data,
        'category_filter': category_filter,
        'category_filter_checked': category_name_checked,
    }

    return render(request, 'table.html', context)
