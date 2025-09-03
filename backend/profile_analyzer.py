import requests
import random
from datetime import datetime, timedelta
import time
import os
from typing import Dict, List, Any

class ProfileAnalyzer:
    """Backend service for analyzing social media profiles for authenticity and coordinated campaigns"""
    
    def __init__(self):
        self.twitter_api_key = os.getenv("TWITTER_API_KEY", "")
        self.instagram_api_key = os.getenv("INSTAGRAM_API_KEY", "")
        self.facebook_api_key = os.getenv("FACEBOOK_API_KEY", "")
        
        # Known VIP database for demo purposes
        self.known_vips = {
            "@elonmusk": {
                "name": "Elon Musk",
                "twitter_verified": True,
                "instagram_verified": True,
                "facebook_verified": True,
                "official_website": "https://www.tesla.com"
            },
            "@oprah": {
                "name": "Oprah Winfrey",
                "twitter_verified": True,
                "instagram_verified": True,
                "facebook_verified": True,
                "official_website": "https://www.oprah.com"
            },
            "@realdonaldtrump": {
                "name": "Donald Trump",
                "twitter_verified": False,  # Account suspended
                "instagram_verified": True,
                "facebook_verified": True,
                "official_website": "https://www.donaldjtrump.com"
            }
        }

    def fetch_twitter_profile(self, handle: str) -> Dict:
        """Fetch or simulate Twitter profile data"""
        clean_handle = handle.lstrip("@")
        time.sleep(0.5)  # Simulate API delay
        
        is_known_vip = clean_handle.lower() in (name.lstrip("@").lower() for name in self.known_vips)
        
        return {
            "platform": "Twitter",
            "handle": f"@{clean_handle}",
            "verified": is_known_vip or random.choice([True, False]),
            "verification_type": "legacy" if is_known_vip else "subscription",
            "followers": random.randint(10000, 50000000) if is_known_vip else random.randint(10, 100000),
            "following": random.randint(100, 10000),
            "created_date": self._random_date(),
            "tweets_count": random.randint(500, 100000),
            "profile_pic_url": f"https://example.com/{clean_handle}.jpg",
            "bio": f"Official @ {clean_handle} account" if is_known_vip else f"Account for {clean_handle}",
            "website": self.known_vips.get(f"@{clean_handle}", {}).get("official_website", ""),
            "location": random.choice(["New York, NY", "Los Angeles, CA", "London, UK", ""]),
            "join_days_ago": random.randint(100, 5000)
        }

    def fetch_instagram_profile(self, handle: str) -> Dict:
        """Fetch or simulate Instagram profile data"""
        clean_handle = handle.lstrip("@")
        time.sleep(0.5)
        is_known_vip = clean_handle.lower() in (name.lstrip("@").lower() for name in self.known_vips)
        
        return {
            "platform": "Instagram",
            "handle": f"@{clean_handle}",
            "verified": is_known_vip or random.choice([True, False]),
            "followers": random.randint(5000, 30000000) if is_known_vip else random.randint(100, 50000),
            "following": random.randint(50, 5000),
            "created_date": self._random_date(),
            "posts_count": random.randint(100, 10000),
            "profile_pic_url": f"https://example.com/{clean_handle}_insta.jpg",
            "bio": f"Official @ {clean_handle} Instagram" if is_known_vip else f"Account for {clean_handle}",
            "website": self.known_vips.get(f"@{clean_handle}", {}).get("official_website", ""),
            "category": "Public Figure" if is_known_vip else "Personal",
        }

    def fetch_facebook_profile(self, handle: str) -> Dict:
        """Fetch or simulate Facebook page/profile data"""
        clean_handle = handle.lstrip("@")
        time.sleep(0.5)
        is_known_vip = clean_handle.lower() in (name.lstrip("@").lower() for name in self.known_vips)
        return {
            "platform": "Facebook",
            "handle": clean_handle,
            "verified": is_known_vip or random.choice([True, False]),
            "likes": random.randint(10000, 100000000) if is_known_vip else random.randint(10, 100000),
            "followers": random.randint(10000, 30000000) if is_known_vip else random.randint(100, 50000),
            "created_date": self._random_date(),
            "about": f"Official @ {clean_handle} Facebook Page" if is_known_vip else f"Facebook Page for {clean_handle}",
            "website": self.known_vips.get(f"@{clean_handle}", {}).get("official_website", ""),
            "category": "Public Figure" if is_known_vip else "Personal",
        }

    def analyze_authenticity(self, profiles: Dict[str, Dict]) -> Dict:
        """Analyze profile data for authenticity indicators"""
        score = 0
        max_score = len(profiles) * 6  # 6 checks per platform
        issues = []
        positives = []
        for platform, data in profiles.items():
            platform_score = 0
            # Verification badge
            if data.get("verified", False):
                platform_score += 1
                positives.append(f"✅ {platform} Verified badge present")
            else:
                issues.append(f"⚠️ {platform} Missing verified badge")
            # Follower ratio
            followers = data.get("followers", 0)
            following = data.get("following", 1)
            if followers > following * 5:
                platform_score +=1
                positives.append(f"✅ {platform} Healthy follower-following ratio")
            else:
                issues.append(f"⚠️ {platform} Suspicious follower-following ratio")
            # Profile completeness
            if data.get("bio", "") or data.get("about", ""):
                platform_score += 1
                positives.append(f"✅ {platform} Profile bio/about complete")
            else:
                issues.append(f"⚠️ {platform} Profile missing bio/about info")
            # Website presence
            if data.get("website"):
                platform_score += 1
                positives.append(f"✅ {platform} Official website linked")
            else:
                issues.append(f"⚠️ {platform} No website linked")
            # Account age - simplified (assuming join_days_ago)
            if data.get("join_days_ago", 0) > 365:
                platform_score += 1
                positives.append(f"✅ {platform} Account older than 1 year")
            else:
                issues.append(f"⚠️ {platform} Account newer than 1 year")
            # Activity level
            posts = data.get("posts_count") or data.get("tweets_count") or 0
            if posts > 100:
                platform_score += 1
                positives.append(f"✅ {platform} Active posting history")
            else:
                issues.append(f"⚠️ {platform} Low posting history")
            score += platform_score
        authenticity_percent = (score / max_score) * 100 if max_score else 0
        return {
            "score": authenticity_percent,
            "issues": issues,
            "positives": positives,
        }

    def detect_suspicious_patterns(self, profiles: Dict[str, Dict]) -> List[Dict]:
        """Detect suspicious impersonation or anomalies"""
        suspicious = []
        for platform, data in profiles.items():
            # Verification type - subscription (vs legacy)
            if data.get("verification_type") == "subscription":
                suspicious.append({
                    "platform": platform,
                    "issue": "Subscription verification badge - may be less reliable",
                    "confidence": 0.5
                })
            # Username oddities
            handle = data.get("handle", "").lower()
            if any(x in handle for x in ["_official", "_real", "2023", "2024", "2025"]):
                suspicious.append({
                    "platform": platform,
                    "issue": f"Suspicious username pattern: {handle}",
                    "confidence": 0.75
                })
            # Follower anomalies
            followers = data.get("followers", 0)
            following = data.get("following", 1)
            if followers and following:
                ratio = followers/following
                if ratio < 0.5:
                    suspicious.append({
                        "platform": platform,
                        "issue": f"Low followers-to-following ratio: {ratio:.2f}",
                        "confidence": 0.6
                    })
        return suspicious

    def detect_coordinated_campaigns(self, handle: str) -> Dict:
        """Mock detection of coordinated campaigns"""
        campaigns = []
        if random.random() < 0.3:
            campaigns.append({
                "type": "Impersonation",
                "accounts": [f"{handle}_fake1", f"{handle}_spam2", f"{handle}_bot3"],
                "platforms": ["Twitter", "Instagram"],
                "pattern": "Frequent identical posts in bursts",
                "risk": "High",
            })
        if random.random() < 0.2:
            campaigns.append({
                "type": "Smear Campaign",
                "accounts": [f"expose_{handle}", f"truth_{handle}"],
                "platforms": ["Facebook", "Twitter"],
                "pattern": "Simultaneous negative messaging",
                "risk": "Medium"
            })
        risk_level = "High" if any(c["risk"]=="High" for c in campaigns) else "Medium" if campaigns else "Low"
        return {
            "campaigns": campaigns,
            "risk_level": risk_level
        }
