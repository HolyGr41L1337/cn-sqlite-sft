CREATE TABLE user_profile (id INTEGER PRIMARY KEY, username TEXT, email TEXT, created_at TEXT, status TEXT);
CREATE TABLE post (id INTEGER PRIMARY KEY, user_profile_id INTEGER, content TEXT, posted_at TEXT, like_count INTEGER);
CREATE TABLE comment (id INTEGER PRIMARY KEY, post_id INTEGER, user_profile_id INTEGER, comment_text TEXT, commented_at TEXT);
CREATE TABLE follow (id INTEGER PRIMARY KEY, follower_id INTEGER, followee_id INTEGER, followed_at TEXT);
