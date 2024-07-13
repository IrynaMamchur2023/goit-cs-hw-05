import requests
import re
import matplotlib.pyplot as plt
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_text_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  
    return response.text

def map_function(text):
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = defaultdict(int)
    for word in words:
        word_count[word] += 1
    return word_count

def reduce_function(mapped_results):
    total_count = defaultdict(int)
    for word_count in mapped_results:
        for word, count in word_count.items():
            total_count[word] += count
    return total_count

def visualize_top_words(word_counts, top_n=10):
    sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
    top_words = sorted_words[:top_n]

    words, counts = zip(*top_words)
    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Words by Frequency')
    plt.xticks(rotation=45)
    plt.show()

def main(url):
    text = fetch_text_from_url(url)
    chunks = [text[i:i + len(text) // 4] for i in range(0, len(text), len(text) // 4)]
    
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(map_function, chunk) for chunk in chunks]
        mapped_results = [future.result() for future in as_completed(futures)]
    
    word_counts = reduce_function(mapped_results)
    visualize_top_words(word_counts)

if __name__ == "__main__":
    url = 'https://www.britannica.com/science/psychology'      
    main(url)



