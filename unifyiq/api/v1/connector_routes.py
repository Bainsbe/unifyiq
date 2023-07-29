import json

from flask import Blueprint, request, jsonify

from fetchers.adapters.fetcher_configs import FETCHER_CONFIG_VALUES
from utils.database.unifyiq_config_db import get_fetcher_configs, add_fetcher_config
from utils.time_utils import format_utc_timestamp

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
            'is_enabled': "False" if row.is_enabled == 0 else "True",
            'last_fetched_ts': format_utc_timestamp(row.last_fetched_ts),
            'start_ts': format_utc_timestamp(row.start_ts),
        }
        configs_list.append(config_dict)
    return configs_list, 200


@connector_routes.route('/fetcher_config_values')
def fetcher_config_values():
    return jsonify(FETCHER_CONFIG_VALUES)


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
        config_json = json.dumps(data['config_json'])
        add_fetcher_config(name, connector_type, url_prefix, cron_expr, start_ts, last_fetched_ts, is_enabled,
                           config_json)
        return {'status': 'success'}, 201
    except Exception as e:
        print(str(e))
        print('hello noooooo')
        return {'error': 'Please try again'}, 400
