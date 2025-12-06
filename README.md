# 👁️ Horus - Docker Container Monitor

**The All-Seeing Eye** - A minimalist web panel to monitor and access any Docker container instances with real-time control.

## 📋 Features

- ✅ Visualize all Docker containers (active and inactive)
- 🔄 Auto-refresh every 30 seconds
- 🚀 Direct access with one click to each instance
- ⚡ Start/Stop containers directly from the interface
- 📊 Real-time statistics
- ⚙️ 100% configurable via environment variables
- 🔌 Filter by container name and specific ports
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
     - CONTAINER_FILTER=myapp        # Pattern to filter containers (leave empty for all)
     - PANEL_PORT=5000               # Panel port
     - SERVER_HOST=192.168.1.100     # IP/domain of your server
     - DEFAULT_TCP_PORT=8080/tcp     # Specific port to filter (e.g., 8069/tcp, 3000/tcp)
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
  -e CONTAINER_FILTER=myapp \
  -e PANEL_PORT=5000 \
  -e SERVER_HOST=192.168.1.100 \
  -e DEFAULT_TCP_PORT=8080/tcp \
  horus
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default Value | Examples |
|----------|-------------|---------------|----------|
| `CONTAINER_FILTER` | Pattern to filter container names (leave empty to show all) | `""` (empty) | `webapp`, `prod-`, `api` |
| `PANEL_PORT` | Port where the panel runs | `5000` | `5000`, `8080`, `3000` |
| `SERVER_HOST` | IP/domain of the Docker server | `localhost` | `192.168.1.100`, `myapp.company.com` |
| `DEFAULT_TCP_PORT` | Specific TCP port to filter containers | `""` (empty) | `8069/tcp`, `3000/tcp`, `80/tcp` |

### Configuration Examples

**Monitor all containers:**
```yaml
environment:
  - CONTAINER_FILTER=                # Empty = show all containers
  - PANEL_PORT=5000
  - SERVER_HOST=192.168.1.100
  - DEFAULT_TCP_PORT=                # Empty = any port
```

**Monitor specific application (e.g., web apps on port 8080):**
```yaml
environment:
  - CONTAINER_FILTER=webapp
  - PANEL_PORT=5000
  - SERVER_HOST=myserver.com
  - DEFAULT_TCP_PORT=8080/tcp
```

**Monitor production containers only:**
```yaml
environment:
  - CONTAINER_FILTER=prod-
  - PANEL_PORT=8080
  - SERVER_HOST=192.168.1.100
  - DEFAULT_TCP_PORT=
```

**Monitor database containers on port 5432:**
```yaml
environment:
  - CONTAINER_FILTER=postgres
  - PANEL_PORT=5000
  - SERVER_HOST=localhost
  - DEFAULT_TCP_PORT=5432/tcp
```

## 🔧 Requirements

- Docker Engine 20.10+
- Docker Compose 2.0+ (optional)
- Containers with ports mapped to the host (for URL access)

## 📝 Important Notes

1. **Docker Socket**: The container needs access to the Docker socket (`/var/run/docker.sock`) to query and control other containers.

2. **Mapped Ports**: Only containers with ports mapped to the host will show a clickable URL. Containers in internal networks without port exposure will still be visible but won't have an accessible URL.

3. **Container Filter**: 
   - The filter searches for the pattern in the container NAME (case-sensitive substring match)
   - Leave `CONTAINER_FILTER` empty to show ALL containers
   - Examples:
     - `CONTAINER_FILTER=web` will find: `webapp`, `web-server`, `my-web-api`
     - `CONTAINER_FILTER=prod-` will find: `prod-api`, `prod-database`, `prod-frontend`

4. **Port Filter**: 
   - Use `DEFAULT_TCP_PORT` to show only containers exposing a specific port
   - Format must include `/tcp` (e.g., `8069/tcp`, `3000/tcp`)
   - Leave empty to show containers with any port mapping

5. **Security**: The container runs with a non-root user and the Docker socket is mounted in read-only mode for listing. Write operations (start/stop) require appropriate permissions.

6. **Container Control**: The interface allows you to start and stop containers directly. Use this feature carefully in production environments.

## 🛠️ Troubleshooting

### No containers are shown
- Verify that the `CONTAINER_FILTER` filter matches your container names (or set it to empty)
- Check if `DEFAULT_TCP_PORT` is too restrictive
- Check the logs: `docker logs horus`

### Docker connection error
- Make sure the socket is mounted correctly: `-v /var/run/docker.sock:/var/run/docker.sock:ro`
- Verify permissions: `ls -la /var/run/docker.sock`
- On some systems, you may need to add the container to the `docker` group

### URLs don't work
- Confirm that `SERVER_HOST` is the correct IP/domain
- Verify that ports are correctly mapped in your containers
- Check if containers are actually running

### Can't start/stop containers
- Verify the Docker socket has write permissions (remove `:ro` if needed, though not recommended)
- Check container logs for specific errors
- Ensure the container isn't in a restarting loop

## 📊 API Endpoints

The panel exposes the following endpoints:

- `GET /` - Web interface
- `GET /api/containers` - Container list (JSON)
- `POST /api/containers/start/<container_id>` - Start a stopped container
- `POST /api/containers/stop/<container_id>` - Stop a running container
- `GET /api/health` - Service health status

## 🔄 Update

To update the panel:

```bash
docker-compose down
docker-compose up -d --build
```

Or with Docker run:

```bash
docker stop horus
docker rm horus
docker build -t horus .
docker run -d --name horus -p 5000:5000 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -e CONTAINER_FILTER= \
  -e PANEL_PORT=5000 \
  -e SERVER_HOST=localhost \
  horus
```

## 🎨 About the Name

**Horus** is the ancient Egyptian sky god, often depicted with the Eye of Horus - a symbol of protection, royal power, and good health. The eye represents the all-seeing watchfulness, making it the perfect name for a container monitoring system.

## 💡 Use Cases

- **Development**: Monitor all your local containers across different projects
- **Production**: Track specific application containers (filter by name/port)
- **DevOps**: Quick overview and control of container states
- **Multi-tenant**: Monitor containers by client/project using name filters
- **Microservices**: Track all services on specific ports

## 📄 License

Free for personal and commercial use.

## 🤝 Support

For issues or suggestions:
- Check the configuration and container logs
- Verify Docker socket permissions
- Review the filter patterns (CONTAINER_FILTER and DEFAULT_TCP_PORT)
- Test with empty filters first to see all containers

## 🔐 Security Recommendations

1. **Read-only socket**: Keep the `:ro` flag on the Docker socket mount when possible
2. **Network isolation**: Use Docker networks to isolate Horus
3. **Authentication**: Consider adding a reverse proxy with authentication for production use
4. **Port exposure**: Only expose the panel port to trusted networks
5. **Regular updates**: Keep Docker and Horus updated to the latest versions