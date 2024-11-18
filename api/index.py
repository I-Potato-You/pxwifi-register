from flask import Flask, request, jsonify
from 平行python import main as registration_main
import threading
import traceback

app = Flask(__name__)

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        if not data:
            return jsonify({'status': 'error', 'message': '无效的请求数据'}), 400
            
        invite_code = data.get('inviteCode')
        count = data.get('count', 1)
        
        def run_registration():
            try:
                registration_main()
                return {'status': 'success', 'message': '注册完成'}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        
        thread = threading.Thread(target=run_registration)
        thread.start()
        
        return jsonify({'status': 'started', 'message': '注册流程已启动'})
        
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error: {str(e)}\nTrace: {error_trace}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'trace': error_trace
        }), 500

@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({
        'status': 'error',
        'message': str(e),
        'type': type(e).__name__
    }), 500

def handler(request):
    with app.app_context():
        return app(request)

if __name__ == '__main__':
    app.run(debug=True) 