
import json
import requests

from odoo import models, fields, _
from odoo.exceptions import UserError
from werkzeug.urls import url_join
import logging

_logger = logging.getLogger(__name__)

class SocialLivePostFacebook(models.Model):
    _inherit = 'social.live.post'

    def _refresh_statistics(self):
        accounts = self.env['social.account'].search([('media_type', '=', 'facebook')])
        accounts.write({'active': 'False'})
        super(SocialLivePostFacebook, self)._refresh_statistics()
        accounts.write({'active': 'True'})

        for account in accounts:
            posts_endpoint_url = url_join(self.env['social.media']._FACEBOOK_ENDPOINT, "/v10.0/%s/%s" % (account.facebook_account_id, 'feed'))
            result = requests.get(posts_endpoint_url,
                params={
                    'access_token': account.facebook_access_token,
                    'fields': 'id,shares,insights.metric(post_impressions),likes.limit(1).summary(true),comments.summary(true)'
                },
                timeout=5
            )

            result_posts = result.json().get('data')
            if not result_posts:
                _logger.warning(f"LSE NOT result_posts {account} {account.name} {result.json()}")
                account.sudo().write({'is_media_disconnected': True})
                return
            else:
                _logger.warning(f"LSE OK result_posts {account} {account.name} {result.json()}")

            facebook_post_ids = [post.get('id') for post in result_posts]
            existing_live_posts = self.env['social.live.post'].sudo().search([
                ('facebook_post_id', 'in', facebook_post_ids)
            ])

            existing_live_posts_by_facebook_post_id = {
                live_post.facebook_post_id: live_post for live_post in existing_live_posts
            }

            for post in result_posts:
                existing_live_post = existing_live_posts_by_facebook_post_id.get(post.get('id'))
                if existing_live_post:
                    likes_count = post.get('likes', {}).get('summary', {}).get('total_count', 0)
                    shares_count = post.get('shares', {}).get('count', 0)
                    comments_count = post.get('comments', {}).get('summary', {}).get('total_count', 0)
                    existing_live_post.write({
                        'engagement': likes_count + shares_count + comments_count,
                    })