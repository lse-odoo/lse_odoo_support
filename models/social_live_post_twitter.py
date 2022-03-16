
import json
import requests

from odoo import models, fields, _
from odoo.exceptions import UserError
from werkzeug.urls import url_join
import logging

_logger = logging.getLogger(__name__)

class SocialLivePostTwitter(models.Model):
    _inherit = 'social.live.post'

    def _refresh_statistics(self):
        accounts = self.env['social.account'].search([('media_type', '=', 'twitter')])
        accounts.write({'active': 'False'})
        super(SocialLivePostTwitter, self)._refresh_statistics()
        accounts.write({'active': 'True'})

        endpoint_name = 'statuses/user_timeline'
        for account in accounts:
            query_params = {
                'user_id': account.twitter_user_id,
                'tweet_mode': 'extended',
                'count': 100
            }
            tweets_endpoint_url = url_join(self.env['social.media']._TWITTER_ENDPOINT, "/1.1/%s.json" % endpoint_name)
            headers = account._get_twitter_oauth_header(
                tweets_endpoint_url,
                params=query_params,
                method='GET'
            )
            result = requests.get(
                tweets_endpoint_url,
                query_params,
                headers=headers
            )

            result_tweets = result.json()
            _logger.warning(f"LSE result_posts TWITTER {result_tweets}")
            if isinstance(result_tweets, dict) and result_tweets.get('errors') or result_tweets is None:
                _logger.warning(f"LSE TWITTER disconnected BP")
                account.sudo().write({'is_media_disconnected': True})
                return

            tweets_ids = [tweet.get('id_str') for tweet in result_tweets]
            existing_live_posts = self.env['social.live.post'].sudo().search([
                ('twitter_tweet_id', 'in', tweets_ids)
            ])

            existing_live_posts_by_tweet_id = {
                live_post.twitter_tweet_id: live_post for live_post in existing_live_posts
            }

            for tweet in result_tweets:
                existing_live_post = existing_live_posts_by_tweet_id.get(tweet.get('id_str'))
                if existing_live_post:
                    likes_count = tweet.get('favorite_count', 0)
                    retweets_count = tweet.get('retweet_count', 0)
                    existing_live_post.write({
                        'engagement': likes_count + retweets_count
                    })

