from flask import jsonify
from services.store_service import get_health_summary


def health_check():
    try:
        return jsonify(get_health_summary()), 200
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500
