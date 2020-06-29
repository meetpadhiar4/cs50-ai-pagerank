import os
import random
import re
import sys
import copy


DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = {}
    l = len(corpus[page])
    if l != 0:
        for i in corpus:
            distribution[i] = (1 - damping_factor) / len(corpus)
        for i in corpus[page]:
            distribution[i] += damping_factor / l
    else:
        for i in corpus:
            distribution[i] = 1 / len(corpus)
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    distribution = {}
    for i in corpus:
        distribution[i] = 0
    page = random.choices(list(corpus.keys()))[0]
    distribution[page] +=  1 / n
    for i in range(1, n):
        model = transition_model(corpus, page, damping_factor)
        links = []
        probabilites = []
        for page, probability in model.items():
            links.append(page)
            probabilites.append(probability)
        page = random.choices(links, weights=probabilites)[0]
        distribution[page] += 1 / n
    return distribution


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    distribution = {}
    N = len(corpus)
    for page in corpus:
        distribution[page] = 1 / N
    change = 1
    while change >= 0.001:
        change = 0
        distribution_copy = distribution.copy()
        for page in distribution:
            links = [link for link in corpus if page in corpus[link]]
            part1 = (1 - damping_factor) / N
            part2 = []
            if len(links) != 0:
                for link in links:
                    num_links = len(corpus[link])
                    val = distribution_copy[link] / num_links
                    part2.append(val)
            summation = sum(part2)
            distribution[page] = part1 + damping_factor * summation
            new_change = abs(distribution[page] - distribution_copy[page])
            if change < new_change:
                change = new_change
    return distribution

    
if __name__ == "__main__":
    main()
