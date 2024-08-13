from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import json

app = Flask(__name__)
es = Elasticsearch(['http://localhost:9200'])  # Elasticsearch 연결 정보를 적절히 수정하세요

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        try:
            # 입력된 쿼리가 비어있지 않은지 확인
            if not query.strip():
                raise ValueError("쿼리가 비어있습니다.")
            
            # 입력된 쿼리를 JSON으로 파싱
            query_json = json.loads(query)
            
            result = es.search(index='woori_card', body=query_json)
            return render_template('result.html', result=result['hits']['hits'])
        except json.JSONDecodeError:
            return render_template('result.html', error="입력된 쿼리가 올바른 JSON 형식이 아닙니다.")
        except ValueError as ve:
            return render_template('result.html', error=str(ve))
        except Exception as e:
            return render_template('result.html', error=str(e))
    else:
        # 기본 검색 쿼리
        query = {
            "query": {
                "match_all": {}
            }
        }
        result = es.search(index='woori_card', body=query)
        return render_template('index.html', result=result['hits']['hits'])

if __name__ == '__main__':
    app.run(debug=True)