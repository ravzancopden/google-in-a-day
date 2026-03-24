import re
import state

def search_query(query):
    query_words = set(re.findall(r'\w+', query.lower()))
    results = []
    
    with state.lock:
        for page in state.index_data:
            score = 0
            title_words = re.findall(r'\w+', page['title'].lower())
            text_words = re.findall(r'\w+', page['text'].lower())
            
            for qw in query_words:
                score += title_words.count(qw) * 5
                score += text_words.count(qw)
                
            if score > 0:
                results.append({'score': score, 'data': (page['url'], page['origin'], page['depth'])})
                
    results.sort(key=lambda x: x['score'], reverse=True)
    return [r['data'] for r in results]