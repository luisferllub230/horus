from flask import Flask, render_template, jsonify
import docker
import os
from datetime import datetime

app = Flask(__name__)

# ============================================
# CONFIGURATION - Modify these values
# ============================================

# Pattern to filter containers (regex or substring)
# Examples: "odoo", "odoo-", "^odoo.*", etc.
CONTAINER_FILTER_PATTERN = os.getenv('CONTAINER_FILTER', 'odoo')

# Port where this panel will run
PANEL_PORT = int(os.getenv('PANEL_PORT', '5000'))

# Host/IP of the server (used to build URLs)
# If not specified, localhost will be used
SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')

# Default Odoo port if no mapping is found
DEFAULT_ODOO_PORT = 8069

# ============================================

client = docker.from_env()

def get_container_info(container):
    """Extrae información relevante de un contenedor"""
    try:
        ports = container.attrs['NetworkSettings']['Ports']
        public_port = None
        
        for container_port, mappings in ports.items() if ports else []:
            if mappings:
                public_port = mappings[0]['HostPort']
                break
        
        state = container.status
        is_running = state == 'running'
        
        url = None
        if public_port and is_running:
            url = f"http://{SERVER_HOST}:{public_port}"
        
        started_at = container.attrs['State'].get('StartedAt', '')
        
        return {
            'id': container.id[:12],
            'name': container.name,
            'status': state,
            'is_running': is_running,
            'public_port': public_port,
            'url': url,
            'image': container.image.tags[0] if container.image.tags else 'unknown',
            'started_at': started_at
        }
    except Exception as e:
        print(f"Error obteniendo info del contenedor {container.name}: {e}")
        return None

@app.route('/')
def index():
    """Página principal del panel"""
    return render_template('index.html', 
                         filter_pattern=CONTAINER_FILTER_PATTERN,
                         server_host=SERVER_HOST)

@app.route('/api/containers')
def get_containers():
    """API para obtener la lista de contenedores filtrados"""
    try:
        all_containers = client.containers.list(all=True)
        print(f"all containers --> {all_containers}")
        
        filtered_containers = []
        for container in all_containers:
            # if CONTAINER_FILTER_PATTERN.lower() in container.name.lower():
            info = get_container_info(container)
            if info:
                filtered_containers.append(info)
        
        filtered_containers.sort(key=lambda x: (not x['is_running'], x['name']))
        
        return jsonify({
            'success': True,
            'containers': filtered_containers,
            'total': len(filtered_containers),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health')
def health():
    """Endpoint de salud"""
    try:
        client.ping()
        return jsonify({'status': 'healthy', 'docker': 'connected'})
    except:
        return jsonify({'status': 'unhealthy', 'docker': 'disconnected'}), 503

if __name__ == '__main__':
    print(f"🚀 Panel de Control Odoo iniciando...")
    print(f"📦 Filtro de contenedores: '{CONTAINER_FILTER_PATTERN}'")
    print(f"🌐 Servidor: {SERVER_HOST}")
    print(f"🔌 Puerto del panel: {PANEL_PORT}")
    app.run(host='0.0.0.0', port=PANEL_PORT, debug=False)