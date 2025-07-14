import praw
import os
from dotenv import load_dotenv
from tqdm import tqdm
import textwrap
from datetime import datetime
from openai import OpenAI


load_dotenv()


reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="UserPersonaScraper/1.0"
)

client= OpenAI(api_key=os.getenv("REPLACE WITH YOUR OPENAI KEY"))


def scrape_reddit_user(username):
    """Scrape user comments and posts from Reddit"""
    user = reddit.redditor(username)

    print(f"Scraping data for user: {username}")


    comments = []
    for comment in tqdm(user.comments.new(limit=100), desc="Fetching comments"):
        comments.append({
            "id": comment.id,
            "body": comment.body,
            "subreddit": str(comment.subreddit),
            "created_utc": comment.created_utc,
            "score": comment.score
        })

    # Get recent submissions
    submissions = []
    for submission in tqdm(user.submissions.new(limit=50), desc="Fetching posts"):
        submissions.append({
            "id": submission.id,
            "title": submission.title,
            "body": submission.selftext,
            "subreddit": str(submission.subreddit),
            "created_utc": submission.created_utc,
            "score": submission.score,
            "url": submission.url
        })

    return {
        "username": username,
        "comments": comments,
        "submissions": submissions
    }


def generate_persona(user_data):
    """Generate user persona using LLM"""

    context = f"Reddit user {user_data['username']} activity summary:\n\n"


    context += "Recent Comments:\n"
    for comment in user_data['comments'][:20]:  # Use first 20 comments for context
        context += f"- In r/{comment['subreddit']}: {comment['body'][:200]}\n"


    context += "\nRecent Posts:\n"
    for post in user_data['submissions'][:10]:  # Use first 10 posts for context
        context += f"- In r/{post['subreddit']}: {post['title']}"
        if post['body']:
            context += f" - {post['body'][:200]}"
        context += "\n"


    prompt = textwrap.dedent(f"""
    Analyze the following Reddit user's activity and create a detailed user persona.
    For each characteristic you identify, include citations from specific comments or posts.

    Follow this persona template:

    [Reddit Username]
    [Basic Demographics] (inferred from language, topics, etc.)
    [Key Interests] (based on subreddits participated in and content)
    [Communication Style]
    [Values/Beliefs] (inferred from comments/posts)
    [Behavioral Patterns]
    [Potential Profession/Education Level]

    Citations should be in the format: [comment_id] or [post_id]

    User Activity:
    {context}
    """)


    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "You are a skilled analyst that creates detailed user personas from online activity."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )

    return response.choices[0].message.content


def save_persona(username, persona_text, user_data):
    """Save persona to text file with metadata"""
    filename = f"persona_{username}.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Reddit User Persona Analysis\n")
        f.write(f"Generated on: {timestamp}\n")
        f.write(f"Profile: https://www.reddit.com/user/{username}/\n\n")
        f.write(persona_text)
        f.write("\n\n=== Raw Data References ===\n")


        f.write("\nComments Analyzed:\n")
        for comment in user_data['comments'][:20]:
            f.write(f"[{comment['id']}] r/{comment['subreddit']}: {comment['body'][:100]}...\n")

        f.write("\nPosts Analyzed:\n")
        for post in user_data['submissions'][:10]:
            f.write(f"[{post['id']}] r/{post['subreddit']}: {post['title']} - {post['body'][:100]}...\n")

    print(f"Persona saved to {filename}")


def main():
    print("Reddit User Persona Generator (Batch Mode)")
    print("Paste multiple Reddit profile URLs (one per line or separated by commas/spaces)")
    print("Press Enter twice when done\n")


    urls = []
    while True:
        try:
            line = input().strip()
            if not line:
                if urls:  # If we have URLs and get empty line, finish
                    break
                continue  # Skip initial empty lines


            for part in line.replace(",", " ").split():
                if "reddit.com/user/" in part:
                    urls.append(part)
                elif part.startswith("user/"):
                    urls.append(f"https://www.reddit.com/{part}")
                elif "/user/" in part:  # Handle partial URLs
                    urls.append(f"https://www.reddit.com/user/{part.split('/user/')[-1]}")

        except (KeyboardInterrupt, EOFError):
            print("\nInput cancelled.")
            return []

    if not urls:
        print("No URLs provided. Exiting.")
        return

    print(f"\nProcessing {len(urls)} profiles...")

    for url in urls:
        try:
            username = url.strip("/").split("/")[-1]
            user_data = scrape_reddit_user(username)
            print(f"\nGenerating persona for {username}...")
            persona = generate_persona(user_data)
            save_persona(username, persona, user_data)
        except Exception as e:
            print(f"\nError processing {url}: {str(e)}")
            continue

if __name__ == "__main__":
    main()