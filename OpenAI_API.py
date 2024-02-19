from openai import OpenAI

def create_tweet_text(key, raw, tweet_url):
    prompt_text = "aşağıdaki bilgilerle Emlak Öneri hesabım ilgi çekici bir twitter post'u hazırla, Yatırım fırsatı olarak değerlendir. 800 karakteri kesinlikle aşmasın! Emoji kullan!:\n" + raw 
    client = OpenAI(api_key = key)
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_text,
            }
        ],
        model="gpt-3.5-turbo",
    )

    """
    post_length = 275 - len(tweet_url)
    tweet_text = response.choices[0].message.content
    print(tweet_text)
    tweet_text = tweet_text[:post_length] + "... " + tweet_url
    """
    tweet_text = response.choices[0].message.content + "   " + tweet_url
    return tweet_text