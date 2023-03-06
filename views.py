from typing import Tuple, Union, Dict, List

from flask import Blueprint, jsonify, request, Response
from marshmallow import ValidationError
from builder import build_query
from models import BatchRequestSchema

main_bp = Blueprint('main', __name__)


@main_bp.route('/perform_query', methods=['POST'])
def perform_query() -> Union[Response, Tuple[Response, int]]:

    data: Dict[str, Union[List[dict], str]] = request.json

    try:
        validated_data = BatchRequestSchema().load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    result = None

    for query in validated_data['queries']:
        result = build_query(
            cmd=query['cmd'],
            value=query['value'],
            file_name=validated_data['file_name'],
            data=result,
        )

    return jsonify(result)
