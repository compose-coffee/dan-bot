def refine_context(raw_results):
    if not raw_results:
        return ""
    
    context_str = ""
    for item in raw_results:
        url = item['url']
        body_text = item['text']
        
        raw_lines = [line.strip() for line in body_text.split('\n')]
        meaningful_lines = [l for l in raw_lines if len(l) > 20]
        unique_lines = []
        for l in meaningful_lines:
            if l not in unique_lines:
                unique_lines.append(l)
        
        context_str += f"\n[참조 : {url}]\n"
        context_str += "\n".join(unique_lines[:30]) + "\n"
        
    return context_str
