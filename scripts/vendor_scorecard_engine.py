# scripts/vendor_scorecard_engine.py

import pandas as pd
from collections import defaultdict
from datetime import datetime
from transformers import pipeline


def extract_prices(ner_pipeline, text):
    entities = ner_pipeline(text)
    prices = []
    current_price = []

    for ent in entities:
        # Use 'entity_group' if present (aggregated mode), else fallback to 'entity'
        label = ent.get("entity", "") or ent.get("entity_group", "")

        if "PRICE" in label:
            current_price.append(ent["word"])
        elif current_price:
            try:
                # Join tokens, remove common currency symbols/words, convert to float
                joined = "".join(current_price).replace("ብር", "").replace(",", "").strip()
                prices.append(float(joined))
            except:
                pass
            current_price = []

    # Final flush if text ends with a PRICE
    if current_price:
        try:
            joined = "".join(current_price).replace("ብር", "").replace(",", "").strip()
            prices.append(float(joined))
        except:
            pass

    return prices


def score_vendors(df, ner_pipeline):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['week'] = df['timestamp'].dt.to_period('W').astype(str)


    vendor_stats = defaultdict(dict)

    for vendor, group in df.groupby('vendor'):
        # Activity
        total_posts = len(group)
        weeks = group['week'].nunique()
        posts_per_week = total_posts / weeks if weeks else 0

        # Views
        avg_views = group['views'].mean()
        top_post = group.loc[group['views'].idxmax()]
        top_text = top_post['text']
        top_views = top_post['views']

        # Prices
        all_prices = []
        for text in group['text']:
            prices = extract_prices(ner_pipeline, text)
            all_prices.extend(prices)
        avg_price = sum(all_prices) / len(all_prices) if all_prices else 0

        # Lending score (simple example)
        lending_score = (avg_views * 0.5) + (posts_per_week * 0.5)

        vendor_stats[vendor] = {
            'Avg. Views/Post': round(avg_views, 1),
            'Posts/Week': round(posts_per_week, 1),
            'Avg. Price (ETB)': round(avg_price, 2),
            'Top Post': top_text,
            'Top Views': top_views,
            'Lending Score': round(lending_score, 2)
        }

    return pd.DataFrame.from_dict(vendor_stats, orient='index').reset_index(names='Vendor')
