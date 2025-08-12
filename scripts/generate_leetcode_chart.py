#!/usr/bin/env python3
import sys, requests
import matplotlib.pyplot as plt

def fetch_leetcode_stats(user):
    query = """
    query userProfile($username: String!) {
      matchedUser(username: $username) {
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """
    res = requests.post("https://leetcode.com/graphql",
                        json={'query': query, 'variables': {'username': user}},
                        headers={'Content-Type':'application/json'})
    res.raise_for_status()
    return res.json()['data']['matchedUser']['submitStats']['acSubmissionNum']

def draw(counts, out):
    labels = ['Easy', 'Medium', 'Hard']
    vals = [counts.get(lbl, 0) for lbl in labels]
    plt.figure(figsize=(6,3.5))
    plt.bar(labels, vals, color=['#4CAF50', '#FFC107', '#F44336'])
    plt.title("LeetCode Solved — Difficulty Breakdown")
    plt.ylabel("Problems solved")
    plt.tight_layout()
    plt.savefig(out, dpi=150)

if __name__ == "__main__":
    user = sys.argv[1]
    out = sys.argv[2]
    ac = fetch_leetcode_stats(user)
    counts = {item['difficulty'].capitalize(): item['count'] for item in ac}
    draw(counts, out)
    print("Chart saved:", out)
