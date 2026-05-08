**Bash**
*uvicorn app.main:app --reload*
`--reload` Automatically restarts the server when code change

*curl flags: -H and -d*
`-H` → Header, Metadata sent with the request.
`-d` → Data (request body), Sends data to the server (usually for POST/PUT)

**Docker**
`docker image prune`: Remove dangling images only (safe)

*PYTHONDONTWRITEBYTECODE=1*
1. Cleaner container: No unnecessary cache files created at runtime
2. Less disk I/O. Important in:
- containers
- serverless
- ephemeral systems
3. Predictable behavior: No hidden files being created

*PYTHONUNBUFFERED=1*
Forces logs to flush immediately
With it → real-time logs
- Docker logs
- Kubernetes logs
- Monitoring systems

**Python**
`app.include_router(router)`: attaching routes from routes.py into the main app
`.isoformat()`: Type = string, Use it when:
- writing logs
- sending data outside FastAPI
- storing in files

**Monitoring**
`docker logs -f devops-api` Live logs
`--restart always` Restart automatically
`docker stats` CPU %, Memory usage, Network I/O
`watch -n 5 curl http://YOUR_PUBLIC_IP:8000/health` Create a script locally: Every 5 seconds = check uptime

**Terraform**
On one command(`apply`) with `-var=` Terraform loads all .tf files in the directory together as ONE configuration.
BUT after command finishes Terraform process exits.
The runtime variable assignment disappears. (`key_name = var.key_name`)
When you run terraform destroy
Terraform still:
 - loads all .tf files
 - parses resources
 - evaluates variables
 - builds dependency graph
 - then deletes resources

So if your config contains: `key_name = var.key_name`
Terraform still needs: `var.key_name`