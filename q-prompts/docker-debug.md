# Debugging Docker Issues  

## **Prompt** (2025-10-05)  

```text
Explain why this Celery worker fails in Docker:  
- Error: "Connection refused to redis://redis:6379"  
- Relevant docker-compose.yml:  
  ```yaml
  services:
    redis:
      image: redis:7
    worker:
      depends_on: [redis]
  ```

```

**Amazon Q Diagnosis**:  
> "The worker starts before Redis is ready. Add:  
> ```yaml
> healthcheck:
>   test: ["CMD", "redis-cli", "ping"]  
>   interval: 5s
> ```"

**Result**: Fixed by adding health checks + startup delays.
