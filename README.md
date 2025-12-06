# 👁️ Horus - Docker Container Monitor

**The All-Seeing Eye** - A minimalist web panel to monitor and access Odoo instances running in Docker containers.

## 📋 Features

- ✅ Visualize all Odoo containers (active and inactive)
- 🔄 Auto-refresh every 30 seconds
- 🚀 Direct access with one click to each instance
- 📊 Real-time statistics
- ⚙️ 100% configurable via environment variables
- 🪶 Minimalist and responsive design

## 🏗️ File Structure

```
.
├── app.py                  # Flask application
├── templates/
│   └── index.html         # Web interface
├── Dockerfile             # Docker image
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Installation and Usage

### Option 1: Docker Compose (Recommended)

1. **Create the files** in a directory (e.g.: `/opt/horus/`)

2. **Edit `docker-compose.yml`** and configure the variables:
   ```yaml
   environment:
     - CONTAINER_FILTER=odoo        # Pattern to filter containers
     - PANEL_PORT=5000              # Panel port
     - SERVER_HOST=192.168.1.100    # IP/domain of your server
   ```

3. **Build and start the container**:
   ```bash
   docker-compose up -d --build
   ```

4. **Access the panel**:
   ```
   http://your-server:5000
   ```

### Option 2: Docker Run

```bash
# Build the image
docker build -t horus .

# Run the container
docker run -d \
  --name horus \
  -p 5000:5000 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -e CONTAINER_FILTER=odoo \
  -e PANEL_PORT=5000 \
  -e SERVER_HOST=192.168.1.100 \
  horus
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default Value | Examples |
|----------|-------------|---------------|----------|
| `CONTAINER_FILTER` | Pattern to filter container names | `odoo` | `odoo`, `odoo-prod`, `erp` |
| `PANEL_PORT` | Port where the panel runs | `5000` | `5000`, `8080`, `3000` |
| `SERVER_HOST` | IP/domain of the Docker server | `localhost` | `192.168.1.100`, `odoo.company.com` |

### Configuration Examples

**Production with multiple instances:**
```yaml
environment:
  - CONTAINER_FILTER=odoo-prod
  - PANEL_PORT=8080
  - SERVER_HOST=odoo.mycompany.com
```

**Local development:**
```yaml
environment:
  - CONTAINER_FILTER=odoo
  - PANEL_PORT=5000
  - SERVER_HOST=localhost
```

**Filter only testing instances:**
```yaml
environment:
  - CONTAINER_FILTER=odoo-test
  - PANEL_PORT=5000
  - SERVER_HOST=192.168.1.50
```

## 🔧 Requirements

- Docker Engine 20.10+
- Docker Compose 2.0+ (optional)
- Odoo containers with ports mapped to the host

## 📝 Important Notes

1. **Docker Socket**: The container needs access to the Docker socket (`/var/run/docker.sock`) to query information from other containers.

2. **Mapped Ports**: Only containers with ports mapped to the host will be shown. Containers in internal networks without exposure will not show a URL.

3. **Container Filter**: The filter searches for the pattern in the container NAME (case-insensitive). For example:
   - `CONTAINER_FILTER=odoo` will find: `odoo-prod`, `my-odoo-test`, `odoo_v16`
   - `CONTAINER_FILTER=odoo-prod` will find: `odoo-prod-1`, `odoo-prod-backup`

4. **Security**: The container runs with a non-root user and the Docker socket is mounted in read-only mode.

## 🛠️ Troubleshooting

### No containers are shown
- Verify that the `CONTAINER_FILTER` filter matches your container names
- Check the logs: `docker logs horus`

### Docker connection error
- Make sure the socket is mounted correctly
- Verify permissions: `ls -la /var/run/docker.sock`

### URLs don't work
- Confirm that `SERVER_HOST` is the correct IP/domain
- Verify that ports are correctly mapped in your Odoo containers

## 📊 API Endpoints

The panel exposes the following endpoints:

- `GET /` - Web interface
- `GET /api/containers` - Container list (JSON)
- `GET /api/health` - Service health status

## 🔄 Update

To update the panel:

```bash
docker-compose down
docker-compose up -d --build
```

## 🎨 About the Name

**Horus** is the ancient Egyptian sky god, often depicted with the Eye of Horus - a symbol of protection, royal power, and good health. The eye represents the all-seeing watchfulness, making it the perfect name for a container monitoring system.

## 📄 License

Free for personal and commercial use.

## 🤝 Support

For issues or suggestions, check the configuration and container logs.