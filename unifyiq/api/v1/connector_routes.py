from flask import Blueprint, request

from utils.database.unifyiq_config_db import get_fetcher_configs, add_fetcher_config

connector_routes = Blueprint('connector_routes', __name__)


@connector_routes.route('/list')
def get_all():
    query_result = get_fetcher_configs()
    configs_list = []
    for row in query_result:
        config_dict = {
            'id': row.id,
            'name': row.name,
            'connector_type': row.connector_type,
            'url_prefix': row.url_prefix,
            'cron_expr': row.cron_expr,
            'last_fetched_ts': row.last_fetched_ts,
        }
        configs_list.append(config_dict)
    return configs_list, 200


@connector_routes.route('/new', methods=['POST'])
def add_new():
    try:
        data = request.get_json()
        name = data['name']
        connector_type = data['connector_type']
        url_prefix = data['url_prefix']
        cron_expr = 0
        start_ts = data['start_ts']
        last_fetched_ts = data['last_fetched_ts']
        is_enabled = data['is_enabled']
        add_fetcher_config(name, connector_type, url_prefix, cron_expr, start_ts, last_fetched_ts, is_enabled)
        return {'status': 'success'}, 201
    except Exception as e:
        print(str(e))
        return {'error': 'Please try again'}, 400
