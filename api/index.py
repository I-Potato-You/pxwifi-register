from flask import Flask, request, jsonify
from 平行python import main as registration_main
import threading
import traceback
import sys
import os

app = Flask(__name__)

@app.route('/api/register', methods=['POST'])
def register():
    try:
        # 打印当前工作目录和Python路径
        print(f"Current working directory: {os.getcwd()}")
        print(f"Python path: {sys.path}")
        
        data = request.json
        if not data:
            return jsonify({'status': 'error', 'message': '无效的请求数据'}), 400
            
        invite_code = data.get('inviteCode')
        count = data.get('count', 1)
        
        print(f"Received request with invite_code: {invite_code}, count: {count}")
        
        def run_registration():
            try:
                # 确保传递参数给主函数
                registration_main(invite_code=invite_code, count=count)
                return {'status': 'success', 'message': '注册完成'}
            except Exception as e:
                error_trace = traceback.format_exc()
                print(f"Registration error: {str(e)}\nTrace: {error_trace}")
                return {'status': 'error', 'message': str(e), 'trace': error_trace}
        
        thread = threading.Thread(target=run_registration)
        thread.start()
        
        return jsonify({
            'status': 'started', 
            'message': '注册流程已启动',
            'details': {
                'invite_code': invite_code,
                'count': count
            }
        })
        
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"API error: {str(e)}\nTrace: {error_trace}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'trace': error_trace,
            'type': type(e).__name__
        }), 500

@app.errorhandler(Exception)
def handle_error(e):
    error_trace = traceback.format_exc()
    print(f"Unhandled error: {str(e)}\nTrace: {error_trace}")
    return jsonify({
        'status': 'error',
        'message': str(e),
        'trace': error_trace,
        'type': type(e).__name__
    }), 500

def handler(request):
    try:
        with app.app_context():
            return app(request)
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Handler error: {str(e)}\nTrace: {error_trace}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'trace': error_trace,
            'type': type(e).__name__
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 